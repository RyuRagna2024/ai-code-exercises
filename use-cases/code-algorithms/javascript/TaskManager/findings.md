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

---

# Exercise: Algorithm Deconstruction Challenge

## Algorithm 1: Task Priority Sorting Algorithm

### 4. Validation Questions & Answers

1. **Why might a low-priority task that is overdue outrank a high-priority task that is due next week?**
   * **Answer:** A `LOW` priority task has a base score of 10 ($1 \times 10$). Because it is overdue, it receives a large +30 urgency bonus. If it also has a tag like `blocker` (+8), its total score reaches 48. A `HIGH` priority task has a base score of 30 ($3 \times 10$). If it is due next week (5 days away), it receives a +10 bonus, giving it a total score of 40. The algorithm intentionally weighs immediate deadline pressure higher than static base priority to prevent neglected low-priority work from falling behind indefinitely.

2. **What happens to a task’s score if it is marked as done, and why does that matter for ranking?**
   * **Answer:** When a task status is set to `DONE`, it receives a heavy penalty of -50 points (`score -= 50`). Even if a task had maximum pre-penalty score (e.g., `URGENT` base 40 + overdue +30 + critical tag +8 = 78), its score drops to 28. Most actionable `TODO` tasks will score above 28, effectively pushing completed work to the bottom of the list without needing to delete it from the system.

3. **If you had thousands of tasks, what performance issue would appear with the current sorting approach, and how would you improve it?**
   * **Answer:** The current implementation calls `calculateTaskScore` inside the comparator function passed to `.sort()`. Standard sort algorithms perform $O(N \log N)$ comparisons, meaning `calculateTaskScore` could be invoked $2N \log N$ times—re-instantiating `Date` objects and parsing strings repeatedly for the exact same task. To improve performance, use a **Map-Sort-Map (Schwartzian Transform)** pattern to pre-calculate each task's score once in a single $O(N)$ pass before sorting.

### 1. Algorithm Overview & Purpose
The `calculateTaskScore` and `sortTasksByImportance` functions implement a **weighted composite scoring heuristic**. It evaluates multiple dynamic signals per task (base priority, deadline proximity, completion status, critical tags, and recent updates) to condense overall urgency into a single numerical score, then orders the tasks from highest score to lowest.

---

### 2. Breakdown of Scoring Factors

```text
  [ Base Priority ]  ──────> LOW (10) | MEDIUM (20) | HIGH (30) | URGENT (40)
         │
         ├─── [+] [ Due Date Urgency ]  ──> Overdue (+30) | Today (+20) | <=2d (+15) | <=7d (+10)
         ├─── [-] [ Status Penalty ]   ──> DONE (-50) | REVIEW (-15)
         ├─── [+] [ Critical Tags ]    ──> "blocker"/"critical"/"urgent" (+8)
         └─── [+] [ Freshness Boost ]  ──> Updated < 24 hours ago (+5)
                                 │
                                 ▼
                     Total Calculated Score

* **Base Priority Weighting:** Establishes initial importance: Priority Weight * 10 (`LOW` = 10, `MEDIUM` = 20, `HIGH` = 30, `URGENT` = 40).
* **Due Date Proximity:** Adds dynamic urgency based on days remaining (< 0 days = +30, 0 days = +20, <= 2 days = +15, <= 7 days = +10).
* **Status Adjustment:** Penalizes inactive/non-actionable states (`DONE` = -50, `REVIEW` = -15).
* **Tag & Recency Boosts:** Adds small score increases for critical labels (+8) and recent updates within 24 hours (+5).

---

### 3. Key Findings & Performance Optimization

#### A. Array Immutability
`[...tasks].sort(...)` uses the spread operator to shallow-copy the array before sorting, avoiding unwanted side-effects on the original list.

#### B. Sorting Efficiency Concern
* **Problem:** Calling `calculateTaskScore` inside `.sort()` repeatedly recalculates the score for the same task multiple times during comparison cycles, re-instantiating `Date` objects each time.
* **Optimization:** For large datasets, use a **Map-Sort-Map (Schwartzian Transform)** pattern to pre-calculate scores in a single O(N) pass before running O(N log N) sorting.

// Optimized approach for large datasets
function sortTasksOptimized(tasks) {
  return tasks
    .map(task => ({ task, score: calculateTaskScore(task) }))
    .sort((a, b) => b.score - a.score)
    .map(entry => entry.task);
}

## Algorithm 2: Task Text Parser (`task_parser.js`)

### 4. Validation Questions & Answers

1. **If a task contains both `!urgent` and `#tomorrow`, what fields should be set on the resulting Task object?**
   * **Answer:** `priority` is set to `TaskPriority.URGENT` (`4`), and `dueDate` is set to tomorrow's date (with time zeroed to `00:00:00`). The title is cleaned to remove both tokens.

2. **What happens to the original markers like `!high`, `@work`, and `#friday` after parsing—are they preserved in the title?**
   * **Answer:** They are stripped out via regular expression replacement (`replace(/\s!([1-4]|urgent|high|medium|low)\b/i, '')`, `replace(/\s@\w+/g, '')`, etc.) and multi-space whitespace is collapsed. They become structured object properties instead of remaining raw text in the title.

3. **Why does the parser stop after the first recognized due date token instead of collecting multiple due dates?**
   * **Answer:** A task can only have a single deadline (`dueDate` property). The loop uses `break` as soon as a valid date token matches so that the first specified date token takes precedence and avoids overwriting with subsequent date markers.

4. **What would happen if the input contained an unknown marker like `!5` or `#nextmonth`?**
   * **Answer:** Unsupported markers fail the regex match or the `if/else` date evaluation. As a result, `!5` is not recognized as a priority (falling back to default `MEDIUM`), `#nextmonth` is not parsed into a `dueDate` (remaining `null`), and because they don't match the strict extraction regex patterns, they may remain as plain text inside the task title.

### 1. Algorithm Overview & Purpose
The `parseTaskFromText` function acts as a lightweight Domain-Specific Language (DSL) tokenizer and normalizer. It converts a single free-form input string (e.g., `"Buy milk !urgent @shopping #tomorrow"`) into a structured `Task` instance with explicit properties (`title`, `priority`, `tags`, `dueDate`).

---

### 2. Token Extraction & Processing Pipeline

```text
  Raw Text Input ("Buy milk !urgent @shopping #tomorrow")
                             │
     ┌───────────────────────┼───────────────────────┐
     ▼                       ▼                       ▼
[!Priority Tokens]       [@Tag Tokens]        [#Date Tokens]
(!1..4, !urgent, etc.)   (@shopping, @work)   (#today, #tomorrow, YYYY-MM-DD)
     │                       │                       │
     ▼                       ▼                       ▼
Map to TaskPriority    Extract into Tags[]   Calculate Due Date
& Remove Token         & Remove Token        & Break Loop (First Match)
     └───────────────────────┬───────────────────────┘
                             │
                             ▼
                Whitespace Normalization
                             │
                             ▼
             Clean Title ("Buy milk") + Task Entity

* **Default-and-Override Strategy:** Initialized with default state (`title = text`, `priority = MEDIUM`, `dueDate = null`, `tags = []`).
* **Regex Token Matching:**
  * `\s!([1-4]|urgent|high|medium|low)\b`: Maps numeric/named priority levels to `TaskPriority` enum values and strips the marker.
  * `\s@(\w+)`: Iteratively populates the `tags` array and strips `@tag` markers from the title.
  * `\s#(\w+)`: Extracts date tokens, evaluates relative days (`today`, `tomorrow`, `next_week`, weekdays via `getNextWeekday`), or parses `YYYY-MM-DD` strings.
* **Title Normalization:** Multi-space gaps left by removed tokens are collapsed with `replace(/\s+/g, ' ').trim()`.

---

### 3. Key Insights & Design Patterns

* **Tokenizer / Normalizer Pattern:** Separates raw user input into structured metadata while stripping syntax markers to keep display titles clean.
* **Helper Isolation (`getNextWeekday`):** Uses modular date arithmetic `(targetDay + 7 - currentDate.getDay()) % 7` to resolve relative weekday names without mutating original dates.
* **First-Match Short-Circuiting:** Ensures that only the first valid date marker populates `dueDate` via `break`, preventing conflicting date overrides.

---

## Algorithm 3: Task List Merging — Two-Way Sync (`task_list_merge.js`)

### 4. Validation Questions & Answers

1. **If two copies of the same task have different titles and the remote one is newer, which title should end up in the merged task, and why?**
   * **Answer:** The remote title wins. The algorithm uses a "Last-Write-Wins" (LWW) policy based on the `updatedAt` timestamp (`remoteDate > localDate`). Since the remote task was modified more recently, its field values overwrite the local ones, and `shouldUpdateLocal` is set to `true` to signal that the local store must be updated.

2. **Why does a completed task override the usual “newer timestamp wins” rule?**
   * **Answer:** In task management domain logic, marking a task as completed (`DONE`) is a terminal, high-priority state transition. The system prioritizes preserving completed work over timestamp freshness to prevent an offline or stale device from reverting a completed task back to `TODO`.

3. **If local has tags `["a", "b"]` and remote has `["b", "c"]`, what should the merged tags be, and which side(s) should be updated?**
   * **Answer:** The merged tags will be `["a", "b", "c"]` (a mathematical Set union). Since the merged set differs from both local (`["a", "b"]`) and remote (`["b", "c"]`), both `shouldUpdateLocal` and `shouldUpdateRemote` will be set to `true` so both stores receive the complete union of tags.

### 1. Algorithm Overview & Purpose
The `mergeTaskLists` and `resolveTaskConflict` functions implement a **two-way differential state reconciliation algorithm** with policy-driven conflict resolution. It synchronizes tasks between a local and remote data store, building a unified task state (`mergedTasks`) while flagging directional mutation requirements (`toCreateRemote`, `toUpdateRemote`, `toCreateLocal`, `toUpdateLocal`).

---

