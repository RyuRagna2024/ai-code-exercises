# Task Manager CLI Frequently Asked Questions (FAQ)

## 1. Getting Started

### What is Task Manager CLI?
Task Manager CLI is a lightweight, command-line tool built with Node.js that lets developers create, organize, filter, and track tasks directly from their terminal.

### What are the prerequisites?
You need Node.js (v12 or higher) and `npm`. All required packages (`commander`, `uuid`) can be installed using `npm install`.

---

## 2. Usage & Functionality

### Where are my tasks saved?
Tasks are stored in a local file called `tasks.json` in the project root directory. This file is automatically created when you run your first command.

### How do priority levels work?
Priority is set on a scale from 1 to 4:
- `1`: LOW
- `2`: MEDIUM
- `3`: HIGH
- `4`: URGENT

### How do I mark a task as completed?
Run the status command with the task ID and `done`:
```bash
node cli.js status <task_id> done

3. Testing & Maintenance
How do I run the automated test suite?
Run npm test to execute all Jest test cases (including unit tests for tasks, storage, and integration tests).

How can I generate a test coverage report?
Run npx jest --coverage in your terminal to generate a detailed coverage breakdown.