from Class_ToDo_List import ToDo_List
from datetime import date

def main():
    changed = False      # Flag to check if tasklist has been changed
    invalid_text = "WRONG input. Enter again"
    print()

    print("Welcome to the ToDo List application")
    print()
    print("Choose")
    print("1. If you want to import tasks from a file")
    print("2. If you want to create a new tasklist")

    # OPENING FILE TO IMPORT TASKS OR CREATING A NEW TASKLIST
    while True:
        file_choice = int(input())
        print()

        if file_choice == 1:    # Importing tasks from a file
            file = input("Enter the name of the file: ")
            print()

            print("Reading file... ")

            while True:
                try:
                    tasklist = ToDo_List.csv_to_tasks(file)
                    break
                except FileNotFoundError:
                    print("File does not exist. Enter again")
                    file = input("Enter the name of the file: ")
                    print()

            todo = ToDo_List(tasklist)
            print("Successfully read tasks from file!")
            print()

            print("Your tasks are:")
            print()
            print(todo.display_tasks())
            print()
            break
            
        elif file_choice == 2:      # Creating a new tasklist
            todo = ToDo_List()
            break
        else:       # Invalid choice
            print(invalid_text)



    # PERFORMING OPERATIONS ON THE TASKLIST
    while True:
        print("Choose from one of the following options:")
        print("1. Add a task")
        print("2. Remove a task")
        print("3. Modify a task")
        print("4. Check off a task")
        print("5. View tasks")
        print("6. Exit")
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

                print(todo.display_tasks())
                print()

                id = int(input("Enter the id of the task you want to remove: "))
                print()

                task_str = todo.remove_task(id)
                print("Task Removed! Details are:")

            elif choice == 3:       # Modifying a task
                if not todo.tasklist:   # If there are no tasks to modify
                    print("No tasks to modify")
                    print()
                    continue

                print("You choose to modify a task")
                print()

                print(todo.display_tasks())
                print()

                id = int(input("Enter the id of the task you want to modify: "))
                print()

                print("What do you want to modify?")
                print("1. title")
                print("2. due_date")
                print("3. due_time")

                while True:
                    modify = int(input())
                    print()

                    if modify == 1:     # title
                        attr = "title"
                        new = input("Enter new title: ")
                        break
                    elif modify == 2:       # due_date
                        attr = "due_date"
                        new = input("Enter new due date (in YYYY-MM-DD format): ")
                        break
                    elif modify == 3:       # due_time
                        attr = "due_time"
                        new = input("Enter new due time (in 24 hr HH:MM format). Else, leave blank: ")
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

                print(todo.display_tasks())
                print()

                id = int(input("Enter the id of the task you want to check off: "))
                print()

                task_str = todo.complete_task(id)
                print("Congratulations on finishing your task. Details are:")

            elif choice == 5:       # Viewing tasks
                print()
                print("What type of view do you prefer?")
                print()
                print("1. Sort by due_date")
                print("2. Sort by priority (high -> low)")
                print("3. Sort by priority (low -> high)")
                print("4. Sort by completed (completed -> not completed)")
                print("5. Sort by completed (not completed -> completed)")
                print("6. Sort by created_at (newest -> oldest)")
                print("7. Sort by created_at (oldest -> newest)")
                print()
                print("8. Filter completed tasks")
                print("9. Filter not completed tasks")
                print("10. Filter high priority tasks")
                print("11. Filter moderate priority tasks")
                print("12. Filter low priority tasks")
                print("13. Filter tasks to be completed by today")
                print("14. Filter pending tasks (due_date has crossed)")
                print()
                print("15. Just show me the tasks!")
                print()
                i = 1

                while i == 1:
                    view_choice = int(input("Enter your choice: "))
                    print()

                    # Sort Takss based on user choice
                    if view_choice == 1:
                        tasklist = todo.sort_tasks(["due_date", "due_time"], ascending=True)
                    elif view_choice == 2:
                        tasklist = todo.sort_tasks("priority", ascending=False)
                    elif view_choice == 3:
                        tasklist = todo.sort_tasks("priority", ascending=True)
                    elif view_choice == 4:
                        tasklist = todo.sort_tasks("completed", ascending=False)
                    elif view_choice == 5:
                        tasklist = todo.sort_tasks("completed", ascending=True)
                    elif view_choice == 6:
                        tasklist = todo.sort_tasks("created_at", ascending=False)
                    elif view_choice == 7:
                        tasklist = todo.sort_tasks("created_at", ascending=True)

                    # Filter Tasks based on user choice
                    elif view_choice == 8:
                        tasklist = todo.filter_tasks(attribute="completed", value=True)
                    elif view_choice == 9:
                        tasklist = todo.filter_tasks(attribute="completed", value=False)
                    elif view_choice == 10:
                        tasklist = todo.filter_tasks(attribute="priority", value="high")
                    elif view_choice == 11:
                        tasklist = todo.filter_tasks(attribute="priority", value="moderate")
                    elif view_choice == 12:
                        tasklist = todo.filter_tasks(attribute="priority", value="low")
                    elif view_choice == 13:
                        today = date.today()
                        tasklist = todo.filter_tasks(attribute="due_date", value=today)
                    elif view_choice == 14:
                        today = date.today()
                        tasklist = todo.filter_tasks(attribute="due_date", value=today, operator="<")

                    # Show Tasks without any sorting or filtering
                    elif view_choice == 15:
                        tasklist = todo.display_tasks()
                    else:
                        print(invalid_text)
                        i = 0
                    
                    i += 1

                print("Your tasks are:")
                print()
                print(tasklist)
                print()

            elif choice == 6:       # Exit
                if changed:
                    file = input("Enter the filename(csv) to which you want to save your tasks: ")
                    print()

                    print("Recording Tasks... ")
                    ToDo_List.tasks_to_csv(todo.tasklist, file)
                    print("Successfully recorded all tasks!")
                    print()

                print("Thanks for using the ToDo application. Have a nice day!")
                print()
                return

            else:       # Invalid Input
                print(invalid_text)
                break

            if choice in [1,2,3,4]:     # Printing task details for add, remove, modify, and complete operations
                print(task_str)
                changed = True      # tasklist has been updated so tasks have to be recorded to a file


            print("What's next on your mind?")
            print("1. Perform the same operation")
            print("2. Perform a different operation")
            print("3. Exit")

            while True:
                next_action = int(input())
                print()

                if next_action == 1:
                    same_op = True
                    break
                elif next_action == 2:
                    same_op = False
                    break
                elif next_action == 3:

                    if changed:     # If the tasklist has been changed
                        file = input("Enter the filename(csv) to which you want to save your tasks: ")
                        print()

                        print("Recording Tasks... ")
                        ToDo_List.tasks_to_csv(todo.tasklist, file)
                        print("Successfully recorded all tasks!")
                        print()

                    print("Thanks for using the ToDo application. Have a nice day!")
                    print()
                    return
                else:
                    print(invalid_text)

            if not same_op:
                break

if __name__ == "__main__":
    main()

    

        
