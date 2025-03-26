# todo-py
Simple Python CLI to-do list manager.

## Requirements
- Python 3.6+

## Installation

1. Clone the repository wherever you want it to live
```bash
git clone https://github.com/PaxUltra/todo-py.git
```
2. Change directory into the `todo-py` directory
```bash
cd todo-py
```
## Usage

The script works via passing command line arguments to the `todo.py` file.

```bash
python todo.py <command>
```
The todo list is saved in `tasks.json` inside the same directory as `todo.py`.

### Supported Commands

#### Add

Adds a task to the todo list.

```bash
python todo.py add name [description]
```

#### List

Lists tasks in the todo list. A filter option can be passed to limit results based on the status of the task.

```bash
python todo.py list task-id ["todo" | "done" | "in-progress"]
```

#### Update

Change the description of a task.

```bash
python todo.py update task-id new-description
```

#### Mark Task as In-Progress

Change the status of a task to in-progress.

```bash
python todo.py mark-in-progress task-id
```

#### Mark Task as Done

Change the status of a task to done.

```bash
python todo.py mark-done task-id
```

#### Delete

Delete a task.

```bash
python todo.py delete task-id
```

To clear the to-do list, simply delete `tasks.json`.

### Testing

To run the provided tests, execute:
```bash
python -m unittest test_todo.py
```