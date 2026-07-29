# Task Manager Application: Project Findings & Structure

## Exercise Part 1: Understanding Project Structure

### 1. Initial Understanding & Assumptions
Before running the AI analysis, my initial observations were:
* **Application Purpose:** A Task Manager application to create, organize, and manage to-do lists.
* **Technology Stack:** Built using JavaScript and Node.js (identified via `package.json` and `.js` file extensions).
* **Codebase Structure:** A flat root folder structure where all core JavaScript logic sits alongside a dedicated `tests/` directory.

### 2. AI Analysis vs. Initial Assumptions (Misconceptions Corrected)
* **CLI vs. Web App:** This is specifically a **Command Line Interface (CLI)** application that runs purely in the terminal (`node cli.js`). There is no front-end web UI or database server.
* **Actual Entry Point:** `cli.js` is the true entry point where user commands enter the application, while `app.js` holds internal business logic (`TaskManager`).
* **Data Storage:** Data is persisted directly to a local file called `tasks.json` managed via `storage.js`.
* **Stand-alone / Modular Utilities:** `task_parser.js`, `task_priority.js`, and `task_list_merge.js` have active test suites but act as modular building blocks for future features.

### 3. Technology Stack & Key Libraries
| Technology / Library | Role & Purpose |
| :--- | :--- |
| **Node.js** | Runtime environment executing JavaScript outside the browser. |
| **JavaScript (CommonJS)** | Primary language using standard `require()` and `module.exports`. |
| **`commander`** | External library in `cli.js` used to parse terminal commands and flags. |
| **`uuid`** | Library in `models.js` used to generate unique IDs for tasks. |
| **`Jest`** | Test runner executing automated tests in the `tests/` directory. |
| **Node.js `fs` Module** | Built-in module used in `storage.js` to read/write task data to disk. |

### 4. Key Components & Responsibilities
1. **`cli.js` (Interface):** Receives user commands in the terminal and passes instructions to `app.js`.
2. **`app.js` (Business Logic):** Contains `TaskManager`. Coordinates creating, listing, updating, and deleting tasks.
3. **`models.js` (Domain Models):** Defines what a `Task` object is (title, priority, status, dates, unique ID).
4. **`storage.js` (Persistence):** Handles reading from and writing to `tasks.json`.

---

## Exercise Part 2: Finding Feature Implementation (Task Export to CSV)

### 1. Initial Search & Approach Evaluation
* **Search Terms Used:** `storage`, `writeFile`, `JSON`, `task`.
* **Files Checked:** `storage.js`, `app.js`, `cli.js`.
* **Evaluation:** Searching for file interaction terms (`writeFile`, `JSON`) led directly to `storage.js`. Feature implementation relies on identifying which module handles each stage of data flow.

### 2. Feature Location & Affected Components
To add a **"Task Export to CSV"** feature, changes are divided across three key files:
1. **`cli.js` (User Interface):** Register a new command (e.g., `node cli.js export <filename>`) using `commander`.
2. **`app.js` (Business Logic):** Add a method (`exportTasksToCSV(filePath)`) to `TaskManager` to direct export processing.
3. **`storage.js` (Data Handling & File I/O):** Add CSV formatting and file-writing logic using Node's `fs` module.

### 3. Step-by-Step Implementation Plan
1. **Step 1:** Create a helper method in `storage.js` to convert JSON tasks into CSV format and save them using `fs.writeFileSync`.
2. **Step 2:** Add an `exportTasks` method to `TaskManager` in `app.js`.
3. **Step 3:** Register the `export` command in `cli.js`.
4. **Step 4:** Add unit tests in `tests/taskStorage.test.js` to test CSV output.

---

  
  
## Exercise Part 3: Understanding Domain Models & Business Concepts

