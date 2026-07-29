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