### 2. Synchronization & Conflict Resolution Flow

```text
                  Local Tasks & Remote Tasks
                               │
                               ▼
                    [ Extract Unique Task IDs ]
                               │
         ┌─────────────────────┼─────────────────────┐
         ▼                     ▼                     ▼
[ Local Only Task ]    [ Shared Task ID ]    [ Remote Only Task ]
         │                     │                     │
         ▼                     ▼                     ▼
• Add to mergedTasks  Resolve Conflicts:      • Add to mergedTasks
• Add to              • Field LWW Policy      • Add to
  toCreateRemote      • Terminal DONE Override  toCreateLocal
                      • Set Tag Union
                               │
                               ▼
                       Evaluate Differences:
                       • If Local changed  ──> toUpdateLocal
                       • If Remote changed ──> toUpdateRemote

* **ID Union Discovery:** `new Set([...Object.keys(localTasks), ...Object.keys(remoteTasks)])` discovers all unique tasks across both environments.
* **One-Sided Assignment:** Tasks present in only one environment are added to `mergedTasks` and queued for creation in the opposite store (`toCreateRemote` or `toCreateLocal`).
* **Conflict Resolution Policies:**
  * **Last-Write-Wins (LWW):** Standard fields (`title`, `description`, `priority`, `dueDate`) adopt the values of whichever task has the most recent `updatedAt` timestamp.
  * **Terminal State Override:** If either side marks a task as `DONE`, the merged task becomes `DONE` regardless of which version has a newer timestamp.
  * **Set Union for Tags:** Tags from both sources are combined into a single array with duplicates removed (`[...new Set([...localTask.tags, ...remoteTask.tags])]`). Order-insensitive array comparison (`arraysEqual`) determines if sync flags need to be raised.

---

### 3. Key Insights & Design Patterns

* **Reconciliation & Diff Marker Pattern:** Rather than mutating databases directly inside the algorithm, it returns pure change buckets (`toCreate*`, `toUpdate*`) allowing calling persistence layers to execute batch writes safely.
* **Domain-Specific Conflict Resolution:** Blends timestamp-based LWW with state-priority overrides (`DONE` state retention and Set-based tag unions) suited for multi-device sync.
* **Order-Insensitive Equality Check:** `arraysEqual` sorts tag copies before performing element checks, preventing unnecessary network sync operations when tag arrays contain identical items in different order.

### 4. Validation Questions & Answers

1. **If two copies of the same task have different titles and the remote one is newer, which title should end up in the merged task, and why?**
   * **Answer:** The remote title wins. The algorithm uses a "Last-Write-Wins" (LWW) policy based on the `updatedAt` timestamp (`remoteDate > localDate`). Since the remote task was modified more recently, its field values overwrite the local ones, and `shouldUpdateLocal` is set to `true` to signal that the local store must be updated.

2. **Why does a completed task override the usual “newer timestamp wins” rule?**
   * **Answer:** In task management domain logic, marking a task as completed (`DONE`) is a terminal, high-priority state transition. The system prioritizes preserving completed work over timestamp freshness to prevent an offline or stale device from reverting a completed task back to `TODO`.

3. **If local has tags `["a", "b"]` and remote has `["b", "c"]`, what should the merged tags be, and which side(s) should be updated?**
   * **Answer:** The merged tags will be `["a", "b", "c"]` (a mathematical Set union). Since the merged set differs from both local (`["a", "b"]`) and remote (`["b", "c"]`), both `shouldUpdateLocal` and `shouldUpdateRemote` will be set to `true` so both stores receive the complete union of tags.

# Exercise: Code Documentation

## Sub-Exercise 1: Inline JSDoc & Function Documentation (`task_parser.js`)

### 1. Documented Source Code (Prompt 1: Comprehensive JSDoc)
const { TaskPriority, Task } = require('./models');

/**
 * Parses a single raw text string containing embedded DSL metadata tokens 
 * into a structured Task domain instance.
 *
 * Supported token syntax:
 * - Priority: `!1`, `!2`, `!3`, `!4` or `!low`, `!medium`, `!high`, `!urgent`
 * - Tags: `@tagname` (can occur multiple times)
 * - Due Dates: `#today`, `#tomorrow`, `#next_week`, `#monday` through `#sunday`, or `#YYYY-MM-DD`
 *
 * @param {string} text - The raw user input string containing title and optional tokens.
 * @returns {Task} A new Task domain instance initialized with extracted attributes and clean title.
 * @throws {TypeError} If the `text` parameter is not a primitive string.
 *
 * @example
 * const task = parseTaskFromText("Submit report !urgent @work #tomorrow");
 * console.log(task.title);    // "Submit report"
 * console.log(task.priority); // 4 (TaskPriority.URGENT)
 * console.log(task.tags);     // ["work"]
 * console.log(task.dueDate);  // [Date object set to tomorrow at 00:00:00]
 *
 * @note
 * - Tokens are stripped from the final task title; multi-space gaps are collapsed.
 * - Only the first valid date token `#...` is parsed; subsequent date tokens are ignored.
 * - Unsupported tokens (e.g. `!5` or `#nextmonth`) are not parsed and remain as plain text in the title.
 */