### 1. Core Domain Entities & Glossary
* **Task:** The central entity representing a single work item (`id`, `title`, `description`, `status`, `priority`, `dueDate`, `tags`, `timestamps`).
* **TaskStatus:** Registry of workflow stages (`TODO`, `IN_PROGRESS`, `REVIEW`, `DONE`). Uses strings (`'todo'`, `'in_progress'`) for human readability.
* **TaskPriority:** Registry of urgency levels (`LOW: 1`, `MEDIUM: 2`, `HIGH: 3`, `URGENT: 4`). Uses numbers so tasks can be sorted numerically by urgency.
* **Audit Timestamps:**
  * `createdAt`: Set once when created.
  * `updatedAt`: Refreshed on every modification.
  * `dueDate`: Optional target deadline.
  * `completedAt`: Set exclusively when marked `DONE`.

### 2. Domain Model Relationship Diagram

┌─────────────────────────────────┐
             │            TASK                 │
             │  id, title, description, tags   │
             └───────────────┬─────────────────┘
                             │
   ┌─────────────────────────┼─────────────────────────┐
   │                         │                         │
   ▼                         ▼                         ▼
┌──────────────┐         ┌──────────────┐         ┌──────────────┐
│   WORKFLOW   │         │  IMPORTANCE  │         │     TIME     │
│  TaskStatus  │         │ TaskPriority │         │              │
│ todo         │         │ 1 LOW        │         │ createdAt    │
│ in_progress  │         │ 2 MEDIUM     │         │ updatedAt    │
│ review       │         │ 3 HIGH       │         │ dueDate      │
│ done         │         │ 4 URGENT     │         │ completedAt  │
└──────────────┘         └──────────────┘         └──────────────┘

### 3. Answers to Domain Model Assessment Questions

1. **Which task shows up in `node cli.js list -o` (Overdue)?**
   * Only the first task (due yesterday, `IN_PROGRESS`) shows up. Overdue status relies strictly on: `dueDate < now` AND `status !== DONE`. Priority does not affect whether a task is overdue.
2. **What happens when a task is completed early? Is it overdue after completion?**
   * No, a completed task is never overdue (`status === DONE` overrides overdue calculations).
   * Marking `DONE` calls `markAsDone()`, updating both `updatedAt` and `completedAt`. Changing status to `IN_PROGRESS` only updates `status` and `updatedAt` (leaving `completedAt` as `null`).
3. **Why use numbers for priority and strings for status?**
   * **Priority (Numbers 1-4):** Allows mathematical comparison and sorting (e.g., `a.priority > b.priority` to show urgent tasks first).
   * **Status (Strings):** Makes terminal outputs and JSON files easily human-readable without requiring a lookup key.
4. **When priority changes from MEDIUM to URGENT on a task in review:**
   * **Domain state changed:** `priority` (2 -> 4) and `updatedAt` timestamp.
   * **Unchanged:** `status` remains `REVIEW`, `createdAt`, `dueDate`, and `completedAt` remain untouched. Workflow and urgency are independent dimensions.
5. **Impact of adding a "snoozed" status:**
   * **`isOverdue()` rule:** Needs evaluation (should snoozed tasks trigger overdue alerts?).
   * **`stats` command:** Needs updating to count/display snoozed items.
   * **CLI & Merge logic:** `cli.js` options and `task_list_merge.js` conflicts need rules for handling snoozed tasks.

---

## Exercise Part 4: Practical Application

### 1. Planning: Overdue Auto-Abandonment Business Rule
**Scenario:** *"Tasks overdue for more than 7 days should automatically be marked as 'abandoned', unless they are marked as high/urgent priority."*

### Files to Modify
1. **`models.js`:**
   * Add `ABANDONED: 'abandoned'` to the `TaskStatus` registry.
   * Add a business rule method to the `Task` class (e.g., `isEligibleForAbandonment()`) that checks if `isOverdue()` is true by $> 7$ days AND `priority < TaskPriority.HIGH`.
2. **`app.js`:**
   * Add a service/manager method `checkAndAbandonTasks()` to iterate over active tasks and update their status using the model rule.
