"""SaiKet Systems Internship Task 1:To-Do List Application
Description:
Build a to-do list application where users can
add tasks, mark them as completed, and
view their tasks. Utilize dictionaries or
classes to represent tasks, including
attributes like description and completion
status. Implement user-friendly interfaces
for task management."""

class Task:
    def __init__(self, description):
        self.description = description
        self.completed = False

    def mark_completed(self):
        self.completed = True


class TodoList:
    def __init__(self):
        self.tasks = []

    def add_task(self, description):
        task = Task(description)
        self.tasks.append(task)
        print("Task added successfully.")

    def view_tasks(self):
        if not self.tasks:
            print("No tasks available.")
            return

        for index, task in enumerate(self.tasks):
            status = "✔" if task.completed else "✘"
            print(f"{index + 1}. {task.description} [{status}]")

    def mark_task_completed(self, index):
        if 0 <= index < len(self.tasks):
            self.tasks[index].mark_completed()
            print("Task marked as completed.")
        else:
            print("Invalid task number.")


def main():
    todo = TodoList()

    while True:
        print("\n--- TO-DO LIST MENU ---")
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Mark Task Completed")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            desc = input("Enter task description: ")
            todo.add_task(desc)

        elif choice == '2':
            todo.view_tasks()

        elif choice == '3':
            todo.view_tasks()
            try:
                num = int(input("Enter task number: ")) - 1
                todo.mark_task_completed(num)
            except ValueError:
                print("Please enter a valid number.")

        elif choice == '4':
            print("Exiting... Goodbye!")
            break

        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()