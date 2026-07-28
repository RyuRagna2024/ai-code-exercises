# Task Manager Application: Project Findings & Structure

 

1. Initial Understanding & Assumptions

Before running the AI analysis, my initial observations were:

- Application Purpose: A Task Manager application to create, organize, and manage to-do lists.
- Technology Stack: Built using JavaScript and Node.js (identified via `package.json` and `.js` file extensions).
- Codebase Structure: A flat root folder structure where all core JavaScript logic sits alongside a dedicated `tests/` directory.

 

1. AI Analysis vs. Initial Assumptions (Misconceptions Corrected)

Running the project structure prompt revealed key clarifications regarding how the application actually works:

- CLI vs. Web App: I originally thought this might be a backend or general application, but it is specifically a Command Line Interface (CLI) application. It runs purely in the terminal `node cli.js`) and has no front-end web UI or database server.
- Actual Entry Point: I assumed `app.js` was the main entry point due to its name. However, `cli.js` is the true entry point where user commands enter the application. `app.js` holds the internal business logic `TaskManager`).
- Data Storage: Data is persisted directly to a local file called `tasks.json` managed via `storage.js`, rather than a traditional database.
- Stand-alone / Modular Utilities: Three files `task_parser.js`, `task_priority.js`, and `task_list_merge.js`) have active test suites but are not yet imported into `cli.js` or `app.js`. They act as modular building blocks for future features (like shorthand text parsing or syncing).

 

