from Class_ToDo_List import ToDo_List
from datetime import date
from colorama import Fore, init

def main():
    init(autoreset=True)  # Initialize colorama to reset colors after each print
    changed = False      # Flag to check if tasklist has been changed
    invalid_text = Fore.RED + "WRONG input. Enter again"
    print()

    print(Fore.YELLOW + "Welcome to the ToDo List application")
    print()
    print("Choose")
    print("1. If you want to import tasks from a file")
    print("2. If you want to create a new tasklist")

    # OPENING FILE TO IMPORT TASKS OR CREATING A NEW TASKLIST
    while True:
        file_choice = input().strip()
        print()

        # Checking if file_choice is an integer
        while True:
            try:
                file_choice = int(file_choice)
                break
            except Exception:
                print(invalid_text)
                file_choice = input().strip()
                print()
        
        # Importing tasks from a file
        if file_choice == 1:    
            file = input("Enter the name of the file (with .csv extension): ")
            # file = "tasks.csv"
            print()

            while True:
                try:        # If file exists, open it
                    tasklist = ToDo_List.csv_to_tasks(file)
                    break
                except FileNotFoundError:   # If file does not exist, ask for a new file
                    print(Fore.RED + "File does not exist. Enter again")
                    file = input("Enter the name of the file: ")
                    print()

            print(Fore.CYAN + "Reading file... ")
            todo = ToDo_List(tasklist)      # Create a ToDo_List object with the tasks read from the file
            print(Fore.GREEN + "Successfully read tasks from file!")
            print()

            # Display the tasks read from the file
            print("Your tasks are:")
            print()
            todo.get_tasks()
            print()
            break
        
        # Creating a new tasklist
        elif file_choice == 2:      
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
        choice = input("Enter your choice: ").strip()
        print()

        # Checking if choice is an integer and among the correct options
        while True:
            if choice.isdigit():

                if int(choice) in [1,2,3,4,5,6]:
                    choice = int(choice)
                    break
                else:
                    print(invalid_text)
                    choice = input("Enter your choice: ").strip()
                    print()
            else:
                print(invalid_text)
                choice = input("Enter your choice: ").strip()
                print()

        while True:

            if choice == 1:     # Adding a task
                print(Fore.CYAN + "You choose to add a task")
                print()

                task = todo.input_task()
                print()

                try:
                    task_str = Fore.GREEN + todo.add_task(task)
                    print(Fore.YELLOW + "Task Added! Details are:")
                except Exception as e:
                    print(e)
                    task_str = Fore.RED + "No task added\n"

            elif choice == 2:      # Removing a task

                # If there are no tasks to remove
                if not todo.tasklist:   
                    task_str = "No tasks to remove\n"
                
                else:
                    print(Fore.CYAN + "You choose to remove a task")

                    # Displaying the tasks to remove
                    print("Your tasks are:")
                    print()
                    todo.get_tasks()
                    print()

                    id = int(input("Enter the id of the task you want to remove: "))
                    print()

                    # If task id is not valid
                    try:
                        task_str = Fore.GREEN + todo.remove_task(id)
                        print(Fore.YELLOW + "Task Removed! Details are:")
                    except Exception as e:
                        print(e)
                        task_str = Fore.RED + "No task removed\n"
                
            elif choice == 3:       # Modifying a task

                # If there are no tasks to modify
                if not todo.tasklist:   
                    task_str = "No tasks to modify\n"
                
                else:
                    print(Fore.CYAN + "You choose to modify a task")

                    # Displaying the tasks to modify
                    print("Your tasks are:")
                    print()
                    todo.get_tasks()
                    print()

                    id = int(input("Enter the id of the task you want to modify: "))
                    print()

                    # Checking if task_id is present
                    if id not in todo.ids:
                        print(Fore.RED + f"Task with id {id} is not present")
                        task_str = Fore.RED + "No task modified\n"
                    
                    else:
                        print("What do you want to modify?")
                        print("1. title")
                        print("2. due_date")
                        print("3. due_time")
                        print("4. priority")

                        # Check if modify is a valid input
                        while True:
                            modify = input().strip()
                            print()

                            if modify.isdigit():

                                if int(modify) in [1,2,3,4]:
                                    modify = int(modify)
                                    break
                                else:
                                    print(invalid_text)
                            
                            else:
                                print(invalid_text)

                        if modify == 1:     # title
                            attr = "title"
                            new = input("Enter new title: ")
                        elif modify == 2:       # due_date
                            attr = "due_date"
                            new = input("Enter new due date (in YYYY-MM-DD format): ")
                        else:       # due_time
                            attr = "due_time"
                            new = input("Enter new due time (in 24 hr HH:MM format). Else, leave blank: ")

                        print()
                        # Checking if new_value passed if of correct type
                        try:
                            task_str = Fore.GREEN + todo.modify_task(id, attr, new)
                            print()
                            print(Fore.YELLOW + "Task Modified! Details are:")
                        except Exception as e:
                            print(e)
                            task_str = Fore.RED + "No task modified\n"

            elif choice == 4:       # Checking off a task

                # If there are no tasks to check off
                if not todo.tasklist:   
                    task_str = "No tasks to check off\n"
                
                else:
                    print(Fore.CYAN + "You choose to tick off a task")

                    # Displaying the tasks to modify
                    print("Your tasks are:")
                    print()
                    tasks = todo.get_tasks(category=['overdue', 'pending'])
                    print()

                    id = int(input("Enter the id of the task you want to check off: "))
                    print()

                    # Checking if id is present
                    if id not in todo.ids:
                        print(Fore.RED + f"Task with id {id} is not present")
                        task_str = Fore.RED + "No task ticked off\n"
                    else:

                        # Checking if task is already completed
                        if id not in tasks["id"].values:
                            task_str = "Task is already complete\n"
                        else:
                            task_str = Fore.GREEN + todo.complete_task(id)
                            print(Fore.YELLOW + "Congratulations on finishing your task. Details are:")

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
                print("8. Filter overdue tasks (due_date has crossed)")
                print("9. Filter pending tasks")
                print("10. Filter completed tasks")
                print("11. Filter high priority tasks")
                print("12. Filter moderate priority tasks")
                print("13. Filter low priority tasks")
                print("14. Filter tasks to be completed by today")
                print()
                print("15. Just show me the tasks!")
                print()
                i = 1

                while i == 1:
                    view_choice = input("Enter your choice: ").strip()
                    print()

                    # Checking if view_choice is an integer
                    while True:
                        try:
                            view_choice = int(view_choice)
                            break
                        except Exception:
                            print(invalid_text)
                            view_choice = input("Enter your choice: ").strip()

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
                        todo.get_tasks(category='overdue')
                    elif view_choice == 9:
                        todo.get_tasks(category='pending')
                    elif view_choice == 10:
                        todo.get_tasks(category='completed')
                    elif view_choice == 11:
                        tasklist = todo.filter_tasks(attribute="priority", value="high")
                    elif view_choice == 12:
                        tasklist = todo.filter_tasks(attribute="priority", value="moderate")
                    elif view_choice == 13:
                        tasklist = todo.filter_tasks(attribute="priority", value="low")
                    elif view_choice == 14:
                        today = date.today()
                        tasklist = todo.filter_tasks(attribute="due_date", value=today)

                    # Show Tasks without any sorting or filtering
                    elif view_choice == 15:
                        todo.get_tasks()

                    else:
                        print(invalid_text)
                        i = 0
                    
                    i += 1

                # Output for these choices are already printed previously
                if view_choice not in [8, 9, 10, 15]:
                    
                    # Checking if tasklist is empty
                    if len(tasklist) == 0:
                        print("No tasks to display")
                    
                    else:
                        print("Your tasks are:")
                        print()
                        print(tasklist)
                    
                    print()

            else:       # Exit
                if changed:

                    # Asking user if he wants to save his changes
                    while True:
                        save = input("Do you want to save your changes (y/n)?: ").lower().strip()

                        if save == 'y':
                            file = input("Enter the filename(csv) to which you want to save your tasks: ")
                            print()

                            print(Fore.CYAN + "Recording Tasks... ")
                            ToDo_List.tasks_to_csv(todo.tasklist, file)
                            print(Fore.GREEN + "Successfully recorded all tasks!")
                            print()
                            break

                        elif save == 'n':
                            break

                        else:
                            print(invalid_text)

                print(Fore.LIGHTYELLOW_EX + "Thanks for using the ToDo application. Have a nice day!")
                print()
                return

            if choice in [1,2,3,4]:     # Printing task details for add, remove, modify, and complete operations
                print(task_str)
                changed = True      # tasklist has been updated so tasks have to be recorded to a file


            print("What's next on your mind?")
            print("1. Perform the same operation")
            print("2. Perform a different operation")
            print("3. Save tasks and exit")
            print("4. Exit without saving")

            while True:
                next_action = input().strip()
                print()

                # Checking if next_action is an integer
                while True:
                    try:
                        next_action = int(next_action)
                        break
                    except Exception:
                        print(invalid_text)
                        next_action = input().strip()

                # Perform same operation
                if next_action == 1:
                    same_op = True      # Flag to check for same operation
                    break
                
                # Perform different operation
                elif next_action == 2:
                    same_op = False
                    print()
                    break
                
                # Save and exit
                elif next_action == 3:
                    if changed:     # If the tasklist has been changed
                        file = input("Enter the file(with .csv extension) to which you want to save your tasks: ")
                        print()

                        print(Fore.CYAN + "Recording Tasks... ")
                        ToDo_List.tasks_to_csv(todo.tasklist, file)
                        print(Fore.GREEN + "Successfully recorded all tasks!")
                        print()

                    print(Fore.LIGHTYELLOW_EX + "Thanks for using the ToDo application. Have a nice day!")
                    print()
                    return
                
                # Exit without saving
                elif next_action == 4:
                    print(Fore.LIGHTYELLOW_EX + "Thanks for using the ToDo application. Have a nice day!")
                    print()
                    return
                
                # Invalid Input
                else:
                    print(invalid_text)

            if not same_op:
                break

if __name__ == "__main__":
    main()

    

        