3. **`cli.js`:**
   * Add or hook into an automated entry point (e.g., a `clean` command or auto-check on `list`) to trigger the abandon logic.
4. **`tests/`:**
   * Add unit tests in `task.test.js` to verify tasks $\le 7$ days overdue or high-priority tasks are *not* marked as abandoned.

### Questions for the Team Before Implementing
* **Priority Threshold:** Does "high priority" strictly mean `TaskPriority.HIGH` (3), or does it also protect `TaskPriority.URGENT` (4)?
* **Timestamp Behavior:** Should abandoning a task record a specific `abandonedAt` date, or just update `updatedAt`?
* **Execution Trigger:** Should this rule run automatically every time a user runs `node cli.js list`, or should it be an explicit maintenance command like `node cli.js cleanup`?

---

### 2. Reflection
* **How AI Prompts Helped:** The structured prompts made it easy to trace how data flows from user commands down to file I/O, helping separate interface code (`cli.js`) from pure domain logic (`models.js`).
* **Remaining Codebase Questions:** How tasks will be synced or merged across external instances using `task_list_merge.js`.
* **Next Steps for Growth:** Build unit tests for edge cases (e.g., leap years or timezone shifts when calculating the 7-day overdue difference) and implement the CSV export feature end-to-end.



---

# Exercise Series 2: Codebase Exploration Challenge

## Exercise Part 1: Understanding Task Creation & Status Updates

### 1. Main Components Involved
* **`cli.js` (CLI Interface):** Uses `commander` to parse command-line arguments (commands like `create` and `status`). Maps CLI inputs to `TaskManager` calls.
* **`app.js` (Application Layer / Orchestrator):** Contains `TaskManager`. Acts as the service layer that coordinates operations between domain models and persistent storage.
* **`models.js` (Domain Model Layer):** Houses the `Task` class, status constants (`TaskStatus`), and priority levels (`TaskPriority`). Contains business methods like `markAsDone()` and `update()`.
* **`storage.js` (Persistence / Repository Layer):** Manages reading and writing task data to disk (`tasks.json`). Re-instantiates plain JSON items back into live `Task` instances.

---

### 2. Detailed Execution Flows

#### Flow A: Creating a Task (`node cli.js create "Buy groceries"`)
1. **Command Parsing:** `cli.js` receives the user input, parses the title string and optional flags (e.g., priority, tags), and invokes `taskManager.createTask(...)`.
2. **Domain Object Instantiation:** `TaskManager` instantiates a new `Task` object (`models.js`), which generates a unique UUID, sets initial timestamps (`createdAt`, `updatedAt`), and assigns default status/priority.
3. **Persistence:** `TaskManager` passes the new `Task` instance to `TaskStorage.addTask(...)` (`storage.js`).
4. **Disk I/O:** `storage.js` appends the object to the in-memory array and serializes the entire array back to `tasks.json` via Node's `fs` module.

#### Flow B: Updating Task Status (`node cli.js status <task_id> done`)
1. **Command Parsing:** `cli.js` receives the task ID and new status target (`done`), then invokes `taskManager.updateTaskStatus(taskId, status)`.
2. **Rehydration:** `app.js` calls `storage.getTaskById(taskId)`. `storage.js` loads the plain JSON data from `tasks.json` and hydrates it back into a true `Task` class instance.
3. **Domain Logic Execution:** `TaskManager` invokes `task.markAsDone()` directly on the `Task` domain instance. This updates `status` to `'done'`, updates `updatedAt` to `now()`, and sets `completedAt` to `now()`.
4. **Re-serialization:** `storage.js` saves the mutated task array back into `tasks.json`.

---

