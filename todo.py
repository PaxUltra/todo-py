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

## Commands
def add(args, task_data):
    name = args[1] # If the command is add, the name will be the second argument
    description = args[2] # Third argument should be description 
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

commands = {
    "add": add
}

## Create/open task list JSON file, and read the contents
with open(TASKS_FILE, "a+") as f:
    task_string = f.read() # Read the entire file into a variable as a string
    # Verify that the json file is not empty
    if task_string != "":
        task_data = json.loads(task_string) # Convert JSON string into a dict
    else:
        task_data = {
            "next_id": 1, # Reset the next ID
            "tasks": [] # If no task list exists, create an empty list
        }

## Accept user command line arguments
args = sys.argv[1:] # sys.argv[0] is the script name. Arguments start at index 1
command = args[0] # The command will always be the first argument

# Make sure the command exists
if command in commands:
    commands[command](args, task_data)
else:
    print("Error: Command not found.")

## Add a task

## Update a task

## Delete a task

## List all tasks

## List all tasks that are done

## List all tasks that are not done

## List all tasks that are in progress