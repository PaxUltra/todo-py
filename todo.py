import sys # For accepting command line arguments
import json
from datetime import datetime

## Constants
TASKS_FILE = "tasks.json"

## Helper functions
def update_json_file(task_data):
    with open(TASKS_FILE, "w") as f:
        json_string = json.dumps(task_data, indent=4) # Convert in memory dict to JSON string
        f.write(json_string)

def print_task_list(task_list):
    for task in task_list:
            print()
            print(f'ID: {task["id"]}')
            print(f'Name: {task["name"]}')
            print(f'Description: {task["description"]}')
            print(f'Status: {task["status"]}')
            print(f'Created At: {task["created_at"]}')
            print(f'Updated At: {task["updated_at"]}')

def find_task_by_id(id, task_data):
    return next((t for t in task_data.get("tasks", []) if str(t["id"]) == str(id)), None)

def current_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

## Commands

# Add a task
def add(args, task_data):
    # If the command is add, the name will be the second argument
    # If no name is provided, stop execution
    name = args[1] if len(args) > 1 else None
    if not name:
        print("Name is a required argument to add a task.")
        return
    
    description = args[2] if len(args) >= 3 else "" # Third argument should be description 
    id = task_data.get("next_id", 1)
    new_task = {
        "id": id,
        "name": name,
        "description": description,
        "status": "todo",
        "created_at": current_timestamp(),
        "updated_at": current_timestamp()
    }

    # Update next ID, and the task list in memory
    task_data["next_id"] = task_data["next_id"] + 1
    task_data["tasks"].append(new_task)

    # Write changes to JSON file
    update_json_file(task_data)

    print(f"\nTask added successfully (ID: {id})")

    return

# List tasks
def list_tasks(args, task_data):
    valid_statuses = {"todo", "done", "in-progress"}
    status_filter = args[1] if len(args) > 1 else None

    # If no arguments are provided, list all tasks
    if status_filter is None:
        print_task_list(task_data["tasks"])
    elif status_filter in valid_statuses:
        filtered_tasks = [task for task in task_data["tasks"] if task["status"] == status_filter]
        print_task_list(filtered_tasks)
    else:
        print("\nStatus must be either todo, done, or in-progress.")

    return

# Update task description
def update(args, task_data):
    # Verify that ID and description arguments are present and valid
    task_id = args[1] if len(args) > 1 else None
    new_description = args[2] if len(args) > 2 else None

    if not task_id or not new_description:
        print("\nTask ID and new description are required arguments.")
        return
    elif not task_id.isdigit():
        print("\nTask ID must be an integer.")
        return
    
    # Find the task with the matching ID
    # Return None if no value is found
    task = find_task_by_id(args[1], task_data)

    if task:
        task["description"] = args[2]
        task["updated_at"] = current_timestamp()
        update_json_file(task_data)
        print(f"\nUpdated task ID {args[1]}.")
    else:
        print("\nTask ID not found.")
    
    return

# Mark task as in-progress
def mark_in_progress(args, task_data):
    # Task ID is required
    task_id = args[1] if len(args) > 1 else None
    if not task_id:
        print("\nTask ID is a required argument.")
        return
    
    # Find the task with the matching ID
    # Return None if no value is found
    task = find_task_by_id(args[1], task_data)

    if task:
        task["status"] = "in-progress"
        task["updated_at"] = current_timestamp()
        update_json_file(task_data)
        print(f"\nTask ID {args[1]} set to in-progress.")
    else:
        print("\nTask ID not found.")

    return

# Mark task as done
def mark_done(args, task_data):
    # Task ID is required
    task_id = args[1] if len(args) > 1 else None
    if not task_id:
        print("\nTask ID is a required argument.")
        return
    
    # Find the task with the matching ID
    # Return None if no value is found
    task = find_task_by_id(args[1], task_data)

    if task:
        task["status"] = "done"
        task["updated_at"] = current_timestamp()
        update_json_file(task_data)
        print(f"\nTask ID {args[1]} set to done.")
    else:
        print("\nTask ID not found.")

    return

# Delete task
def delete(args, task_data):
    # Task ID is required
    task_id = args[1] if len(args) > 1 else None
    if not task_id:
        print("\nTask ID is a required argument.")
        return
    
    # Find the task with the matching ID
    # Return None if no value is found
    task = find_task_by_id(args[1], task_data)

    if task:
        task_data["tasks"].remove(task) # Delete the entry
        update_json_file(task_data)
        print(f"\nTask ID {args[1]} deleted.")
    else:
        print("\nTask ID not found.")

    return

commands = {
    "add": add,
    "list": list_tasks,
    "update": update,
    "mark-in-progress": mark_in_progress,
    "mark-done": mark_done,
    "delete": delete
}

## Create/open task list JSON file, and read the contents
try:
    with open(TASKS_FILE, "r") as f:
        # Read the entire file into a variable as a string
        task_string = f.read().strip()
        # Verify that the json file is not empty, and reset it if it is
        task_data = json.loads(task_string) if task_string else {"next_id": 1, "tasks": []}
except FileNotFoundError:
    task_data = {"next_id": 1, "tasks": []}
    update_json_file(task_data)

## Accept user command line arguments
args = sys.argv[1:] # sys.argv[0] is the script name. Arguments start at index 1
command = args[0] if args else None # The command will always be the first argument

# Make sure the command exists
if not command or command not in commands:
    print("\nError: Command not found.")
else:
    commands[command](args, task_data)