### 3. Key Design Patterns & Architecture Insights
* **Rehydration Pattern (JSON <-> Domain Model):** The JSON file on disk stores raw data attributes, not class methods. When loaded into memory, plain JSON objects are passed back through `new Task(...)` so domain methods (`markAsDone()`, `update()`) become available again.
* **Layered Architecture:** Clear separation of concerns—UI Layer (`cli.js`) -> Service Layer (`app.js`) -> Domain Layer (`models.js`) -> Data Access Layer (`storage.js`).
* **Audit Timestamping:** `createdAt` is immutable; `updatedAt` changes on any mutation; `completedAt` is controlled strictly by status transitions to `DONE`.

---

### 4. Code Change Validation Requirements
To validate my understanding of execution flow and domain state, I will implement three small validation requirements:

1. **Task Creation Feedback:** Upon creating a task, print its generated `id`, `status`, `createdAt`, and `updatedAt` directly to the terminal output.
2. **Status Transition Verification:** When updating a task to `done`, log both the previous state and new state to confirm `completedAt` and `updatedAt` were correctly modified.
3. **Disk vs. Memory Inspection:** Add a debug logger during save operations in `storage.js` to print the raw JSON payload being written to `tasks.json`.

## Exercise Part 2: Deepening Understanding of Task Prioritization

### 1. Initial Understanding vs. Discoveries
* **Initial Assumption:** Priority is just a simple number set by the user at task creation.
* **Discovered Reality:** Priority handling involves a multi-stage normalization pipeline. Raw CLI input strings (`"high"`, `"HIGH"`, `"3"`) are sanitized and validated against `TaskPriority` before being attached to the `Task` domain model as numbers (`1` to `4`).

---

### 2. Answers to Guided Investigation Questions

#### Q1 & Q2: Transformation & Validation of Priority Inputs
* **First Transformation Point:** Input normalization occurs in the parsing layer (`task_priority.js` / `task_parser.js`).
* **Handling Varied Inputs:** Strings like `"high"`, `"HIGH"`, and `"3"` are lowercased and matched against `TaskPriority` mappings or parsed as integers.
* **Invalid Inputs (`"ultra"`, `99`):** Invalid inputs fail validation against known keys/range. The system gracefully falls back to default `TaskPriority.MEDIUM` (`2`) or throws a validation error before creating/updating the task.

#### Q3 & Q4: Priority Data Flow & Transformations
* **Step 1 - CLI Layer (`cli.js`):** Captures raw string flag (e.g., `--priority high`).
* **Step 2 - App/Parser Layer (`app.js` / `task_priority.js`):** Normalizes `"high"` -> `3` (`TaskPriority.HIGH`).
* **Step 3 - Domain Layer (`models.js`):** Instantiates `Task` with numeric `priority = 3`.
* **Step 4 - Persistence Layer (`storage.js`):** Saves `{"priority": 3}` as plain JSON.
* **Step 5 - Sorting/Listing (`app.js`):** Sorts tasks using numerical comparison (`b.priority - a.priority`).

#### Q5: Handling Priority Ties in Sorting
* **Primary Rule:** Tasks sharing the same priority level rely on JavaScript's stable array sorting (`.sort()`), which preserves the original insertion order of elements with equal values.
* **Secondary Tie-Breaker:** If a strict order is needed beyond insertion sequence, the app can evaluate a secondary field like `createdAt` timestamps.

---

### 3. Architecture Reflection: Input Normalization Strategy
* **Conclusion:** Input should be normalized at the **CLI/Boundary Layer** as early as possible. Converting raw user strings into strict domain types (`TaskPriority` numbers) before passing them to `TaskManager` ensures the core business logic operates purely on valid data, eliminating duplicate validation logic.

# Exercise Part 3: Mapping Data Flow and State Management

## 1. Data Flow Diagram

[ Terminal Input ] ──> `node cli.js status <taskId> done`
                              │
                              ▼
                         [ cli.js ]
              (Parses `taskId` and status `'done'`)
                              │
                              ▼
                         [ app.js ] (TaskManager)
               (Calls `storage.getTask(taskId)`)
                              │
                              ▼
                        [ models.js ] (Task)
              (Executes `task.markAsDone()`)
                              │
                              ▼
                       [ storage.js ] (TaskStorage)
              (Executes `storage.save()`)
                              │
                              ▼
                      [ tasks.json ]
            (Synchronously overwritten to disk)

