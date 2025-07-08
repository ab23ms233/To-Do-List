from Class_ToDo_List import ToDo_List
import pandas as pd

def main():
    invalid_text = "WRONG input. Enter again"
    print()

    print("Welcome to the ToDo List application")
    print()
    print("Choose")
    print("1. If you want to import tasks from a file")
    print("2. If you want to create a new tasklist")
    file_choice = int(input())
    print()

    if file_choice == 1:
        file = input("Enter the name of the file: ")
        df = pd.read_csv(file)

        if df.empty:
            print("The file is empty. Initialising empty tasklist... ")
            todo = ToDo_List()
        else:
            df["completed"] = df["completed"].astype(bool)
            df["due_date"] = pd.to_datetime(df["due_date"]).dt.date
            df["due_time"] = df["due_time"].replace('NA', pd.NA)
            df["due_time"] = pd.to_datetime(df["due_time"], format="%H:%M", errors='coerce').dt.time

            tasklist = df.to_dict(orient="records")
            todo = ToDo_List(tasklist)
    
    elif file_choice == 2:
        todo = ToDo_List()

    while True:
        print("Choose from one of the following options:")
        print("1. Add a task")
        print("2. Remove a task")
        print("3. Modify a task")
        print("4. Check off a task")
        print("5. View all tasks")
        print()
        choice = int(input("Enter your choice: "))

        while True:
            if choice == 1:     # Adding a task
                print("You choose to add a task")
                print()

                task = todo.input_task()
                print()

                task_str = todo.add_task(task)
                print("Task Added! Details are:")

            elif choice == 2:      # Removing a task
                if not todo.tasklist:   # If there are no tasks to remove
                    print("No tasks to remove")
                    print()
                    continue

                print("You choose to remove a task")
                print()

                todo.display_tasks()
                print()

                id = int(input("Enter the id of the task you want to remove: "))
                print()

                task_str = todo.remove_task(id)
                print("Task Removed! Details are:")

            elif choice == 3:   # Modifying a task
                if not todo.tasklist:   # If there are no tasks to modify
                    print("No tasks to modify")
                    print()
                    continue

                print("You choose to modify a task")
                print()

                todo.display_tasks()
                print()

                id = int(input("Enter the id of the task you want to modify: "))
                print()

                print("What do you want to modify?")
                print("1. title")
                print("2. due_date")
                print("3. due_time")

                while True:
                    modify = int(input())

                    if modify == 1:
                        attr = "title"
                        new = input("Enter new title: ")
                        break
                    elif modify == 2:
                        attr = "due_date"
                        new = input("Enter new due date (in YYYY-MM-DD format): ")
                        break
                    elif modify == 3:
                        attr = "due_time"
                        new = input("Enter new due time (in 24 hr HH:MM format): ")
                        break
                    else:
                        print(invalid_text)

                task_str = todo.modify_task(id, attr, new)
                print()
                print("Task Modified! Details are:")

            elif choice == 4:       # Checking off a task
                if not todo.tasklist:   # If there are no tasks to check off
                    print("No tasks to check off")
                    print()
                    continue

                print("You choose to tick off a task")
                print()

                todo.display_tasks()
                print()

                id = int(input("Enter the id of the task you want to check off: "))
                print()

                task_str = todo.complete_task(id)
                print("Congratulations on finishing your task. Details are:")

            elif choice == 5:       # Viewing all tasks
                print("Your tasks are:")
                print()
                todo.display_tasks()
                print()

            if choice in [1,2,3,4]:  # Printing task details for add, remove, modify, and complete operations
                print(task_str)

            print("What's next on your mind?")
            print("1. Perform the same operation")
            print("2. Perform a different operation")
            print("3. Exit")

            while True:
                next = int(input())
                print()

                if next == 1:
                    same_op = True
                    break
                elif next == 2:
                    same_op = False
                    break
                elif next == 3:
                    if file_choice == 2:
                        file = input("Enter the filename(csv) to which you want to save your tasks: ")
                        print()

                        print("Recording Tasks... ")
                        df = pd.DataFrame(todo.tasklist)
                        df.to_csv(file, index=False)

                    print("Thanks for using the ToDo application. Have a nice day!")
                    print()
                    return
                else:
                    print(invalid_text)

            if not same_op:
                break

if __name__ == "__main__":
    main()

    

        
