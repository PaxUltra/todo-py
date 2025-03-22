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

## Commands

# Add a task
def add(args, task_data):
    # If the command is add, the name will be the second argument
    # If no name is provided, stop execution
    try:
        name = args[1]
    except IndexError:
        print("Name is a required argument to add a task.")
        return
    
    description = args[2] if len(args) >= 3 else "" # Third argument should be description 
    id = task_data["next_id"]
    now = datetime.now() # Current date/time
    timestamp_str = now.strftime("%Y-%m-%d %H:%M:%S") # YYYY-MM-DD HH:MM:SS
    new_task = {
        "id": id,
        "name": name,
        "description": description,
        "status": "todo",
        "created_at": timestamp_str,
        "updated_at": timestamp_str
    }

    # Update next ID, and the task list in memory
    task_data["next_id"] = task_data["next_id"] + 1
    task_data["tasks"].append(new_task)

    # Write changes to JSON file
    update_json_file(task_data)

    print(f"\nTask added successfully (ID: {id})")

    return

# List tasks
def list(args, task_data):
    # If no arguments are provided, list all tasks
    if len(args) < 2:
        print_task_list(task_data["tasks"])
    elif args[1] == "todo":
        # Filter todo tasks
        filtered_tasks = [task for task in task_data["tasks"] if task["status"] == "todo"]
        print_task_list(filtered_tasks)
    elif args[1] == "done":
        # Filter done tasks
        filtered_tasks = [task for task in task_data["tasks"] if task["status"] == "done"]
        print_task_list(filtered_tasks)
    elif args[1] == "in-progress":
        # Filter in-progress tasks
        filtered_tasks = [task for task in task_data["tasks"] if task["status"] == "in-progress"]
        print_task_list(filtered_tasks)
    else:
        print("\nStatus must be either todo, done, or in-progress.")

    return

# Update task description
def update(args, task_data):
    # Verify that ID and description arguments are present and valid
    if len(args) < 3:
        print("\nTask ID and new description are required arguments.")
        return
    elif not (args[1]).isdigit():
        print("\nTask ID must be an integer.")
        return
    
    # Find the task with the matching ID
    # Return None if no value is found
    task = next((t for t in task_data["tasks"] if t["id"] == int(args[1])), None)

    if task:
        task["description"] = args[2]
        update_json_file(task_data)
        print(f"\nUpdated task ID {args[1]}.")
    else:
        print("\nTask ID not found.")
    
    return

# Mark task as in-progress
def markInProgress(args, task_data):
    # Task ID is required
    if len(args) < 2:
        print("\nTask ID is a required argument.")
        return
    
    # Find the task with the matching ID
    # Return None if no value is found
    task = next((t for t in task_data["tasks"] if t["id"] == int(args[1])), None)

    if task:
        task["status"] = "in-progress"
        update_json_file(task_data)
        print(f"\nTask ID {args[1]} set to in-progress.")
    else:
        print("\nTask ID not found.")

    return

commands = {
    "add": add,
    "list": list,
    "update": update,
    "mark-in-progress": markInProgress
}

## Create/open task list JSON file, and read the contents
try:
    with open(TASKS_FILE, "r") as f:
        task_string = f.read() # Read the entire file into a variable as a string
        # Verify that the json file is not empty
        if task_string != "":
            task_data = json.loads(task_string) # Convert JSON string into a dict
        else:
            task_data = {
                "next_id": 1, # Reset the next ID
                "tasks": [] # If no task list exists, create an empty list
            }
except FileNotFoundError:
    with open(TASKS_FILE, "w"):
        task_data = {
                "next_id": 1, # Reset the next ID
                "tasks": [] # If no task list exists, create an empty list
            }
        update_json_file(task_data)

## Accept user command line arguments
args = sys.argv[1:] # sys.argv[0] is the script name. Arguments start at index 1
command = args[0] # The command will always be the first argument

# Make sure the command exists
if command in commands:
    commands[command](args, task_data)
else:
    print("Error: Command not found.")

## Delete a task