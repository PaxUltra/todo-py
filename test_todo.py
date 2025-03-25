import unittest
from todo import add, update, mark_in_progress, mark_done, delete, list_tasks

class TestTodoFunctions(unittest.TestCase):
    def setUp(self):
        # Runs before each test.
        self.task_data = {"next_id": 1, "tasks": []}

    def test_add_task(self):
        # If a task name is not provided, task_data should not grow
        args = ["add"]
        add(args, self.task_data)
        self.assertEqual(len(self.task_data["tasks"]), 0)

        # Add a full task
        args = ["add", "Test Task", "This is a test."]
        add(args, self.task_data)
        self.assertEqual(len(self.task_data["tasks"]), 1)
        self.assertEqual(self.task_data["tasks"][0]["name"], "Test Task")
        self.assertEqual(self.task_data["tasks"][0]["description"], "This is a test.")
        self.assertEqual(self.task_data["tasks"][0]["status"], "todo")

        # Add task without description
        args = ["add", "Test Task 2"]
        add(args, self.task_data)
        self.assertEqual(len(self.task_data["tasks"]), 2)
        self.assertEqual(self.task_data["tasks"][1]["name"], "Test Task 2")
        self.assertEqual(self.task_data["tasks"][1]["description"], "")
        self.assertEqual(self.task_data["tasks"][1]["status"], "todo")

    def test_update_task(self):
        args_add = ["add", "Task to Update", "Old Description"]
        add(args_add, self.task_data)

        task_id = str(self.task_data["tasks"][0]["id"])
        args_update = ["update", task_id, "New Description"]
        update(args_update, self.task_data)

        self.assertEqual(self.task_data["tasks"][0]["description"], "New Description")

    def test_mark_in_progress(self):
        args_add = ["add", "Task to Progress"]
        add(args_add, self.task_data)
        
        task_id = str(self.task_data["tasks"][0]["id"])
        args_mark = ["mark-in-progress", task_id]
        mark_in_progress(args_mark, self.task_data)

        self.assertEqual(self.task_data["tasks"][0]["status"], "in-progress")

    def test_mark_done(self):
        args_add = ["add", "Task to Complete"]
        add(args_add, self.task_data)
        
        task_id = str(self.task_data["tasks"][0]["id"])
        args_mark = ["mark-done", task_id]
        mark_done(args_mark, self.task_data)

        self.assertEqual(self.task_data["tasks"][0]["status"], "done")

    def test_delete_task(self):
        args_add = ["add", "Task to Delete"]
        add(args_add, self.task_data)
        
        task_id = str(self.task_data["tasks"][0]["id"])
        args_delete = ["delete", task_id]
        delete(args_delete, self.task_data)

        self.assertEqual(len(self.task_data["tasks"]), 0)

    def test_list_todo_tasks(self):
        add(["add", "Task 1", "Desc 1"], self.task_data)
        add(["add", "Task 2", "Desc 2"], self.task_data)
        mark_done(["mark-done", "1"], self.task_data)  # Mark first task as done

        filtered_tasks = [t for t in self.task_data["tasks"] if t["status"] == "todo"]
        self.assertEqual(len(filtered_tasks), 1)

if __name__ == '__main__':
    unittest.main()