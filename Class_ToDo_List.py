from datetime import datetime, date, time
from typing import Dict, List, Literal, Any
import pandas as pd
from IPython.display import display

class ToDo_List:
    attributes = {"id": int, 
                  "title": str, 
                  "due_date": date, 
                  "due_time": time, 
                  "priority": str,
                  "created_at": datetime, 
                  "completed": bool}
    
    input_attributes = ["title", "due_date", "due_time", "priority", "completed"]

    def correct_attributes(self, task: Dict[str, Any]) -> bool:
        """
        Checks if the task dictionary contains all required attributes and validates their types.

        **Parameters**:
            `task` (Dict[str, Any]): A dictionary representing a task with attributes like id, title, due_date, due_time, created_at, and completed.
        
        **Returns:**
            `bool`: True if the task dictionary is valid, otherwise raises an error.
        
        **Raises:**
            - `TypeError`: If the task is not a dictionary or if any attribute is not of the expected type.
            - `ValueError`: If the task dictionary does not contain all required attributes or contains unexpected keys.
        """        
        # Check if the task dictionary contains all required attributes
        if not set(task.keys()).issubset(ToDo_List.attributes.keys()):
            raise ValueError(f"Task dictionary must only contain the following keys: {list(ToDo_List.attributes.keys())}")
        
        for attr in ToDo_List.attributes:
             
            if attr == "id" and attr not in task.keys():    # Generates the id automatically if not present
                self.num_of_tasks += 1
                task[attr] = self.num_of_tasks

            elif attr == "created_at" and attr not in task.keys():      # Generates the creation time automatically if not present
                creation_time = datetime.now()
                task[attr] = creation_time

            elif attr == "due_date" and not isinstance(task[attr], date):        # Converts due_date from string to date object if not already
                task[attr] = datetime.strptime(task[attr], "%Y-%m-%d").date()

            elif attr == "due_time":        # Converts due_time from string to time object if not already
                if task[attr] != 'NA' and not isinstance(task[attr], time):
                    task[attr] = datetime.strptime(task[attr], "%H:%M").time()

            # Check if the attribute is of the expected type
            elif not isinstance(task[attr], ToDo_List.attributes[attr]):
                raise TypeError(f"{attr} must be of type {ToDo_List.attributes[attr]}")
            
        return True

    def __init__(self, tasklist: pd.DataFrame = pd.DataFrame()) -> None:
        """
        Initializes a ToDo_List instance with an optional list of tasks.

        **Parameters:**
            - `tasklist` (pd.Dataframe, optional):  
              A list of tasks, where each task is a dictionary containing task attributes.  
              If no tasklist is provided, it initializes with an empty list.

        *Each task dictionary should contain the following keys:*
            - `title` (str): Title of the task.  
            - `due_date` (str): Due date of the task in YYYY-MM-DD format.  
            - `due_time` (str): Due time of the task in 24 hr format (HH:MM). 'NA' if no time is set.  
            - `completed` (bool): Indicates whether the task is completed or not.

        **Attributes:**
            - `num_of_tasks` (int): The number of tasks in the tasklist.
            - `tasklist` (List[Dict]): The list of tasks, where each task is represented as a dictionary.

        **Raises:**
            `TypeError`: If the tasklist is not a list or contains items that are not dictionaries.

        **Example:**
            >>> todo = ToDo_List([
            ...     {"id": 1, "title": "Sample Task", "due_date": "2023-10-01",
            ...      "due_time": "12:00", "created_at": "2023-09-30 10:00", "completed": False}
            ... ])
        """
        if not isinstance(tasklist, pd.DataFrame):
            raise TypeError("tasklist must be a pandas DataFrame.")
        
        self.num_of_tasks = 0

        # Checks if all attributes are of the correct type and if all required attributes are present
        for task in tasklist:
            self.correct_attributes(task)

        self.tasklist = tasklist
                   
    @staticmethod
    def task_to_str(task: Dict[str, Any]) -> str:
        """
        Converts a task dictionary to a formatted string representation.

        **Parameters:**
            `task` (Dict[str, Any]):  A dictionary representing a task with attributes like id, title, due_date, due_time, created_at, and completed.
        
        **Returns:**
            `str`:  A formatted string representation of the task, with each attribute on a new line.
        
        **Example:**
            >>> task = {"id": 1, "title": "Sample Task", "due_date": "2023-10-01", "due_time": "12:00", "created_at": "2023-09-30 10:00", "completed": False}
            >>> print(ToDo_List.task_to_str(task))
            id: 1
            title: Sample Task
            due_date: 2023-10-01
            due_time: 12:00
            created_at: 2023-09-30 10:00
            completed: False
        """
        task_str = ''

        for i in task:
            attribute = i
            val = task[i]
            task_str += f"{attribute}: {val}\n"

        return task_str

    def input_task(self) -> Dict[str, Any]:
        """
        Asks the user to input details for a new task.

        **Returns:**
            `Dict[str, Any]`: A dictionary representing the new task with attributes like id, title, due_date, due_time, created_at, and completed.
        """
        title = input("Enter the task: ")
        duedate = input("Enter due date (in DD/MM/YYYY format):")
        duetime = input("Enter due time if any, else leave blank (in 24 hr format: HH:MM): ")

        self.num_of_tasks += 1
        task_id =  self.num_of_tasks
        due_date = datetime.strptime(duedate, "%d/%m/%Y").date()

        if duetime == '':
            due_time = 'NA'
        else:
            due_time = datetime.strptime(duetime, "%H:%M").time()
        
        created_at = datetime.now()
        completed = False

        values = [task_id, title, due_date, due_time, created_at, completed]
        task = {attribute: value for (attribute, value) in zip(ToDo_List.attributes, values)}

        return task

    def add_task(self, task: Dict[str, Any]) -> str:
        """
        Adds a new task to the tasklist.

        **Parameters:**
            - `task` (Dict[str, Any]): A dictionary representing the task to be added. 
        
        *It should contain the following keys:*
            - `title` (str): Title of the task.  
            - `due_date` (str): Due date of the task in YYYY-MM-DD format.  
            - `due_time` (str): Due time of the task in 24 hr format (HH:MM). 'NA' if no time is set.  
            - `completed` (bool): Indicates whether the task is completed or not.

        **Returns:**
            `str`: A formatted string representation of the added task.

        **Raises:**
            - `TypeError`: If the task is not a dictionary or if any attribute is not of the expected type.
            - `ValueError`: If the task dictionary does not contain all required attributes.

        **Example:**
            >>> task = {"title": "Sample Task", "due_date": "2023-10-01", "due_time": "12:00", "completed": False}
            >>> todo = ToDo_List()
            >>> print(todo.add_task(task))
            id: 1
            title: Sample Task
            due_date: 2023-10-01
            due_time: 12:00
            created_at: 2023-09-30 10:00
            completed: False
        """
        self.correct_attributes(task)
        self.tasklist.append(task)
        return ToDo_List.task_to_str(task)
    
    def display_tasks(self) -> None:
        """
        Displays the current tasklist in a tabular format using pandas DataFrame.
        """
        tasklist = pd.DataFrame(self.tasklist)
        display(tasklist)

    def modify_task(self, id: int, attribute: Literal["title", "due_date", "due_time"], new_value) -> str:
        """
        Modifies an existing task in the tasklist.

        **Parameters:**
            - `id` (int): The ID of the task to be modified.
            - `attribute` (Literal["title", "due_date", "due_time"]): The attribute of the task to be modified.
            - `new_value`: The new value for the specified attribute.
        
        **Returns:**
            `str`: A formatted string representation of the modified task.
        
        **Raises:**
            - `TypeError`: If the new value is not appropriate for the attribute.
            - `ValueError`: If the specified attribute is not valid.

        **Example:**
            >>> todo = ToDo_List([
            ...     {"title": "Sample Task", "due_date": "2023-10-01", "due_time": "12:00", "completed": False}
            ... ])
            >>> print(todo.modify_task(1, "title", "Updated Task"))
            id: 1
            title: Updated Task
            due_date: 2023-10-01
            due_time: 12:00
            created_at: 2023-09-30 10:00
            completed: False
        """
        if attribute not in ["title", "due_date", "due_time"]:
            raise ValueError("attribute must be one of ['title', 'due_date', 'due_time']")
        if attribute == "title" and not isinstance(new_value, str):
            raise TypeError(f"title must be of str type")
        
        if attribute == "due_date":
            new_value = datetime.strptime(new_value, "%Y-%m-%d").date()
        elif attribute == "due_time":
            new_value = datetime.strptime(new_value, "%H:%M").time()

        self.tasklist[id-1][attribute] = new_value
        task = self.tasklist[id-1]

        return ToDo_List.task_to_str(task)
    
    def complete_task(self, id: int) -> str:
        """
        Checks off a task as completed in the tasklist.

        **Parameters:**
            `id` (int): The ID of the task to be marked as completed.
        
        **Returns:**
            `str`: A formatted string representation of the completed task.
        
        **Raises:**
            `IndexError`: If the task ID is out of range.
        """
        if id < 1 or id > len(self.tasklist):
            raise IndexError("Task ID out of range.")
        
        self.tasklist[id-1]["completed"] = True
        task = self.tasklist[id-1]

        return ToDo_List.task_to_str(task)
    
    def remove_task(self, id: int) -> str:
        """
        Removes a task from the tasklist by its ID.

        **Parameters:**
            `id` (int): The ID of the task to be removed.
        
        **Returns:**
            `str`: A formatted string representation of the removed task.
        
        **Raises:**
            `IndexError`: If the task ID is out of range.
        """
        if id < 1 or id > len(self.tasklist):
            raise IndexError("Task ID out of range.")
        
        task = self.tasklist.pop(id-1)
        return ToDo_List.task_to_str(task)