1. Technology Stack & Key Libraries
  echnology / Library  Role & Purpose 
  ode.js  Runtime environment that executes the JavaScript code outside a browser. 
  avaScript (CommonJS)  Primary language using standard `require()` and `module.exports` syntax. 
  commander  `External library used in` cli.js`to parse terminal commands and flags.  uuid` Library in `models.js` used to generate unique IDs for tasks. 
  Jest  `Test runner used in the` tests/`directory to run automated unit and integration tests.  ode.js`fs`Module  Built-in module used in`storage.js` to read and write task data to disk.
  1. Key Components & Responsibilities (Architectural Pattern)

The application follows a simple 4-layer flow when processing a command:

1. `cli.js` (Front Desk / Interface):
  - Receives user commands in the terminal (e.g., `node cli.js create`) and parses flags. Passes instructions to `app.js`.
2. `app.js` (Business Logic Manager):
  - Contains the `TaskManager` class. Coordinates creating, listing, updating, and deleting tasks.
3. `models.js` (Domain Models):
  - Defines what a "Task" object is (title, priority, status, dates, unique ID).
4. `storage.js` (Data Storage / Persistence):
  - Acts as the filing cabinet, handling reading from and writing to `tasks.json`.
  1. Important Entry Points

- CLI Application: `node cli.js [command]` (Primary entry point for users).
- Automated Test Suite: `npm test` (Runs Jest against the `tests/` directory).

1. Unused Modules: Are `task_parser.js`, `task_priority.js`, and `task_list_merge.js` planned to be integrated into `cli.js`, or are they standalone exercise modules?
2. Storage Roadmap: Is local JSON file storage `tasks.json`) the long-term solution, or are there plans to migrate to a database?
3. Testing Workflow: What is the expected development workflow when adding a feature—should we write Jest tests first, or update `cli.js` first?
  *Exercise Part 2: Finding Feature Implementation (Task Export to CSV)**
  *
  1. Initial Search & Approach Evaluation**

*** Search Terms Used:** `storage`**,** `writeFile`**,** `JSON`**,** `task`**.**

*** Files Checked:** `storage.js`**,** `app.js`**,** `cli.js`**.**

*** Evaluation: Searching for file interaction terms** `writeFile`**,** `JSON`**) led directly to** `storage.js`**. Because all files sit in the root directory, feature implementation relies on identifying which module handles each stage of data flow rather than navigating complex directory structures.**

 **2. Feature Location & Affected Components**

**To add a "Task Export to CSV" feature, changes are divided across three key files:**

**1.** `cli.js` **(User Interface / Entry Point):**

   *** Needs a new command definition (e.g.,** `.command('export <filename>')`**) using the** `commander` **library to capture the user's terminal input.**

**2.** `app.js` **(Business Logic /** `TaskManager` **Class):**

   *** Needs a new method (e.g.,** `exportTasksToCSV(filePath)`**) that fetches current tasks and directs the storage layer to export them.**

**3.** `storage.js` **(Data Handling & File I/O):**

   *** Needs the core CSV formatting and file-writing logic (e.g., converting task objects to comma-separated strings and writing them to disk using Node's** `fs` **module).**

**3. Investigation Process & Data Flow**

**The complete flow for this feature follows this path:**

User Terminal Command ➔ cli.js (Parses args) ➔ app.js (Business Logic) ➔ storage.js (Generates CSV & Writes File)

1. Self-Assessment Questions & Navigation Patterns

When exploring or validating feature locations in this codebase: 

- Where does user input enter?* Look for command registrations in `cli.js`. 
- Where does domain logic live?* Look for method definitions inside the `TaskManager` class in `app.js`. 
- Where do side effects (file reads/writes) happen?* Look for `fs` module calls in `storage.js`.

 

1. Step 1: Create a helper method in `storage.js` to convert JSON tasks into CSV format and save them using `fs.writeFileSync`.
2. Step 2: Add an `exportTasks` method to `TaskManager` in `app.js`.
3. Step 3: Register the `export` command in `cli.js`.
4. Step 4: Add unit tests in `tests/taskStorage.test.js` to test CSV output.



Exercise Part 3: Understanding Domain Models & Business Concepts



 1. Core Domain Entities & Glossary

* Task: The central entity representing a single work item `id`, `title`, `description`, `status`, `priority`, `dueDate`, `tags`, `timestamps`).

* TaskStatus: Registry of workflow stages `TODO`, `IN_PROGRESS`, `REVIEW`, `DONE`). Uses strings `'todo'`, `'in_progress'`) for human readability.

* TaskPriority: Registry of urgency levels `LOW: 1`, `MEDIUM: 2`, `HIGH: 3`, `URGENT: 4`). Uses numbers so tasks can be sorted numerically by urgency.

* Audit Timestamps:

  * `createdAt`: Set once when created.

  * `updatedAt`: Refreshed on every modification.

  * `dueDate`: Optional target deadline.

  * `completedAt`: Set exclusively when marked `DONE`.



2. Domain Model Relationship Diagram



┌─────────────────────────────────┐ │ TASK │ │ id, title, description, tags │ └───────────────┬─────────────────┘ │ ┌─────────────────────────┼─────────────────────────┐ │ │ │ ▼ ▼ ▼



┌──────────────┐ ┌──────────────┐ ┌──────────────┐ │ WORKFLOW │ │ IMPORTANCE │ │ TIME │ │ TaskStatus │ │ TaskPriority │ │ │ │ todo │ │ 1 LOW │ │ createdAt │ │ in_progress │ │ 2 MEDIUM │ │ updatedAt │ │ review │ │ 3 HIGH │ │ dueDate │ │ done │ │ 4 URGENT │ │ completedAt │ └──────────────┘ └──────────────┘ └──────────────┘



3. Answers to Domain Model Assessment Questions 

1. Which task shows up in `node cli.js list -o` (Overdue)? 

* Only the first task (due yesterday, `IN_PROGRESS`) shows up. Overdue status relies strictly on: `dueDate < now` AND `status !== DONE`. Priority does not affect whether a task is overdue. 

2. What happens when a task is completed early? Is it overdue after completion? 

* No, a completed task is never overdue `status === DONE` overrides overdue calculations). 

* Marking `DONE` calls `markAsDone()`, updating both `updatedAt` and `completedAt`. Changing status to `IN_PROGRESS` only updates `status` and `updatedAt` (leaving `completedAt` as `null`). 

3. Why use numbers for priority and strings for status? 

* Priority (Numbers 1-4): Allows mathematical comparison and sorting (e.g., `a.priority > b.priority` to show urgent tasks first). 

* Status (Strings): Makes terminal outputs and JSON files easily human-readable without requiring a lookup key. 

4. When priority changes from MEDIUM to URGENT on a task in review: 

* Domain state changed: `priority` (2 -> 4) and `updatedAt` timestamp. 

* Unchanged: `status` remains `REVIEW`, `createdAt`, `dueDate`, and `completedAt` remain untouched. Workflow and urgency are independent dimensions. 

5. Impact of adding a "snoozed" status: 

* `isOverdue()` rule: Needs evaluation (should snoozed tasks trigger overdue alerts?). 

* `stats` command: Needs updating to count/display snoozed items. 

* CLI & Merge logic: `cli.js` options and `task_list_merge.js` conflicts need rules for handling snoozed tasks.