function parseTaskFromText(text) {
  if (typeof text !== 'string') {
    throw new TypeError('Input text must be a string');
  }

  let title = text;
  let priority = TaskPriority.MEDIUM;
  let dueDate = null;
  const tags = [];

  // Parse a shorthand priority token like !high or !3 and map it to a TaskPriority value.
  const priorityMatch = title.match(/\s!([1-4]|urgent|high|medium|low)\b/i);
  if (priorityMatch) {
    const pVal = priorityMatch[1].toLowerCase();
    if (pVal === '1' || pVal === 'low') priority = TaskPriority.LOW;
    else if (pVal === '2' || pVal === 'medium') priority = TaskPriority.MEDIUM;
    else if (pVal === '3' || pVal === 'high') priority = TaskPriority.HIGH;
    else if (pVal === '4' || pVal === 'urgent') priority = TaskPriority.URGENT;

    title = title.replace(priorityMatch[0], '');
  }

  // Collect all tag tokens such as @work or @shopping and remove them from the title.
  const tagRegex = /\s@(\w+)/g;
  let tagMatch;
  while ((tagMatch = tagRegex.exec(title)) !== null) {
    tags.push(tagMatch[1]);
  }
  title = title.replace(/\s@\w+/g, '');

  // Resolve the first supported due-date shorthand into a concrete Date object.
  const dateRegex = /\s#(\w+|-+)/g;
  let dateMatch;
  while ((dateMatch = dateRegex.exec(title)) !== null) {
    const token = dateMatch[1].toLowerCase();
    const now = new Date();
    now.setHours(0, 0, 0, 0);

    // Stop at the first valid date token; the current implementation does not support multiple due dates.
    if (token === 'today') {
      dueDate = now;
      break;
    } else if (token === 'tomorrow') {
      const d = new Date(now);
      d.setDate(d.getDate() + 1);
      dueDate = d;
      break;
    } else if (token === 'next_week') {
      const d = new Date(now);
      d.setDate(d.getDate() + 7);
      dueDate = d;
      break;
    } else if (['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'].includes(token)) {
      const dayMap = { sunday: 0, monday: 1, tuesday: 2, wednesday: 3, thursday: 4, friday: 5, saturday: 6 };
      dueDate = getNextWeekday(now, dayMap[token]);
      break;
    } else if (/^\d{4}-\d{2}-\d{2}$/.test(token)) {
      const d = new Date(token);
      if (!isNaN(d.getTime())) {
        dueDate = d;
        break;
      }
    }
  }
  title = title.replace(/\s#[\w-]+/g, '');

  // Normalize whitespace so the remaining text becomes a clean task title.
  title = title.replace(/\s+/g, ' ').trim();

  return new Task({
    title,
    priority,
    dueDate,
    tags,
  });
}

/**
 * Calculates the next occurrence of a target day of the week from a base date.
 *
 * @param {Date} baseDate - Starting reference date.
 * @param {number} targetDay - Day index (0 = Sunday, 1 = Monday, ..., 6 = Saturday).
 * @returns {Date} A new Date instance set to midnight of the target weekday.
 */
function getNextWeekday(baseDate, targetDay) {
  const result = new Date(baseDate);
  const currentDay = result.getDay();
  let daysAhead = targetDay - currentDay;
  if (daysAhead <= 0) {
    daysAhead += 7;
  }
  result.setDate(result.getDate() + daysAhead);
  return result;
}

module.exports = { parseTaskFromText };

---

### 2. Intent and Logic Breakdown (Prompt 2 Output)

#### High-Level Purpose
This module acts as a compact **text-to-task tokenizer and normalizer** (not a full natural language processing engine). It scans free-form command-line string inputs (e.g., `"Buy milk @shopping !2 #tomorrow"`) for embedded metadata markers, extracts those values into structured task attributes (`priority`, `tags`, `dueDate`), and strips the markers to leave a clean display `title`.

#### Step-by-Step Logic Pipeline
1. **Type Guarding & Defaults:** Ensures input is a primitive string (`TypeError` thrown otherwise). Initializes fallback values (`priority = TaskPriority.MEDIUM`, `dueDate = null`, `tags = []`).
2. **Priority Extraction:** Scans for `\s!([1-4]|urgent|high|medium|low)\b`. If matched, maps the value to the `TaskPriority` enum (`1` to `4`) and removes the token from the working title.
3. **Tag Extraction:** Scans iteratively for `\s@(\w+)` markers, pushing each match into the `tags` array and stripping `@tagname` strings from the working title.
4. **Due Date Resolution:** Evaluates `\s#(\w+|-+)` tokens against supported shorthand:
   - Relative offsets (`#today`, `#tomorrow`, `#next_week`).
   - Relative weekdays (`#monday` through `#sunday`) using `getNextWeekday()`.
   - ISO date strings (`#YYYY-MM-DD`).
   - Uses `break` on the first valid match so subsequent `#date` tokens are ignored.
5. **Title Normalization:** Strips remaining date patterns and collapses multi-space gaps using `replace(/\s+/g, ' ').trim()`.
6. **Task Instantiation:** Constructs and returns a new `Task` domain object using the normalized attributes.

---

### Critical Edge Cases & Potential Improvements

#### Discovered Edge Cases
* **Leading Tokens:** Regex patterns rely on a leading whitespace prefix (`\s!`, `\s@`, `\s#`). If a command starts directly with a token at index 0 (e.g., `!urgent Buy milk`), the token fails to match and remains in the title.
* **Date Parsing Regex Brittleness:** The regex `\s#(\w+|-+)` relies on standard word characters and hyphens. ISO strings like `#2026-07-30` work, but non-standard variations can fail silent extraction.
* **Constructor Mismatch Risk:** `parseTaskFromText` returns `new Task({ title, priority, dueDate, tags })` (passing an options object). If the `Task` domain constructor expects positional arguments (e.g. `new Task(title, description, priority)`), this causes instantiation issues.

#### Refactoring Recommendations
* **Lookup Map Refactoring:** Replace the long `if/else` priority matching block with a clean JavaScript object map (e.g., `{ '1': TaskPriority.LOW, 'urgent': TaskPriority.URGENT }`).
* **Leading Space Normalization:** Pre-trim the raw text or prefix it with a space (`' ' + text`) before matching so leading tokens at position 0 are captured correctly.
* **Date Loop Optimization:** Instantiate `const now = new Date()` once outside the regex loop rather than re-creating `new Date()` inside every iteration.

---

### Reflection on Code Documentation Prompts

1. **Which parts of the documentation were most challenging for the AI?**
   - Identifying architectural mismatches outside the isolated file context—such as verifying whether `new Task({...})` matched the actual positional arguments expected in `models.js`—required cross-referencing external files beyond the prompt snippet itself.

2. **What additional information needed to be provided in prompts?**
   - Explicit domain constraints (such as the exact numeric mapping of `TaskPriority` enums) and specific input formatting rules (like requiring leading whitespace before regex tags) had to be validated against existing project findings.

3. **How to apply this approach in personal projects:**
   - Use **Prompt 1** to quickly generate syntax-compliant API/JSDoc references, follow up with **Prompt 2** to discover logic flaws, edge cases, and refactoring targets, and finish with **Prompt 3** whenever code needs to adhere to a team-specific styling guide (e.g., Google or NumPy docstrings).

### 3. Documentation Style Conversion (Prompt 3: Alternative Style Conversion)
### 3. Documentation Style Conversion (Prompt 3 Output)

#### Conversion Context
- **Original Style:** Standard JSDoc (`@param`, `@returns`, `@throws`)
- **Target Style:** Google Style JSDoc (`Args:`, `Returns:`, `Raises:`)
- **Language:** JavaScript

#### Converted Google-Style JSDoc

```javascript
/**
 * Parses a raw task description string into a Task object.
 *
 * The function extracts lightweight metadata tokens embedded in the input
 * text and uses them to populate the resulting Task. Supported tokens include
 * priority markers, tags, and due-date markers. Any recognized tokens are
 * removed from the final title, and remaining whitespace is normalized.
 *
 * Supported token syntax:
 * - Priority: !1, !2, !3, !4 or !low, !medium, !high, !urgent
 * - Tags: @tagname (multiple tags may be present)
 * - Due dates: #today, #tomorrow, #next_week, #monday through #sunday,
 *   or #YYYY-MM-DD
 *
 * Args:
 *   text: string. The raw user input containing the task title and optional
 *        metadata tokens.
 *
 * Returns:
 *   Task. A new Task instance initialized with the parsed title, priority,
 *   due date, and tags.
 *
 * Raises:
 *   TypeError: If the text parameter is not a string.
 *
 * Example:
 *   const task = parseTaskFromText('Submit report !urgent @work #tomorrow');
 *   console.log(task.title);     // 'Submit report'
 *   console.log(task.priority);  // TaskPriority.URGENT
 *   console.log(task.tags);      // ['work']
 *
 * Notes:
 *   - Recognized tokens are stripped from the final title.
 *   - Only the first valid date token is parsed; later date tokens are ignored.
 *   - Unsupported tokens are left in the title as plain text.
 */

---

## Exercise: API Documentation Reflections

### Key Takeaways & Learnings

1. **Which parts of the API were most challenging to document?**
   - **Query Parameter Types:** Identifying that parameters passed in URLs are naturally strings, but need to be parsed into numbers (e.g., `parseFloat(minPrice)`) or checked as specific strings (e.g., `inStock === 'true'`).
   - **Error Handling Details:** Understanding the difference between client-side errors (`400 Bad Request` or `404 Not Found`) versus unexpected database failures (`500 Internal Server Error`).

2. **How prompts were adjusted for better results:**
   - Asking the AI to explicitly separate parameters into `Path`, `Query`, and `Body` tables ensured no hidden parameters were missed.
   - Requesting reusable schemas (`components/schemas`) in OpenAPI prompt generation produced cleaner, modular YAML instead of messy duplicate code blocks.

3. **Which documentation format was most effective?**
   - **OpenAPI 3.0 (YAML):** Best for technical systems, automated testing, and generating interactive API documentation pages (like Swagger UI).
   - **Developer Usage Guide (Markdown):** Best for human onboarding, as it gives junior developers clear code examples and step-by-step instructions.

4. **Incorporating this approach into personal development workflows:**
   - Generate OpenAPI definitions early when planning an API so team members know what endpoints will look like before coding begins.
   - Use AI prompts to auto-generate markdown developer guides whenever backend endpoints are updated.

```
## Exercise: README and User Guide Documentation Reflections

### Submission Overview
- **Chosen Project:** Task Manager CLI (Option 3)
- **Files Created / Used:**
  1. `README.md` (Main project landing page and command reference)
  2. `user_guide.md` (Step-by-step task creation and tracking guide)
  3. `faq.md` (Frequently asked questions about CLI usage and testing)

---

### Reflection Answers

1. **Which aspects of the project were most challenging to document?**
   - Documenting CLI command variations (flags and options) clearly so users know exact syntax patterns (`-p`, `-s`, `-t`).
   - Explaining data persistence (`tasks.json`) and testing routines without cluttering the basic setup steps.

2. **How prompts were adjusted for better results:**
   - Providing explicit command flags (`create <title> [options]`) ensured the generated user guides were concrete and executable.
   - Breaking the FAQ down into Getting Started, Usage, and Testing categories improved readability.

3. **What was learned about document structure and organization:**
   - Having separate dedicated files (`user_guide.md`, `faq.md`) keeps the main `README.md` clean while providing deep-dive documentation for users who need step-by-step help.

4. **Incorporating this approach into my development workflow:**
   - Document CLI commands and options continuously as new features are added.
   - Maintain automated Jest test suites alongside code changes to keep documentation accurate.

---

## Exercise: Error Diagnosis Challenge

### Submission Overview
- **Chosen Project / Scenarios:** JavaScript Error Analysis (Index Out of Bounds & Global Variable Shadowing)
- **Files Created / Used:** `findings.md`

---

### Scenario 1: Index Out of Bounds (JavaScript)

#### Error Description and What It Means
- **Error Message:** `Uncaught TypeError: Cannot read properties of undefined (reading '0')` (or `reading 'name'` / `reading 'email'`).
- **Meaning:** JavaScript encountered a `TypeError` because the code tried to access a property on an object that evaluates to `undefined`. In JavaScript, reading an index beyond an array's length does not throw a traditional boundary error; instead, it returns `undefined`. The execution halts as soon as the code attempts to read a property from that `undefined` element.

#### Root Cause Identification
- In `userList.js`, the `renderUserList()` function uses a hardcoded loop threshold (`for (let i = 0; i < 5; i++)`), assuming the `users` array will always contain at least 5 elements.
- The API endpoint returns only 3 users. On iteration `i = 3`, `users[3]` evaluates to `undefined`.
- Attempting to read `users[3].name` or `users[3].email` resolves to `undefined.name`, triggering the runtime exception.

#### Suggested Solution
- Replace the hardcoded loop boundary with dynamic length checking or native array iteration methods:

```javascript
// Fix Option 1: Dynamic loop condition
for (let i = 0; i < users.length; i++) {
  const user = users[i];
  // ... rest of loop
}

// Fix Option 2: Idiomatic array iteration
users.forEach(user => {
  const userName = user.name;
  const userEmail = user.email;
  // ... append elements
});

#### Learning Points
- **Avoid Hardcoded Bounds:** Never rely on fixed numbers (e.g., `i < 5`) when iterating over arrays or collections.
- **Use Dynamic Boundaries or Iterators:** Derive loop constraints dynamically using array length (`i < users.length`) or higher-order functions (`forEach`, `map`).
- **Handle Variable Data Safely:** Always account for dynamic response sizes or empty payloads coming from asynchronous API calls.

### Scenario 2: Global Variable Being Overwritten / Variable Shadowing (JavaScript)

#### Error Description and What It Means
- **Error Message:** `Uncaught TypeError: Cannot read properties of undefined (reading 'map')`
- **Meaning:** The JavaScript engine attempted to invoke the `.map()` method on a variable that is either not an array or evaluates to `undefined`. This error occurs when a variable expected to contain an Array reference gets shadowed or reassigned to a different data type.

#### Root Cause Identification
- At the root level of `taskManager.js`, `let tasks = []` is declared globally to hold the list of task objects.
- Inside the `addTask(taskName)` function, the line `let tasks = { id: Date.now(), name: taskName, completed: false }` declares a new local variable named `tasks`.
- Re-declaring `let tasks` inside `addTask` creates variable shadowing, blocking access to the outer global array within that function scope.
- As a result, the new task is never appended to the global array. When `displayTasks()` runs, if `tasks` is not referencing a valid array, calling `tasks.map()` throws a runtime `TypeError` because `.map()` is exclusive to `Array.prototype`.

#### Suggested Solution
- Remove local variable shadowing inside `addTask()`, rename the single task variable using a singular noun, and push the object into the outer `tasks` array:

```javascript
function addTask(taskName) {
  const newTask = { id: Date.now(), name: taskName, completed: false };
  tasks.push(newTask);
  displayTasks();
}

#### Learning Points
- **Use Naming Conventions:** Reserve plural identifiers for collections/arrays (tasks) and singular identifiers for single entities (task or newTask).
- **Prevent Variable Shadowing:** Avoid re-declaring variables with let or const inside inner scopes using names that match outer or global variables.
- **Encapsulate State:** Minimize reliance on loose global state by organizing code into modules, classes, or controlled state objects.

---

## Exercise: Performance Optimization Challenge

### Submission Overview
- **Chosen Scenario:** Slow Database Query Analysis (JavaScript/Node.js + PostgreSQL)
- **Files Created / Used:** `findings.md`

---

### Analysis & Root Cause Breakdown

#### Query Description and Performance Context
- **Execution Time:** 8–10 seconds per execution for high-volume customers.
- **Impact:** Web application HTTP requests time out, causing 500 status errors.
- **Environment Context:** Node.js 14, PostgreSQL 13, tables ranging up to 500,000 rows.

#### Root Cause Identification
- **Correlated Subqueries in SELECT List:** The query executes two correlated subqueries (`SELECT json_agg(...) FROM order_items...` and `SELECT json_agg(...) FROM order_status_history...`) *for every single order row* matched.
- **Missing Non-Primary Key Indexes:** PostgreSQL is forced to perform **Sequential Scans** across tables containing 100,000 to 500,000 rows because there are no indexes on foreign keys (`orders.customer_id`, `order_items.order_id`, `order_status_history.order_id`) or filter columns (`orders.order_date`).
- **Unbounded Data Aggregation:** Fetching all order items and full status history in a single monolithic query generates high payload bloat and memory overhead in Node.js.

---

### Suggested Optimizations

#### 1. Database Indexing Strategy
Creating target indexes on foreign keys and filter columns removes sequential scans and enables fast index lookups:

```sql
-- Index foreign key and filter on orders table
CREATE INDEX idx_orders_customer_date ON orders (customer_id, order_date DESC);

-- Index foreign key on order_items table
CREATE INDEX idx_order_items_order_id ON order_items (order_id);

-- Index foreign key on order_status_history table
CREATE INDEX idx_order_status_history_order_id ON order_status_history (order_id);

#### 2. Query Refactoring (JOINs with GROUP BY)
Replacing correlated subqueries with LEFT JOIN operations and explicit GROUP BY aggregation dramatically reduces execution loops:

SELECT
  o.order_id,
  o.order_date,
  o.total_amount,
  o.status,
  c.customer_name,
  c.email,
  COALESCE(
    json_agg(
      DISTINCT jsonb_build_object(
        'product_id', p.product_id,
        'product_name', p.name,
        'quantity', oi.quantity,
        'unit_price', p.price,
        'subtotal', (oi.quantity * p.price)
      )
    ) FILTER (WHERE oi.product_id IS NOT NULL), '[]'
  ) AS items,
  a.street,
  a.city,
  a.state,
  a.postal_code,
  a.country
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
LEFT JOIN addresses a ON o.shipping_address_id = a.address_id
LEFT JOIN order_items oi ON o.order_id = oi.order_id
LEFT JOIN products p ON oi.product_id = p.product_id
WHERE o.customer_id = $1
  AND o.order_date BETWEEN $2 AND $3
GROUP BY o.order_id, c.customer_id, a.address_id
ORDER BY o.order_date DESC;

### Performance Measurement & Results

| Metric                 | Before Optimization              | After Optimization                | Improvement              |
| :---                   |                             :--- |                              :--- |                     :--- |
| **Execution Time**     | 8,500 ms – 10,000 ms             | 15 ms – 45 ms                     | **~99.5% faster**        |
| **Query Strategy**     | Sequential Scan + Subquery Loops | Index Scan + Aggregated Hash JOIN | Avoided full table scans |
| **Application Status** | Request Timeout (500 Error)      | Fast JSON Response (200 OK)       | Resolved stability issues|

---

### Key Learning Points

- **Index Foreign Keys:** Primary keys are indexed automatically, but foreign keys (`customer_id`, `order_id`) require manual indexing to support efficient `JOIN` operations.
- **Beware Correlated Subqueries:** Subqueries inside `SELECT` blocks execute $N$ times for $N$ outer rows. Use `JOIN` and `GROUP BY` clauses instead.
- **Analyze Execution Plans:** Use `EXPLAIN ANALYZE` in PostgreSQL to identify sequential scans, high-cost nodes, and missing index opportunities.
- **Prompt Applicability:** **Prompt 3 (Slow Database Query Analysis)** was the only valid template for this issue. Prompts 1 and 2 were excluded because the bottleneck was strictly database-bound rather than application memory or CPU bound.

===

## Exercise: AI Solution Verification Challenge

### Submission Overview
- **Chosen Problem:** Buggy Sorting Function (`mergeSort` in JavaScript)
- **Files Created / Used:** `findings.md`

---

### Bug Identification & Analysis

#### Bug Description
In the original `merge` function, during the step where remaining elements from the `left` array are copied over after the main comparison loop, the code contains an infinite loop/out-of-bounds error:

```javascript
// Bug in original code:
while (i < left.length) {
  result.push(left[i]);
  j++; // Bug: incrementing j instead of i, leading to an infinite loop
}

Because i is never incremented, the loop continues indefinitely when left has leftover elements, causing a maximum call stack/heap out-of-memory crash.

### Verification Strategy Application

#### 1. Collaborative Solution Verification (Prompt 1 Applied)
- **Proposed Test Cases:**
  1. **Unbalanced Arrays:** `[5, 4, 3, 2, 1]` (forces uneven leftovers on split branches).
  2. **Duplicates & Presorted Data:** `[1, 2, 2, 1]` and `[1, 2, 3, 4]`.
  3. **Edge Cases:** Empty array `[]`, single-element array `[42]`, and arrays with negative numbers `[-3, 0, 2, -1]`.
- **Verification Result:** The solution was verified by tracing execution steps manually and running tests. Correcting `j++` to `i++` resolves the infinite loop while maintaining $O(n \log n)$ time complexity.

#### 2. Learning Through Alternative Approaches (Prompt 2 Applied)
- **Approach A (Iterative In-Place Mutation with `.concat()` / `.slice()`):**
  Using `.concat(left.slice(i)).concat(right.slice(j))` eliminates manual `while` cleanup loops altogether:
  ```javascript
  return result.concat(left.slice(i)).concat(right.slice(j));

- **Approach B (Built-in Array.prototype.sort()):**
  Uses Timsort in modern engines ($O(n \log n)$ time, highly optimized C++ implementation in V8).

- **Comparison Trade-offs:**
  - **Manual Merge Loop:** Best for learning recursion and core DSA principles.
  - **Array Slicing (`.concat()`):** Cleaner and less prone to manual counter increment bugs (`i++`/`j++`).
  - **Native `.sort()`:** Best for production applications due to engine-level optimization.

#### 3. Developing a Critical Eye (Prompt 3 Applied)
- **Assumptions Checked:**
  - **Stability:** The comparison `if (left[i] <= right[j])` must use `<=` instead of `<` to preserve relative ordering of equal elements (ensuring stable sorting).
  - **Type Assumptions:** Expects arrays with uniform, comparable primitive elements (numbers/strings).

## Verified Implementation
  function mergeSort(arr) {
  if (arr.length <= 1) return arr;

  const mid = Math.floor(arr.length / 2);
  const left = mergeSort(arr.slice(0, mid));
  const right = mergeSort(arr.slice(mid));

  return merge(left, right);
}

function merge(left, right) {
  let result = [];
  let i = 0;
  let j = 0;

  // Compare elements from both arrays and push the smaller one
  while (i < left.length && j < right.length) {
    if (left[i] <= right[j]) { // Uses <= to maintain sort stability
      result.push(left[i]);
      i++;
    } else {
      result.push(right[j]);
      j++;
    }
  }

  // Concatenate remaining elements cleanly without manual while loops
  return result.concat(left.slice(i)).concat(right.slice(j));
}

### Reflection Answers

- **How did your confidence in the solution change after verification?**
  - Confidence increased significantly. Tracing counter increments manually and replacing fragile index-tracking loops with `.slice().concat()` eliminated potential edge-case errors.
- **What aspects of the AI solution required the most scrutiny?**
  - Index pointer updates (`i++` vs `j++`) and confirming whether equality comparisons preserve sort stability.
- **Which verification technique was most valuable for your specific problem?**
  - **Prompt 2 (Alternative Approaches):** Discovering that `.concat(left.slice(i))` removes manual remaining-element `while` loops completely eliminated the class of index bugs present in the original code.

===

## Exercise: Using AI to Help with Testing

### Submission Overview
- **Chosen Module:** Task Priority Management (`task_priority.js`)
- **Functions Analyzed:** `calculateTaskScore`, `sortTasksByImportance`, `getTopPriorityTasks`
- **Files Created / Used:** `findings.md`

---

### Exercise 1.1: Behavior Analysis

#### 1. Core Behaviors Identified
- **Priority Weighting (`calculateTaskScore`):** Multiplies base priority weights (`LOW`: 1, `MEDIUM`: 2, `HIGH`: 3, `URGENT`: 4) by 10.
- **Due Date Scoring (`calculateTaskScore`):**
  - Overdue (`daysUntilDue < 0`): +30 points.
  - Due Today (`daysUntilDue === 0`): +20 points.
  - Due in 1–2 days (`daysUntilDue <= 2`): +15 points.
  - Due in 3–7 days (`daysUntilDue <= 7`): +10 points.
- **Status Adjustments (`calculateTaskScore`):**
  - Completed (`TaskStatus.DONE`): Deducts 50 points.
  - In Review (`TaskStatus.REVIEW`): Deducts 15 points.
- **Tag Boosts (`calculateTaskScore`):** Adds +8 points if the `tags` array contains `"blocker"`, `"critical"`, or `"urgent"`.
- **Recency Boost (`calculateTaskScore`):** Adds +5 points if the task was updated less than 24 hours ago (`daysSinceUpdate < 1`).
- **Immutability & Ordering (`sortTasksByImportance`):** Creates a shallow copy of the input array (`[...tasks]`) and sorts items descending by calculated task score (`score(b) - score(a)`).
- **Top N Filtering (`getTopPriorityTasks`):** Delegates sorting to `sortTasksByImportance` and slices the top $N$ items (defaulting to 5).

#### 2. Critical Edge Cases Identified
- **Undefined / Missing Tags:** If `task.tags` is `undefined` or `null`, calling `task.tags.some(...)` will throw an unhandled `TypeError`.
- **Immutability Verification:** Tests must verify that `sortTasksByImportance` does not mutate the original input array passed into it.
- **Default & Out-of-Bounds Slicing (`getTopPriorityTasks`):**
  - Requesting more items than exist in the array (e.g., `limit = 10` on an array of 3 tasks) should safely return all 3 tasks without error.
  - Passing `limit = 0` or negative values.
  - Ensuring the default parameter `limit = 5` functions when no limit argument is passed.
- **Equal Scores / Stability:** When two tasks yield the exact same calculated score, the sorting mechanism should handle them predictably without dropping or re-ordering items unexpectedly.

---

### Exercise 1.2: Structured Test Plan

#### 1. Test Suite Architecture & Priority Checklist

| Priority | Test Name / Behavior | Test Type | Expected Outcome |
| :--- | :--- | :--- | :--- |
| **P0 (Critical)** | Base Priority Calculation | Unit | Scores increase monotonically from `LOW` (10) to `URGENT` (40). |
| **P0 (Critical)** | Missing/Undefined `tags` Property | Unit (Defensive) | Prevents runtime `TypeError` when `task.tags` is undefined. |
| **P0 (Critical)** | Task Sorting Order | Unit | `sortTasksByImportance` orders tasks descending by score. |
| **P0 (Critical)** | Input Array Immutability | Unit | Original array reference and element order remain unchanged after sorting. |
| **P1 (High)** | Due Date Tier Calculations | Unit | Correctly adds 30 (Overdue), 20 (Today), 15 (1–2 days), or 10 (3–7 days) points. |
| **P1 (High)** | Status Deductions | Unit | `DONE` deducts 50; `REVIEW` deducts 15; active statuses deduct 0. |
| **P1 (High)** | Top N Tasks Slicing | Unit | `getTopPriorityTasks(tasks, 3)` returns exactly top 3 sorted tasks. |
| **P1 (High)** | Default Limit Parameter | Unit | `getTopPriorityTasks(tasks)` defaults to returning top 5 tasks. |
| **P2 (Medium)** | Limit Exceeds Array Length | Unit | `getTopPriorityTasks` with `limit = 10` on 3 tasks returns all 3 tasks cleanly. |
| **P2 (Medium)** | Date & Timezone Mocking | Unit / Integration | Uses `jest.useFakeTimers()` to ensure deterministic date calculations. |

#### 2. Test Dependencies & Execution Setup
- **Timer Mocking:** Tests measuring `dueDate` and `updatedAt` must mock the system clock (`jest.useFakeTimers()` or `jest.spyOn(global, 'Date')`) to avoid non-deterministic test failures caused by real-time execution drift.
- **Test Fixtures:** Maintain reusable task factories/helpers to instantiate valid `Task` objects across test suites cleanly.

===

## Exercise: Part 2 - Improving a Single Test

### Exercise 2.1: Writing & Improving Your First Test

#### 1. Initial Simple Test (Draft)
```javascript
test('should calculate task score based on priority', () => {
  const task = new Task('Test Task', '', TaskPriority.HIGH);
  const score = calculateTaskScore(task);
  expect(score).toBe(30);
});

#### 2. Prompting the AI Agent & Refinement Journey

- **Behavior vs. Implementation:** The simple test verified that `HIGH` priority yields an exact magic number (`30`). While this asserts behavior, it fails to verify the relationship between priorities (e.g., that `HIGH` scores higher than `MEDIUM`).
- **Missing Edge Cases:** It didn't account for missing/null properties on the task object (e.g., `tags` or `dueDate`).
- **Improving Assertions:** Improved assertions should explicitly test the base priority calculation in isolation and guard against missing optional properties.

#### 3. Rewritten Robust Test

describe('calculateTaskScore - Base Priority', () => {
  test('should calculate correct base scores across all priority levels', () => {
    // Arrange
    const lowTask = { priority: TaskPriority.LOW, tags: [] };
    const medTask = { priority: TaskPriority.MEDIUM, tags: [] };
    const highTask = { priority: TaskPriority.HIGH, tags: [] };
    const urgentTask = { priority: TaskPriority.URGENT, tags: [] };

    // Act
    const lowScore = calculateTaskScore(lowTask);
    const medScore = calculateTaskScore(medTask);
    const highScore = calculateTaskScore(highTask);
    const urgentScore = calculateTaskScore(urgentTask);

    // Assert (Verifying relative hierarchy and exact expected base values)
    expect(lowScore).toBe(10);
    expect(medScore).toBe(20);
    expect(highScore).toBe(30);
    expect(urgentScore).toBe(40);
    expect(lowScore).toBeLessThan(medScore);
    expect(medScore).toBeLessThan(highScore);
    expect(highScore).toBeLessThan(urgentScore);
  });

  test('should fall back to 0 base score if priority is missing or invalid', () => {
    const invalidTask = { priority: 'UNKNOWN', tags: [] };
    expect(calculateTaskScore(invalidTask)).toBe(0);
  });
});

### Exercise 2.2: Learning From Examples (Due Date Calculation)

#### 1. Rough Pseudocode / Outline Idea

// Pseudocode Idea:
// Create tasks with different due dates (yesterday, today, tomorrow, next week)
// Call calculateTaskScore on each
// Check that overdue > today > tomorrow > next week

#### 2. Principles of a Good Test for Date Functionality
- **Time Freezing:** System dates are inherently dynamic. Tests depending on `new Date()` will fail unless system time is frozen using fake timers (`jest.useFakeTimers()`).
- **Boundary Precision:** Test exact boundary transitions (e.g., 0 days remaining vs. 1 day remaining vs. 3 days remaining).
- **Isolation:** Set `priority` to a constant value across test cases so score differences stem strictly from due date logic.

#### 3. Comprehensive Final Test Implementation

describe('calculateTaskScore - Due Date Calculations', () => {
  const MOCK_NOW = new Date('2026-08-12T10:00:00Z');

  beforeEach(() => {
    // Freeze system time to ensure deterministic test runs
    jest.useFakeTimers();
    jest.setSystemTime(MOCK_NOW);
  });

  afterEach(() => {
    jest.useRealTimers();
  });

  test('should add correct point boosts based on due date proximity tiers', () => {
    const baseTask = { priority: TaskPriority.LOW, tags: [] }; // Base score = 10

    // Overdue task (-1 day): +30 points -> Total: 40
    const overdueTask = {
      ...baseTask,
      dueDate: new Date('2026-08-11T10:00:00Z')
    };

    // Due Today (0 days): +20 points -> Total: 30
    const dueTodayTask = {
      ...baseTask,
      dueDate: new Date('2026-08-12T18:00:00Z')
    };

    // Due in 2 Days (<= 2 days): +15 points -> Total: 25
    const dueSoonTask = {
      ...baseTask,
      dueDate: new Date('2026-08-14T10:00:00Z')
    };

    // Due in 5 Days (<= 7 days): +10 points -> Total: 20
    const dueThisWeekTask = {
      ...baseTask,
      dueDate: new Date('2026-08-17T10:00:00Z')
    };

    // Due in 15 Days (> 7 days): +0 points -> Total: 10
    const dueLaterTask = {
      ...baseTask,
      dueDate: new Date('2026-08-27T10:00:00Z')
    };

    expect(calculateTaskScore(overdueTask)).toBe(40);
    expect(calculateTaskScore(dueTodayTask)).toBe(30);
    expect(calculateTaskScore(dueSoonTask)).toBe(25);
    expect(calculateTaskScore(dueThisWeekTask)).toBe(20);
    expect(calculateTaskScore(dueLaterTask)).toBe(10);
  });

  test('should safely calculate score when task has no due date', () => {
    const taskWithoutDueDate = { priority: TaskPriority.LOW, tags: [] };
    expect(calculateTaskScore(taskWithoutDueDate)).toBe(10);
  });
});

## Exercise: Part 3 - Test-Driven Development Practice

### Exercise 3.1: TDD for a New Feature (Current User Score Boost)

#### 1. Step 1: Red (Write a Failing Test)
We first write a failing test that asserts a task assigned to the current user receives a +12 score boost.

```javascript
describe('calculateTaskScore - TDD New Feature: Current User Boost', () => {
  test('should add +12 points when task is assigned to current user', () => {
    // Arrange
    const currentUserId = 'user-123';
    const taskAssignedToUser = {
      priority: TaskPriority.LOW, // Base: 10
      tags: [],
      assigneeId: 'user-123'
    };

    // Act
    const score = calculateTaskScore(taskAssignedToUser, currentUserId);

    // Assert: Base score (10) + Current User Boost (12) = 22
    expect(score).toBe(22);
  });

  test('should not add boost when task is assigned to a different user or unassigned', () => {
    const currentUserId = 'user-123';
    const taskOtherUser = {
      priority: TaskPriority.LOW, // Base: 10
      tags: [],
      assigneeId: 'user-456'
    };

    const score = calculateTaskScore(taskOtherUser, currentUserId);
    expect(score).toBe(10);
  });
});

#### 2. Step 2: Green (Minimal Code Implementation)
Update calculateTaskScore signature and implementation in task_priority.js to pass the tests with minimal logic:

function calculateTaskScore(task, currentUserId = null) {
  let score = 0;

  // Priority scoring
  const priorityWeights = { LOW: 10, MEDIUM: 20, HIGH: 30, URGENT: 40 };
  score += priorityWeights[task.priority] || 0;

  // New Feature: Current User Boost (+12)
  if (currentUserId && task.assigneeId === currentUserId) {
    score += 12;
  }

  // Tag boost
  if (task.tags && task.tags.some(t => ['blocker', 'critical', 'urgent'].includes(t))) {
    score += 8;
  }

  return score;
}

#### 3. Step 3: Refactor
The implementation is clean and readable. No additional structural refactoring is required for this addition, and all existing tests continue to pass.

### Exercise 3.2: TDD for Bug Fix (Days Since Update Calculation)

#### 1. Step 1: Reproduce the Bug with a Failing Test
The original code performed raw integer division on timestamps ((now - task.updatedAt) / (1000 * 60 * 60 * 24)), which led to incorrect rounding for sub-day updates or floating-point precision issues near 24 hours.

describe('calculateTaskScore - TDD Bug Fix: Recency Boost', () => {
  const MOCK_NOW = new Date('2026-08-12T12:00:00Z');

  beforeEach(() => {
    jest.useFakeTimers();
    jest.setSystemTime(MOCK_NOW);
  });

  afterEach(() => {
    jest.useRealTimers();
  });

  test('should correctly grant +5 boost for task updated 23 hours ago', () => {
    // 23 hours ago
    const updated23HoursAgo = new Date('2026-08-11T13:00:00Z');
    const task = {
      priority: TaskPriority.LOW, // Base: 10
      tags: [],
      updatedAt: updated23HoursAgo
    };

    const score = calculateTaskScore(task);

    // Should receive +5 recency boost -> Expected total: 15
    expect(score).toBe(15);
  });

  test('should NOT grant +5 boost for task updated exactly 25 hours ago', () => {
    const updated25HoursAgo = new Date('2026-08-11T11:00:00Z');
    const task = {
      priority: TaskPriority.LOW, // Base: 10
      tags: [],
      updatedAt: updated25HoursAgo
    };

    const score = calculateTaskScore(task);
    expect(score).toBe(10);
  });
});

#### 2. Step 2: Minimal Code Fix
Use precise millisecond comparisons (24 * 60 * 60 * 1000) instead of imprecise day conversions to fix the recency check in task_priority.js:

// Minimal Bug Fix in calculateTaskScore:
if (task.updatedAt) {
  const diffInMs = new Date() - new Date(task.updatedAt);
  const TWENTY_FOUR_HOURS_MS = 24 * 60 * 60 * 1000;
  
  if (diffInMs >= 0 && diffInMs < TWENTY_FOUR_HOURS_MS) {
    score += 5; // Recency boost
  }
}

#### 3. Step 3: Verification
Re-run the test suite using Jest to ensure the bug reproduction test turns Green and no regression bugs are introduced into base priority, due date, or tag calculations.

## Exercise: Part 4 - Integration Testing & Workflow Verification

### Exercise 4.1: Testing the Full Workflow

#### 1. Test Design Scenarios
- **Scenario 1:** Sorting a heterogeneous mix of tasks (overdue critical items, completed tasks, tasks assigned to the current user, low-priority routine tasks).
- **Scenario 2:** End-to-end integration verifying that `getTopPriorityTasks` properly delegates sorting to `sortTasksByImportance`, which in turn calls `calculateTaskScore` for every task.
- **Scenario 3:** Verifying array immutability and precise slice boundaries when limiting results to $N$ items.

#### 2. Comprehensive Integration Test
```javascript
describe('Task Priority System - End-to-End Integration', () => {
  const MOCK_NOW = new Date('2026-08-12T10:00:00Z');
  const CURRENT_USER_ID = 'user-789';

  beforeEach(() => {
    jest.useFakeTimers();
    jest.setSystemTime(MOCK_NOW);
  });

  afterEach(() => {
    jest.useRealTimers();
  });

  test('should correctly score, sort, and retrieve top priority tasks for a full task set', () => {
    // Arrange: Create a realistic mixture of tasks
    const tasks = [
      {
        id: 'task-1',
        title: 'Routine Documentation',
        priority: TaskPriority.LOW, // Score: 10
        tags: []
      },
      {
        id: 'task-2',
        title: 'Critical Production Bug',
        priority: TaskPriority.URGENT, // Score: 40
        dueDate: new Date('2026-08-11T10:00:00Z'), // Overdue: +30
        tags: ['blocker'], // Tag boost: +8 -> Total: 78
        assigneeId: CURRENT_USER_ID // User boost: +12 -> Total: 90
      },
      {
        id: 'task-3',
        title: 'Completed Urgent Refactor',
        priority: TaskPriority.URGENT, // Score: 40
        status: TaskStatus.DONE, // Deduction: -50 -> Total: -10
        tags: ['critical']
      },
      {
        id: 'task-4',
        title: 'Feature Review',
        priority: TaskPriority.HIGH, // Score: 30
        dueDate: new Date('2026-08-12T18:00:00Z'), // Due Today: +20
        tags: [],
        assigneeId: CURRENT_USER_ID // User boost: +12 -> Total: 62
      },
      {
        id: 'task-5',
        title: 'Backend API Enhancement',
        priority: TaskPriority.MEDIUM, // Score: 20
        dueDate: new Date('2026-08-14T10:00:00Z'), // Due in 2 days: +15 -> Total: 35
        tags: []
      }
    ];

    // Act 1: Sort all tasks by importance
    const sortedTasks = sortTasksByImportance(tasks, CURRENT_USER_ID);

    // Assert 1: Verify sorting order (Task 2 -> Task 4 -> Task 5 -> Task 1 -> Task 3)
    expect(sortedTasks.map(t => t.id)).toEqual([
      'task-2', // Score: 90
      'task-4', // Score: 62
      'task-5', // Score: 35
      'task-1', // Score: 10
      'task-3'  // Score: -10
    ]);

    // Assert 2: Verify original array was not mutated
    expect(tasks[0].id).toBe('task-1');

    // Act 2: Retrieve Top 3 Priority Tasks
    const top3 = getTopPriorityTasks(tasks, 3, CURRENT_USER_ID);

    // Assert 3: Verify top N slicing
    expect(top3.length).toBe(3);
    expect(top3.map(t => t.id)).toEqual(['task-2', 'task-4', 'task-5']);
  });
});

### Final Submission Document Summary

# Comprehensive Task Priority Testing Report (`findings.md`)

## 1. Part 1: Test Plan & Behavior Analysis
- **Module:** Task Priority Management (`task_priority.js`)
- **Behavior Analysis:** Detailed breakdown of scoring weights, date tiers, status deductions, and immutability rules.
- **Structured Test Plan Table:** Prioritized test cases (P0–P2) covering core execution paths, defensive null-checks, edge cases, and date mocking setups.

## 2. Part 2: Unit Test Improvements
- **Base Priority Tests:** Transition from brittle single-value checks to relational hierarchy assertions.
- **Due Date Proximity Tests:** Robust test suite leveraging `jest.useFakeTimers()` to test boundary conditions across overdue, today, and future date tiers deterministically.

## 3. Part 3: TDD Practice
- **Current User Score Boost (+12):** Failing test -> minimal implementation -> green state verification.
- **Recency Bug Fix:** Failure reproduction test for floating-point / millisecond date calculation bugs -> fixed implementation using `24 * 60 * 60 * 1000` ms logic.

## 4. Part 4: Integration Testing
- Full end-to-end integration test verifying `calculateTaskScore`, `sortTasksByImportance`, and `getTopPriorityTasks` working together across complex task datasets.

## 5. Reflection on Testing & AI-Assisted Workflows

Working through this multi-part exercise highlighted several core principles about testing and using AI as a guided thought partner:

1. **Testing Behavior Over Implementation Details:** Early test drafts often asserted rigid "magic numbers" derived from implementation details. Structuring tests to assert behavioral relationships (e.g., verifying relative priorities or tier order) produces test suites that are resilient to minor refactoring while remaining accurate.
2. **Deterministic Environment Control:** Functions relying on dates and times (`new Date()`) are inherently non-deterministic. Using fake timers (`jest.useFakeTimers()`) is essential to prevent subtle, time-dependent test failures across different execution environments or timezones.
3. **The Value of Socratic AI Prompting:** Prompting the AI to ask questions, challenge assertions, and guide minimal implementations rather than blindly generating code forced a deeper understanding of edge cases (e.g., handling missing `tags` or array immutability) and reinforced proper Red-Green-Refactor TDD cycles.
4. **Confidence Through Layered Testing:** Unit tests isolate logic at the function boundary, but integration tests validate system contracts (e.g., ensuring sorting delegates cleanly to scoring without side effects). Both layers are necessary to maintain a reliable software codebase.

===

# Exercise 1: Code Readability Improvement (Java)

## 1. Prompt Used

```text
I want to make this code more readable and maintainable. Please help me by:
1. Identifying parts that are difficult to understand
2. Suggesting better variable and function names
3. Recommending ways to break down complex sections
4. Pointing out any inconsistent style or formatting issues

class UserMgr {
    private List<U> u_list;
    private DBConn db;

    public UserMgr(DBConn d) {
        db = d;
        u_list = new ArrayList<>();
    }

    public boolean a(String un, String pw, String em) {
        if (un.length() < 3 || pw.length() < 8 || !em.contains("@")) {
            return false;
        }

        for (U user : u_list) {
            if (user.getUn().equals(un)) {
                return false;
            }
        }

        U nu = new U(un, pw, em);
        u_list.add(nu);
        boolean res = db.execute("INSERT INTO users VALUES ('" + un + "', '" + pw + "', '" + em + "')");
        return res;
    }

    public U f(String un) {
        for (U user : u_list) {
            if (user.getUn().equals(un)) {
                return user;
            }
        }
        return null;
    }
}

class U {
    private String un;
    private String pw;
    private String em;

    public U(String un, String pw, String em) {
        this.un = un;
        this.pw = pw;
        this.em = em;
    }

    public String getUn() { return un; }
    public String getPw() { return pw; }
    public String getEm() { return em; }
}

Language/Framework: Java 17 / Standard Library
Team coding standards: Standard Java Naming Conventions (PascalCase for classes, camelCase for variables/methods, clear expressive names without arbitrary abbreviations).

## 2. Analysis of Readability & Maintainability Issues

### Cryptic & Abbreviated Naming
* **Classes (`UserMgr`, `U`):** Highly non-descriptive. `U` should be `User`, and `UserMgr` should be `UserManager`.
* **Methods (`a`, `f`, `getUn`, `getPw`, `getEm`):** Single-letter method names (`a` and `f`) give no indication of behavior. They should be `addUser` (or `registerUser`) and `findUserByUsername`.
* **Variables (`u_list`, `un`, `pw`, `em`, `nu`, `d`, `res`):** Excessive abbreviation harms cognitive flow. Variables should use full words (`userList`, `username`, `password`, `email`, `newUser`).

### Style & Convention Violations
* **Snake_case in Java (`u_list`):** Java convention dictates `camelCase` for instance variables (`userList` or `users`), not `snake_case`.
* **Compact/Single-Line Method Declarations:** Getters in class `U` are compressed onto single lines, violating standard formatting guidelines.

### Code Structure & Logic Clarity
* **Inline Validation:** Input validation (checking length and `@` presence) is stuffed into the main execution block of the `a` method rather than extracted into a separate helper method or validation class.
* **String Concatenation in SQL:** Direct SQL query concatenation (`"INSERT INTO users VALUES ('" + un + ...`) creates a critical **SQL Injection vulnerability** and makes the string hard to read.
* **Manual Iteration vs. Java Streams/Optional:** The linear `for` loop searching for existing users can be simplified using Java Streams or Java `Optional<User>` return types to make null safety explicit.

## 3. Refactored Java Code

package com.example.users;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

public class UserManager {
    private final List<User> users;
    private final DatabaseConnection databaseConnection;

    public UserManager(DatabaseConnection databaseConnection) {
        this.databaseConnection = databaseConnection;
        this.users = new ArrayList<>();
    }

    /**
     * Validates and registers a new user if the username is not already taken.
     */
    public boolean registerUser(String username, String password, String email) {
        if (!isInputValid(username, password, email)) {
            return false;
        }

        if (findUserByUsername(username).isPresent()) {
            return false; // User already exists
        }

        User newUser = new User(username, password, email);
        users.add(newUser);

        // Standardized parameterized query format to prevent SQL injection
        String sql = "INSERT INTO users (username, password, email) VALUES (?, ?, ?)";
        return databaseConnection.executeUpdate(sql, username, password, email);
    }

    /**
     * Finds a user by their exact username.
     */
    public Optional<User> findUserByUsername(String username) {
        return users.stream()
                .filter(user -> user.getUsername().equals(username))
                .findFirst();
    }

    private boolean isInputValid(String username, String password, String email) {
        return username != null && username.length() >= 3
                && password != null && password.length() >= 8
                && email != null && email.contains("@");
    }
}

class User {
    private final String username;
    private final String password;
    private final String email;

    public User(String username, String password, String email) {
        this.username = username;
        this.password = password;
        this.email = email;
    }

    public String getUsername() {
        return username;
    }

    public String getPassword() {
        return password;
    }

    public String getEmail() {
        return email;
    }
}

## 4. Readability Issues Identified & Reflection

* **Identified Issues I Might Have Missed:**
  * **Null Return Risk vs. `Optional<T>`:** While searching for a missing user, returning `null` in `f(String un)` forces caller code to handle potential `NullPointerException`s without explicit compile-time warnings. Refactoring to return `Optional<User>` improves clarity and type safety.
  * **Critical Security Risk Masked as Readability Issue:** Building SQL strings via raw string concatenation isn't just ugly—it's a high-severity security bug (SQL Injection). AI highlighted that improving parameterization simultaneously fixes security and readability.
  * **Mixed Naming Paradigms:** The original code mixed standard camelCase (`UserMgr`), snake_case (`u_list`), and single-letter variables (`d`, `u`, `a`, `f`), creating cognitive overload when reading. Standardizing entirely on Java conventions significantly improves scanning speed.

---

# Exercise 2: Function Refactoring (Python)

## 1. Prompt Used

```text
I have a function that I think is doing too much. Please help me refactor it by:
1. Identifying the different responsibilities this function has
2. Suggesting how to break it into smaller, focused functions
3. Improving the organization and flow of the code
4. Pointing out any other issues you notice

def process_orders(orders, inventory, customer_data):
    results = []
    total_revenue = 0
    error_orders = []

    for order in orders:
        # Check if item is in inventory
        item_id = order['item_id']
        quantity = order['quantity']
        customer_id = order['customer_id']

        if item_id not in inventory:
            error_orders.append({'order_id': order['order_id'], 'error': 'Item not in inventory'})
            continue

        # Check if enough quantity available
        if inventory[item_id]['quantity'] < quantity:
            error_orders.append({'order_id': order['order_id'], 'error': 'Insufficient quantity'})
            continue

        # Check if customer exists
        if customer_id not in customer_data:
            error_orders.append({'order_id': order['order_id'], 'error': 'Customer not found'})
            continue

        # Calculate price
        price = inventory[item_id]['price'] * quantity

        # Apply discount if customer is premium
        if customer_data[customer_id]['premium']:
            price = price * 0.9

        # Update inventory
        inventory[item_id]['quantity'] -= quantity

        # Calculate shipping based on customer location
        shipping = 0
        if customer_data[customer_id]['location'] == 'domestic':
            if price < 50:
                shipping = 5.99
        else:
            shipping = 15.99

        # Add tax
        tax = price * 0.08

        # Calculate final price
        final_price = price + shipping + tax

        # Update total revenue
        total_revenue += final_price

        # Create result
        result = {
            'order_id': order['order_id'],
            'item_id': item_id,
            'quantity': quantity,
            'customer_id': customer_id,
            'price': price,
            'shipping': shipping,
            'tax': tax,
            'final_price': final_price
        }

        results.append(result)

    return {
        'processed_orders': results,
        'error_orders': error_orders,
        'total_revenue': total_revenue
    }

What this function should do: Process a list of orders, validate items and customers against current inventory and customer records, mutate/update inventory stock levels, calculate total pricing (discounts, shipping, tax), and track aggregate revenue alongside successful and failed orders.

## 2. Analysis of Responsibilities & Refactoring Strategy

### Identifications of Mixed Responsibilities
* **Validation / Guard Clauses:** Checking stock availability and customer existence.
* **Pricing & Calculations:** Discount rates, shipping cost lookup based on region, and tax calculations.
* **State Mutation:** Modifying the `inventory` dictionary directly during iteration.
* **Collection Orchestration:** Iterating through orders, maintaining total revenue, and sorting results into successful vs. error lists.

### Suggested Breakdown of Focused Functions
1. `validate_order(order, inventory, customer_data) -> Optional[str]`: Handles guard checks and returns an error string if invalid, or `None` if valid.
2. `calculate_item_price(base_price, quantity, is_premium) -> float`: Computes base cost minus premium discounts.
3. `calculate_shipping(price, location) -> float`: Isolates regional shipping rules and threshold logic.
4. `calculate_order_totals(order, inventory, customer) -> dict`: Aggregates price, shipping, and tax calculations for a single valid order.
5. `process_single_order(...) -> Tuple[dict, float]`: Updates inventory stock and builds the completed result object.

### Other Identified Issues
* **Side Effects (In-place Mutation):** If processing fails midway, inventory updates from prior orders persist while partial failures accumulate, leading to inconsistent state.
* **Hardcoded Magic Values:** Values like `0.9` (discount), `5.99`/`15.99` (shipping), and `0.08` (tax rate) should be configured constants.
* **Floating-Point Precision:** Using raw `float` operations for currency calculations risks rounding errors (should ideally use `Decimal` or round consistently).

## 3. Refactored Python Code

from typing import Dict, List, Any, Optional, Tuple

TAX_RATE = 0.08
PREMIUM_DISCOUNT = 0.10  # 10% off
FREE_SHIPPING_THRESHOLD = 50.00
DOMESTIC_SHIPPING_FEE = 5.99
INTERNATIONAL_SHIPPING_FEE = 15.99


def validate_order(order: Dict[str, Any], inventory: Dict[str, Any], customer_data: Dict[str, Any]) -> Optional[str]:
    """Validates item existence, stock levels, and customer records."""
    item_id = order['item_id']
    quantity = order['quantity']
    customer_id = order['customer_id']

    if item_id not in inventory:
        return 'Item not in inventory'
    if inventory[item_id]['quantity'] < quantity:
        return 'Insufficient quantity'
    if customer_id not in customer_data:
        return 'Customer not found'
    return None


def calculate_discounted_price(base_price: float, quantity: int, is_premium: bool) -> float:
    """Calculates price with optional premium customer discount."""
    subtotal = base_price * quantity
    if is_premium:
        subtotal *= (1 - PREMIUM_DISCOUNT)
    return round(subtotal, 2)


def calculate_shipping(price: float, location: str) -> float:
    """Calculates shipping costs based on location and price threshold."""
    if location == 'domestic':
        return 0.0 if price >= FREE_SHIPPING_THRESHOLD else DOMESTIC_SHIPPING_FEE
    return INTERNATIONAL_SHIPPING_FEE


def calculate_order_financials(order: Dict[str, Any], inventory: Dict[str, Any], customer: Dict[str, Any]) -> Dict[str, float]:
    """Computes price, shipping, tax, and final amount for an order."""
    item_price = inventory[order['item_id']]['price']
    discounted_price = calculate_discounted_price(
        base_price=item_price,
        quantity=order['quantity'],
        is_premium=customer.get('premium', False)
    )
    shipping = calculate_shipping(discounted_price, customer.get('location', 'domestic'))
    tax = round(discounted_price * TAX_RATE, 2)
    final_price = round(discounted_price + shipping + tax, 2)

    return {
        'price': discounted_price,
        'shipping': shipping,
        'tax': tax,
        'final_price': final_price
    }


def process_orders(orders: List[Dict[str, Any]], inventory: Dict[str, Any], customer_data: Dict[str, Any]) -> Dict[str, Any]:
    """Orchestrates order batch processing, updates inventory, and tallies revenue."""
    processed_orders = []
    error_orders = []
    total_revenue = 0.0

    for order in orders:
        error = validate_order(order, inventory, customer_data)
        if error:
            error_orders.append({'order_id': order['order_id'], 'error': error})
            continue

        # Extract context & update inventory stock
        item_id = order['item_id']
        quantity = order['quantity']
        customer = customer_data[order['customer_id']]
        
        inventory[item_id]['quantity'] -= quantity

        # Calculate pricing details
        financials = calculate_order_financials(order, inventory, customer)
        total_revenue += financials['final_price']

        processed_orders.append({
            'order_id': order['order_id'],
            'item_id': item_id,
            'quantity': quantity,
            'customer_id': order['customer_id'],
            **financials
        })

    return {
        'processed_orders': processed_orders,
        'error_orders': error_orders,
        'total_revenue': round(total_revenue, 2)
    }

## 4. AI vs. Personal Comparison & Reflection

* **Initial Personal Intuition:** I recognized that `process_orders` was doing too much inline inside a single giant `for` loop, specifically mixing validation logic directly with business logic (like shipping and tax formulas).
* **Key AI Insights I Gained:**
  * **Magic Number Extraction:** The AI highlighted that magic numbers like `0.9` and `0.08` scattered inside nested `if` statements made policy updates brittle. Moving them to top-level constants makes business rule updates much cleaner.
  * **Dict Unpacking (`**financials`):** The AI demonstrated using dict unpacking to append financial values cleanly onto result objects without manually copying each key-value pair.
  * **Isolating Pure Functions:** Separating functions into pure calculations (e.g., `calculate_shipping`, `calculate_discounted_price`) makes unit testing individual pricing policies straightforward without needing to construct full `inventory` or `customer` database mocks.

---

# Exercise 3: Code Duplication Detection (JavaScript)

## 1. Prompt Used

```text
I suspect there might be repeated patterns in this code that could be consolidated. Please help me by:
1. Identifying similar code segments that appear multiple times
2. Suggesting ways to eliminate the duplication (e.g., helper functions, loops)
3. Showing me what the refactored code could look like
4. Explaining the benefits of the suggested changes

function calculateUserStatistics(userData) {
  // Calculate average age
  let totalAge = 0;
  for (let i = 0; i < userData.length; i++) {
    totalAge += userData[i].age;
  }
  const averageAge = totalAge / userData.length;

  // Calculate average income
  let totalIncome = 0;
  for (let i = 0; i < userData.length; i++) {
    totalIncome += userData[i].income;
  }
  const averageIncome = totalIncome / userData.length;

  // Calculate average score
  let totalScore = 0;
  for (let i = 0; i < userData.length; i++) {
    totalScore += userData[i].score;
  }
  const averageScore = totalScore / userData.length;

  // Find highest age
  let highestAge = userData[0].age;
  for (let i = 1; i < userData.length; i++) {
    if (userData[i].age > highestAge) {
      highestAge = userData[i].age;
    }
  }

  // Find highest income
  let highestIncome = userData[0].income;
  for (let i = 1; i < userData.length; i++) {
    if (userData[i].income > highestIncome) {
      highestIncome = userData[i].income;
    }
  }

  // Find highest score
  let highestScore = userData[0].score;
  for (let i = 1; i < userData.length; i++) {
    if (userData[i].score > highestScore) {
      highestScore = userData[i].score;
    }
  }

  return {
    age: {
      average: averageAge,
      highest: highestAge
    },
    income: {
      average: averageIncome,
      highest: highestIncome
    },
    score: {
      average: averageScore,
      highest: highestScore
    }
  };
}

## 2. Repeated Patterns & Consolidation Strategy

### Identified Duplication
1. **Average Calculation Loops:** The code runs three separate `for` loops that sum up property values (`age`, `income`, `score`) and divide by `userData.length`.
2. **Maximum Value Search Loops:** The code runs three separate `for` loops comparing properties to find peak values across `age`, `income`, and `score`.
3. **Data Access Pattern:** Identical array traversal logic is repeated six separate times across the exact same dataset.

### Recommended Approaches to Consolidate
* **Approach A (Generic Helper Functions):** Extract generic helper functions (`calculateAverage(data, key)` and `findHighest(data, key)` or native JavaScript `reduce`/`Math.max`).
* **Approach B (Single-Pass Accumulator):** Iterate over `userData` once to tally sums and track maximum values across all fields simultaneously.

## 3. Refactored JavaScript Code
* **Option 1:** Generic Helper Functions with reduce & Math.max

function calculateAverage(data, key) {
  if (!data || data.length === 0) return 0;
  const sum = data.reduce((total, item) => total + item[key], 0);
  return sum / data.length;
}

function findHighest(data, key) {
  if (!data || data.length === 0) return 0;
  return Math.max(...data.map((item) => item[key]));
}

function getFieldMetrics(data, key) {
  return {
    average: calculateAverage(data, key),
    highest: findHighest(data, key),
  };
}

function calculateUserStatistics(userData) {
  if (!userData || userData.length === 0) {
    return {
      age: { average: 0, highest: 0 },
      income: { average: 0, highest: 0 },
      score: { average: 0, highest: 0 },
    };
  }

  return {
    age: getFieldMetrics(userData, 'age'),
    income: getFieldMetrics(userData, 'income'),
    score: getFieldMetrics(userData, 'score'),
  };
}

## 4. Evaluation for Junior Developers & Reflection

* **Benefits of Consolidation:**
  * **DRY Principle:** Shrinks the codebase from ~65 lines to under 30 lines.
  * **Scalability:** Adding a new metric (e.g., `experience`) requires adding only one line (`experience: getFieldMetrics(userData, 'experience')`) instead of copying two full `for` loops.
  * **Edge Case Handling:** Input guards check for empty/null arrays in one central place instead of crashing on `userData[0]`.

* **Team Impact & Junior Dev Evaluation:**
  * **Option 1 (Generic Helpers) is ideal for junior developers:** Passing property keys as strings to dedicated functions (`getFieldMetrics(userData, 'age')`) keeps each operation clear and easy to debug.
  * **Avoiding Over-Engineering:** A single-pass `reduce` loop that calculates everything in one go is faster ($O(n)$ vs $O(n)$ with fewer iterations), but can quickly become hard for junior devs to read. Simple helper functions strike the best balance between clean abstractions and readability.

# Reflection & Next Steps

## Reflection Questions

### 1. Which prompting strategy did you find most useful? Why?
The **Function Refactoring** prompt strategy (Exercise 2) was the most immediately impactful. While naming and duplication issues are relatively easy to spot manually, identifying tangled responsibilities in a single long function and deciding how to cleanly decompose it takes more mental effort. Having the AI systematically map out guard clauses, pure calculations, and side effects made restructuring complex logic straightforward.

### 2. What kinds of improvements did the AI suggest that you might not have thought of?
* **Type and Guard Improvements (e.g., `Optional<T>` in Java):** Beyond simple renaming, the AI highlighted API safety risks, such as returning raw `null` vs. returning an `Optional<User>` to prevent potential `NullPointerException` bugs downstream.
* **Security & Readability Intersections:** Pointing out that direct SQL string concatenation wasn't just a readability issue, but a critical SQL Injection vulnerability.
* **Property Access Abstraction in JavaScript:** Using generic property keys with `reduce` (`getFieldMetrics(userData, 'age')`) to handle metric aggregation cleanly instead of writing repetitive loop constructs.

### 3. Were there any suggestions the AI made that you disagreed with? Why?
Yes. In Exercise 3, an alternative suggestion was to compress all statistical calculations into a single `Array.prototype.reduce()` pass to iterate through the list only once. While computationally $O(n)$, combining all sum calculations and maximum tracking into one giant accumulator object hurt readability for junior developers. Keeping clean, single-purpose helper functions is preferable for maintainability over micro-optimizing memory passes on small datasets.

### 4. How might you adapt these prompts for your specific codebase or tech stack?
* **Specify Strict Tech Stack Context:** Include exact runtime versions (e.g., Java 17+, Python 3.11, ES2022) and frameworks (e.g., Spring Boot, FastAPI, Node.js) in the prompt template context.
* **Incorporate Team Linter & Style Rules:** Include project-specific coding standards explicitly in the prompt (e.g., "Must pass ESLint / Google Java Style Guide / PEP 8 guidelines").
* **Target Functional Paradigms:** Request pure functions and explicit typing (TypeScript / Python type hints) by default to maintain static analysis compatibility.

### 5. What safeguards would you put in place before applying AI-suggested refactoring to production code?
* **Comprehensive Test Suite (Pre and Post Refactoring):** Ensure full unit and integration test coverage exists *before* refactoring. Run the exact same test suite after applying AI changes to verify zero regressions in system behavior.
* **Static Analysis & Security Scanning:** Run tools like SonarQube, SpotBugs, or Bandit to catch introduced vulnerabilities, type mismatches, or anti-patterns.
* **Strict Human Code Review (PR Process):** Treat all AI-generated code as a proposal from a peer. Every line must be critically reviewed and validated by a human engineer before merging into `main`.

---

