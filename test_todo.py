import unittest
from todo import add, update, mark_in_progress, mark_done, delete

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
        # Valid arguments
        args_add = ["add", "Task to Update", "Old Description"]
        add(args_add, self.task_data)

        task_id = str(self.task_data["tasks"][0]["id"])
        args_update = ["update", task_id, "New Description"]
        update(args_update, self.task_data)

        self.assertEqual(self.task_data["tasks"][0]["description"], "New Description")

        # When a non-existent ID is provided, the task list should not change
        initial_data = self.task_data
        invalid_id = "999"
        args_invalid_id = ["update", invalid_id, "Another Description"]
        update(args_invalid_id, self.task_data)
        self.assertEqual(self.task_data, initial_data)

        # When a non-int ID is provided, the task list should not change
        invalid_id = "dog"
        args_invalid_id = ["update", invalid_id, "Another Description"]
        update(args_invalid_id, self.task_data)
        self.assertEqual(self.task_data, initial_data)

        invalid_id = "3.14"
        args_invalid_id = ["update", invalid_id, "Another Description"]
        update(args_invalid_id, self.task_data)
        self.assertEqual(self.task_data, initial_data)

        # When arguments are missing, the task list should not change
        args_no_id = ["update"]
        update(args_no_id, self.task_data)
        self.assertEqual(self.task_data, initial_data)

        args_no_desc = ["update", "1"]
        update(args_no_id, self.task_data)
        self.assertEqual(self.task_data, initial_data)

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

if __name__ == '__main__':
    unittest.main()