## 2. Transient vs. Persistent State Changes

### Transient State (In-Memory during Command Execution)
* **Entry Point (`cli.js`):** The `taskId` string and target status `'done'` exist as temporary command-line argument variables.
* **Lookup & Instantiation (`storage.js` / `app.js`):** `TaskManager` requests the task via `this.storage.getTask(taskId)`, retrieving the live JavaScript `Task` class instance stored in the in-memory map `this.tasks`.
* **Domain Mutation (`models.js`):** Calling `task.markAsDone()` mutates properties in local memory:
  * `this.status` transforms from `'todo'` (or `'in_progress'`) to `'done'`.
  * `this.completedAt` transforms from `null` to a new `Date` timestamp.
  * `this.updatedAt` is updated to match `completedAt`.

### Persistent State (Durable Storage in `tasks.json`)
* State becomes durable **only** when `this.storage.save()` runs in `storage.js`.
* The entire in-memory `this.tasks` map is serialized via `JSON.stringify` and synchronously written to disk using `fs.writeFileSync`.

---

## 3. Key Code Snippets

### CLI Parsing (`cli.js`)
```javascript
program
  .command('status <task_id> <status>')
  .description('Update task status')
  .action((taskId, status) => {
    if (taskManager.updateTaskStatus(taskId, status)) {
      console.log(`Updated task status to ${status}`);
    } else {
      console.log('Failed to update task status. Task not found.');
    }
  });

  Domain Logic & State Mutation (app.js & models.js)

  // app.js - TaskManager
updateTaskStatus(taskId, newStatusValue) {
  if (newStatusValue === TaskStatus.DONE) {
    const task = this.storage.getTask(taskId);
    if (task) {
      task.markAsDone();
      this.storage.save();
      return true;
    }
    return false;
  }
  return this.storage.updateTask(taskId, { status: newStatusValue });
}

// models.js - Task
markAsDone() {
  this.status = TaskStatus.DONE;
  this.completedAt = new Date();
  this.updatedAt = this.completedAt;
}

Disk Persistence (storage.js)

save() {
  try {
    const tasksArray = Object.values(this.tasks);
    fs.writeFileSync(this.storagePath, JSON.stringify(tasksArray, null, 2));
  } catch (error) {
    console.error(`Error saving tasks: ${error.message}`);
  }
}

## 4. Potential Points of Failure

1. **Unmatched Task ID:** Passing an invalid or truncated ID causes `storage.getTask(taskId)` to return `undefined`. `updateTaskStatus()` returns `false`, and no changes occur.
2. **Silent Save Failure:** `storage.js` catches filesystem write errors inside `save()` using `try/catch` and logs to the console without re-throwing or returning a success/failure boolean. As a result, `updateTaskStatus()` returns `true` to `cli.js`, giving a false indication that the task was saved when disk writing failed.
3. **Synchronous I/O Blocking:** File operations (`fs.readFileSync` and `fs.writeFileSync`) run synchronously on Node's main event loop. If the filesystem is slow or locked, execution halts until the operation completes.
4. **Data Corruption on Malformed Input:** If `tasks.json` becomes corrupted, `load()` fails to parse JSON, leaving `this.tasks` empty (`{}`). A subsequent call to `save()` will overwrite `tasks.json` and wipe existing data.

---

## 5. Architectural Tradeoffs & Reflections

* **Current Architecture (*In-Memory Hash Map with File Flush*):** Fast in-memory access during process execution, but blurs boundaries by requiring explicit calls to `this.storage.save()` after domain object mutations.
* **Alternative Model (*Explicit Read → Transform → Write Pipeline*):** For a short-lived CLI execution, a stateless pipeline that loads the file, applies a functional transformation, and immediately writes back to disk would enforce clearer layer boundaries and reduce state desynchronization risks.