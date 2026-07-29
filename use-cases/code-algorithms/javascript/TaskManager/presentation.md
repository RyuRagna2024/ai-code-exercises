# Exercise Series 2: Codebase Exploration Challenge

## Exercise Part 4: Presentation & Reflection Script

**Format:** Written Presentation / Speaker Script  
**Target Duration:** 3–5 Minutes  
**Topic:** Navigating and Mapping the Node.js CLI TaskManager Architecture  

---

## Slide / Section 1: High-Level Architecture Overview (~1 minute)
* **Script / Speaker Notes:**
  > "Hello everyone. Today I’m presenting a walkthrough of our Command Line Interface (CLI) TaskManager application built with Node.js and CommonJS modules.
  > 
  > Architecturally, this application follows a strict four-layer pipeline operating in a short-lived process context:
  > 1. **Interface Layer (`cli.js`):** Built with the Commander library, this layer parses terminal commands and user arguments.
  > 2. **Application Logic Layer (`app.js`):** Orchestrated by `TaskManager`, this manages feature coordination, input validation, and business workflow logic.
  > 3. **Domain Model Layer (`models.js`):** Encapsulates the core `Task` entity, defining state transitions, priority levels, and timestamp rules using the `uuid` package for unique identification.
  > 4. **Persistence Layer (`storage.js`):** A custom `TaskStorage` repository that reads from and writes synchronously to a local `tasks.json` file.
  > 
  > Every CLI command execution spins up a new process, reads the disk state into an in-memory hash map, performs operations, and writes the entire updated state back to disk."

---

## Slide / Section 2: How the Three Key Features Work (~1.5 minutes)
* **Script / Speaker Notes:**
  > "Let's examine the data flow across our three core features:
  > 
  > 1. **Task Creation (`create` command):**
  >    - **Flow:** User inputs title, priority, due date, and tags $\rightarrow$ `cli.js` passes these to `TaskManager.createTask()` $\rightarrow$ A new `Task` instance is instantiated in `models.js` generating a UUID and setting status to `'todo'` $\rightarrow$ `TaskStorage.addTask()` inserts it into the in-memory dictionary and calls `save()`, stringifying the array back to `tasks.json`.
  > 
  > 2. **Task Prioritization (`priority` command):**
  >    - **Flow:** User inputs a task ID and numerical priority (1–4) $\rightarrow$ `cli.js` routes to `TaskManager.updateTaskPriority()` $\rightarrow$ Calls `TaskStorage.updateTask()` $\rightarrow$ Invokes `task.update({ priority })` on the domain model, updating `updatedAt` $\rightarrow$ `save()` flushes the updated dictionary back to `tasks.json`.
  > 
  > 3. **Task Completion (`status <id> done` command):**
  >    - **Flow:** User inputs task ID and status `'done'` $\rightarrow$ `TaskManager.updateTaskStatus()` recognizes the `'done'` state transition $\rightarrow$ Calls domain method `task.markAsDone()`, which sets `status = 'done'`, records `completedAt = new Date()`, and updates `updatedAt` $\rightarrow$ `TaskStorage.save()` persists the state to disk."

---

## Slide / Section 3: Key Design Pattern Discovered (~1 minute)
* **Script / Speaker Notes:**
  > "One interesting design approach I discovered in this architecture is the **In-Memory Active Repository / Data Mapper hybrid pattern**.
  > 
  > Rather than querying disk for individual items, `TaskStorage.load()` reads all JSON data on application start and re-hydrates plain JSON objects into full JavaScript `Task` class instances with active methods (like `markAsDone()` and `isOverdue()`). 
  > 
  > While this makes in-memory operations extremely fast, it creates a crucial distinction between **transient state** (RAM state active during the single command run) and **durable persistent state** (JSON bytes saved on disk)."

---

## Slide / Section 4: Reflections & Challenges (~1 minute)
* **Script / Speaker Notes:**
  > "The most challenging part of this exercise was tracing where state changes actually become permanent versus where they exist only in memory. 
  > 
  > For instance, I discovered that `storage.js` catches filesystem errors in a `try/catch` block without re-throwing them or returning a success boolean. This means `app.js` could report a successful status update to the user even if `fs.writeFileSync` failed silently on disk!
  > 
  > Using structured AI prompting helped me break this down into a clear pipeline: *Input $\rightarrow$ Command Parsing $\rightarrow$ Task Lookup $\rightarrow$ Domain Mutation $\rightarrow$ Disk Persistence*. If I were to refactor this application in the future, I would replace the silent error handling with explicit return booleans or custom exceptions, and consider a purely functional Read-Transform-Write pipeline suited for CLI runtimes."