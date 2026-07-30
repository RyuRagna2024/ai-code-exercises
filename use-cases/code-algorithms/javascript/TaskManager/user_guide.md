# Step-by-Step Guide: Creating and Managing Tasks in Task Manager CLI

**Target Audience:** Beginners / Terminal Users  
**Objective:** Learn how to create, update, filter, and track tasks using the Task Manager CLI.

---

## Prerequisites

Before starting, make sure you have:
1. Node.js (v12 or higher) installed on your system.
2. The repository dependencies installed by running `npm install` inside the project folder.

---

## Step 1: Create Your First Task

1. Open your terminal in the project directory.
2. Run the `create` command with a title, priority, due date, and tags:

```bash
node cli.js create "Complete Project Documentation" -d "Write README, user guide, and FAQ" -p 3 -u 2026-12-31 -t "work,important"

1. Note down the ID generated in the console output (e.g., abc123). You will need this ID for future updates.

Step 2: View and Filter Tasks
1. To view all tasks, run:

   node cli.js list

1. To filter for only high priority tasks (priority 3):

   node cli.js list -p 3

1. To check for any overdue tasks:

   node cli.js list -o

Step 3: Update Task Status and Details
1. Change a task status to in_progress or done:

   node cli.js status abc123 in_progress

1. Add a new tag to the task:

   node cli.js tag abc123 urgent

1. Inspect full details of the updated task:

   node cli.js show abc123

Step 4: Check Productivity Statistics
Run the stats command to generate an overview of your progress:

   node cli.js stats

You will see counts of total tasks, breakdowns by status and priority, and tasks completed in the last 7 days.

Troubleshooting
"Command Not Found" or Execution Error
- Make sure you are in the correct root directory where cli.js lives.
- Ensure you run commands using node cli.js or make it executable with chmod +x cli.js.

Cannot Find Created Tasks
- Check that tasks.json has been created in the project root folder. Do not manually edit or delete tasks.json while running commands.