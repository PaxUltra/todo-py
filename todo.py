import sys # For accepting command line arguments
import json

## Create/open task list JSON file, and read the contents
tasks_file = "tasks.json"
with open(tasks_file, "a+") as f:
    task_string = f.read() # Read the entire file into a variable as a string
    # Verify that the json file is not empty
    if task_string != "":
        tasks = json.loads(task_string) # Convert JSON string into a dict
    else:
        tasks = {} # If no task list exists, create an empty dict

print(tasks)

## Accept user command line arguments
args = sys.argv[1:] # sys.argv[0] is the script name. Arguments start at index 1
print("Arguments:", args)

## Add a task

## Update a task

## Delete a task

## List all tasks

## List all tasks that are done

## List all tasks that are not done

## List all tasks that are in progress