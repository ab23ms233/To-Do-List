from datetime import datetime, date, time
from dateutil.parser import parse
from typing import Dict, List, Literal, Any, Union
import pandas as pd
import csv
import os


class ToDo_List:
    """
    A class representing a To-Do List, allowing for the management of tasks with attributes such as title, due date, due time, priority, creation time, and completion status.

    **Class Attributes:**
        - `attributes` (Dict[str, type]): A dictionary defining the expected types for each task attribute.
        - `input_attributes` (List[str]): A list of attributes that can be input by the user when adding a new task.
        - `priority_values` (List[str]): A list of valid priority values for tasks.

    **Instance Attributes:**
        - `tasklist` (List[Dict[str, Any]]): A list of tasks, where each task is represented as a dictionary.
        - `ids` (List[int]): A list of task IDs.
    
    **Task Attributes:**
        - `id` (int): Unique identifier for the task.
        - `title` (str): Title of the task.
        - `due_date` (date): Due date of the task in YYYY-MM-DD format.
        - `due_time` (time): Due time of the task in 24 hr format (HH:MM). 'NA' if no time is set.
        - `priority` (str): Priority of the task. Must be one of (high, moderate, low).
        - `created_at` (datetime): Creation time of the task.
        - `completed` (bool): Indicates whether the task is completed or not.
    
    **Methods:**
        - `correct_attributes(task: Dict[str, Any]) -> Dict[str, Any]`: Validates and corrects the attributes of a task.
        - `input_task() -> Dict[str, Any]`: Prompts the user to input details for a new task.
        - `add_task(task: Dict[str, Any]) -> str`: Adds a new task to the tasklist.
        - `display_tasks() -> pd.DataFrame`: Displays the current tasklist as a pandas DataFrame.
        - `modify_task(id: int, attribute: Literal["title", "due_date", "due_time", "priority"], new_value) -> str`: Modifies an existing task in the tasklist.
        - `complete_task(id: int) -> str`: Marks a task as completed.
        - `remove_task(id: int) -> str`: Removes a task from the tasklist by its ID.
        - `sort_tasks(attribute: Union[Literal["priority", "created_at", "completed"], List], ascending: bool = False) -> pd.DataFrame`: Sorts the tasks in the tasklist based on a specified attribute.
        - `filter_tasks(attribute: Literal["due_date", "priority", "completed"], value, operator: str = "=") -> pd.DataFrame`: Filters tasks in the tasklist based on a specified attribute and value.
        - `tasks_to_csv(tasklist: List[Dict[str, Any]], filename: str) -> None`: Writes the tasklist to a CSV file.
        - `csv_to_tasks(filename: str) -> List[Dict[str, Any]]`: Reads tasks from a CSV file and returns them as a list of dictionaries.
    
    **Example:**
        >>> todo = ToDo_List([
        ...     {"id": 1, "title": "Sample Task", "due_date": "2023-10-01",
        ...      "due_time": "12:00", "priority": "high", "created_at": "2023-09-30 10:00", "completed": False}
        ... ])
        >>> print(todo.add_task({"title": "New Task", "due_date": "2023-10-02", "due_time": "14:00", "priority": "moderate", "completed": False}))
        id: 2
        title: New Task
        due_date: 2023-10-02
        due_time: 14:00
        priority: moderate
        created_at: 2023-09-30 10:00
        completed: False
    """
    # Class attributes defining the expected types and values for task attributes
    attributes = {"id": int, 
                  "title": str, 
                  "due_date": date, 
                  "due_time": time, 
                  "priority": str,
                  "created_at": datetime, 
                  "completed": bool}
    
    input_attributes = ["title", "due_date", "due_time", "priority", "completed"]
    priority_values = ["high", "moderate", "low"]

    def correct_attributes(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Checks if the task dictionary contains all required attributes and validates their types.

        **Parameters**:
            `task` (Dict[str, Any]): A dictionary representing a task with attributes like id, title, due_date, due_time, priority, created_at, and completed.
        
        **Returns:**
            `Dict[str, Any]`: The corrected task dictionary with all attributes validated and corrected if necessary.
        
        **Raises:**
            - `TypeError`: If the task is not a dictionary or if any attribute is not of the expected type.
            - `ValueError`: If the task dictionary does not contain all required attributes or contains unexpected keys.
        """        
        # Check if the task dictionary contains all required attributes
        if not set(task.keys()).issubset(ToDo_List.attributes.keys()):
            raise ValueError(f"Task dictionary must only contain the following keys: {list(ToDo_List.attributes.keys())}")
        
        for attr in ToDo_List.attributes:
            
            # Correction for id attribute
            if attr == "id":    
                if attr in task:        # If id is present
                    if not isinstance(task[attr], int):     # If id is not int
                        try:
                            task[attr] = int(task[attr])    # Try converting to int
                        except Exception:
                            raise TypeError(f"{attr} must be of type {ToDo_List.attributes[attr]}")   
                    
                    if task[attr] in self.ids:      # Check if id is unique
                        raise ValueError(f"task with id {task[attr]} is already present")
                    
                else:       # Generates the id automatically if not present
                    new_id = (max(self.ids) if self.ids else 0) + 1
                    task[attr] = new_id
                    
            # Correction for title attribute
            elif attr == "title" and not isinstance(task[attr], str):      # Checks if title is a string
                raise TypeError(f"{attr} must be of type {ToDo_List.attributes[attr]}")
            
            # Correction for created_at attribute
            elif attr == "created_at":      
                if attr not in task:        # Generates the creation time automatically if not present
                    creation_time = datetime.now().replace(microsecond=0)
                    task[attr] = creation_time
                elif not isinstance(task[attr], datetime):     # Checks if created_at is a datetime object
                    try:
                        task[attr] = parse(task[attr])
                    except Exception:
                        raise TypeError(f"{attr} must be of type {ToDo_List.attributes[attr]}")

            # Correction for due_date attribute
            elif attr == "due_date" :       
                if not isinstance(task[attr], date):         # Checks if due_date is a date object
                    try:
                        task[attr] = parse(task[attr]).date()
                    except Exception:
                        raise TypeError(f"{attr} must be of type {ToDo_List.attributes[attr]}")

            # Correction for due_time attribute
            elif attr == "due_time":        
                if task[attr] == '':
                    task[attr] = 'NA'
                elif task[attr] != 'NA' and not isinstance(task[attr], time):       # Checks if due_time is a time object
                    try:
                        task[attr] = parse(task[attr]).time()
                    except Exception:
                        raise TypeError(f"{attr} must be of type {ToDo_List.attributes[attr]}")
                    
            # Correction for priority attribute
            elif attr == "priority":      
                if not isinstance(task[attr], str):
                    raise ValueError("priority must be of type str")
                
                task[attr] = task[attr].lower()
                if task[attr] not in ToDo_List.priority_values:     # Checks if priority is one of the valid values
                    raise ValueError(f"{attr} must be one of {ToDo_List.priority_values}")
                
            # Correction for completed attribute
            elif attr == "completed" and not isinstance(task[attr], bool):      
                if isinstance(task[attr], str) and task[attr].lower() == "true":        # Convert string values to boolean
                    task[attr] = True
                elif isinstance(task[attr], str) and task[attr].lower() == "false":
                    task[attr] = False
                else:
                    raise TypeError(f"{attr} must be of type {ToDo_List.attributes[attr]}")

            # Check if the attribute is of the expected type
            elif not isinstance(task[attr], ToDo_List.attributes[attr]):
                raise TypeError(f"{attr} must be of type {ToDo_List.attributes[attr]}")
            
        return task

    def __init__(self, tasklist: List[Dict[str, Any]] = []) -> None:
        """
        Initializes a ToDo_List instance with an optional list of tasks.

        **Parameters:**
            - `tasklist` (List[Dict[str, Any]], optional):  
              A list of tasks, where each task is a dictionary containing task attributes.  
              If no tasklist is provided, it initializes with an empty list.

        *Each task dictionary should contain the following keys:*
            - `title` (str): Title of the task.  
            - `due_date` (str): Due date of the task in YYYY-MM-DD format.  
            - `due_time` (str): Due time of the task in 24 hr format (HH:MM). 'NA' if no time is set. 
            - `priority` (str): Priority of the task. Must be one of (high, moderate, low).
            - `completed` (bool): Indicates whether the task is completed or not.

        **Attributes:**
            - `tasklist` (List[Dict[str, Any]]): The list of tasks, where each task is represented as a dictionary.
            - `ids` (List[int]): A list of task IDs.

        **Raises:**
            `TypeError`: If the tasklist is not a list or contains items that are not dictionaries.

        **Example:**
            >>> todo = ToDo_List([
            ...     {"id": 1, "title": "Sample Task", "due_date": "2023-10-01",
            ...      "due_time": "12:00", "priority": "high", "created_at": "2023-09-30 10:00", "completed": False}
            ... ])
        """
        if not isinstance(tasklist, list):
            raise TypeError("tasklist must be a list.")
        if not all(isinstance(task, dict) for task in tasklist):
            raise TypeError("tasks must be dictionaries")
        
        self.ids = []

        # Checks if all attributes are of the correct type and if all required attributes are present
        for task in tasklist:
            task = self.correct_attributes(task)
            self.ids.append(task["id"])     # Collects the ids of the tasks

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
            >>> task = {"id": 1, "title": "Sample Task", "due_date": "2023-10-01", "due_time": "12:00", "priority": "high", "created_at": "2023-09-30 10:00", "completed": False}
            >>> print(ToDo_List.task_to_str(task))
            id: 1
            title: Sample Task
            due_date: 2023-10-01
            due_time: 12:00
            priority: high
            created_at: 2023-09-30 10:00
            completed: False
        """
        task_str = ''

        for attr in ToDo_List.attributes:
            val = task[attr]
            task_str += f"{attr}: {val}\n"

        return task_str

    def input_task(self) -> Dict[str, Any]:
        """
        Asks the user to input details for a new task.

        **Returns:**
            `Dict[str, Any]`: A dictionary representing the new task with attributes like id, title, due_date, due_time, priority, created_at, and completed.
        """
        title = input("Enter the task: ")
        duedate = input("Enter due date (in YYYY/MM/DD format): ")
        duetime = input("Enter due time if any, else leave blank (in 24 hr format: HH:MM): ")
        priority = input(f"Enter the priority of the task [low(1), moderate(2), high(3)]: ")

        priority_order = {"1": "low", "2": "moderate", "3": "high"}

        if priority.isdigit() and priority in priority_order:     # Converts priority from string to priority value if it is a digit
            priority = priority_order[priority]

        completed = False
        values = [title, duedate, duetime, priority, completed]
        task = {attribute: value for (attribute, value) in zip(ToDo_List.input_attributes, values)}

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
            - `priority` (str): Priority of the task. Must be one of (high, moderate, low).
            - `completed` (bool): Indicates whether the task is completed or not.

        **Returns:**
            `str`: A formatted string representation of the added task.

        **Raises:**
            - `TypeError`: If the task is not a dictionary or if any attribute is not of the expected type.
            - `ValueError`: If the task dictionary does not contain all required attributes.
            - `ValueError`: If the due_date is in the past or if the due_time is in the past on the same day.

        **Example:**
            >>> task = {"title": "Sample Task", "due_date": "2023-10-01", "due_time": "12:00", "priority": "high, "completed": False}
            >>> todo = ToDo_List()
            >>> print(todo.add_task(task))
            id: 1
            title: Sample Task
            due_date: 2023-10-01
            due_time: 12:00
            priority: high
            created_at: 2023-09-30 10:00
            completed: False
        """
        task = self.correct_attributes(task)

        if task["due_date"] < date.today():       # Check if due_date is in the past
            raise ValueError("due_date cannot be in the past.")
        if task["due_date"] == date.today() and (isinstance(task["due_time"], time) and task["due_time"] < datetime.now().time()):       # Check if due_time is in the past
            raise ValueError("due_time cannot be in the past.")
        
        self.ids.append(task["id"])
        self.tasklist.append(task)

        return ToDo_List.task_to_str(task)
    
    def display_tasks(self) -> pd.DataFrame:
        """
        Displays the current tasklist as a pandas DataFrame.

        **Returns:**
            `pd.DataFrame`: A DataFrame containing the current tasklist, with each task represented as a row.
        """
        tasklist = pd.DataFrame(self.tasklist, columns=list(ToDo_List.attributes))
        return tasklist

    def modify_task(self, id: int, attribute: Literal["title", "due_date", "due_time", "priority"], new_value) -> str:
        """
        Modifies an existing task in the tasklist.

        **Parameters:**
            - `id` (int): The ID of the task to be modified.
            - `attribute` (Literal["title", "due_date", "due_time", "priority"]): The attribute of the task to be modified.
            - `new_value`: The new value for the specified attribute.
        
        **Returns:**
            `str`: A formatted string representation of the modified task.
        
        **Raises:**
            - `TypeError`: If the new value is not appropriate for the attribute.
            - `ValueError`: If the specified attribute is not valid.
            - `ValueError`: If the task ID is not present in the tasklist.
            - `ValueError`: If the due_date is in the past or if the due_time is in the past on the same day.

        **Example:**
            >>> todo = ToDo_List([
            ...     {"title": "Sample Task", "due_date": "2023-10-01", "due_time": "12:00", "priority": "high", "completed": False}
            ... ])
            >>> print(todo.modify_task(1, "title", "Updated Task", "high"))
            id: 1
            title: Updated Task
            due_date: 2023-10-01
            due_time: 12:00
            priority: high
            created_at: 2023-09-30 10:00
            completed: False
        """
        # Check for id
        if not isinstance(id, int):
            try:
                id = int(id)
            except Exception:
                raise TypeError("id must be of type int")
            
        if id not in self.ids:
            raise ValueError(f"task with id {id} is not present") 
        
        for i in range(len(self.ids)):
            if id == self.tasklist[i]["id"]:
                index = i
                break

        task = self.tasklist[index]

        
        # Checks if the attribute is valid
        if attribute not in ["title", "due_date", "due_time", "priority"]:      
            raise ValueError("attribute must be one of ['title', 'due_date', 'due_time', 'priority']")
        
        # Check for title
        if attribute == "title" and not isinstance(new_value, str):
            raise TypeError(f"title must be of str type")
        
        # Check for due_date
        if attribute == "due_date":     
            if not isinstance(new_value, date):     # Checks if the new value is in the correct format for due_date
                try:
                    new_value = parse(new_value).date()
                except Exception:
                    raise ValueError("due_date must be in YYYY-MM-DD format.")
            
            if new_value < date.today():     # Check if due_date is in the past
                raise ValueError("due_date cannot be in the past.")

        # Check for due_time
        elif attribute == "due_time":   
            if isinstance(new_value, str) and new_value.strip() == '':
                new_value = 'NA'
            elif not isinstance(new_value, time):       # Checks if the new value is in the correct format for due_time
                try:
                    new_value = parse(new_value).time()
                    
                    if task["due_date"] == date.today() and new_value < datetime.now().time():       # Check if due_date is in the past
                        raise ValueError("due_time cannot be in the past.")
                    
                except Exception:
                    raise ValueError("due_time must be in 24 hr format (HH:MM).")
        
        # Check for priority
        elif attribute == "priority" and new_value not in ToDo_List.priority_values:        # Checks if the new value is a valid priority
            raise ValueError(f"priority must be one of {ToDo_List.priority_values}")

        self.tasklist[index][attribute] = new_value
        task = self.tasklist[index]

        return ToDo_List.task_to_str(task)
    
    def complete_task(self, id: int) -> str:
        """
        Checks off a task as completed in the tasklist.

        **Parameters:**
            `id` (int): The ID of the task to be marked as completed.
        
        **Returns:**
            `str`: A formatted string representation of the completed task.
        
        **Raises:**
            `ValueError`: If the task ID is not present.

        **Example:**
            >>> todo = ToDo_List([
            ...     {"title": "Sample Task", "due_date": "2023-10-01", "due_time": "12:00", "priority": "high", "completed": False}
            ... ])
            >>> print(todo.complete_task(1))
            id: 1
            title: Sample Task
            due_date: 2023-10-01
            due_time: 12:00
            priority: high
            created_at: 2023-09-30 10:00
            completed: True
        """
        if id not in self.ids:
            raise ValueError(f"task with id {id} is not present.")
        
        for i in range(len(self.ids)):
            if id == self.tasklist[i]["id"]:
                index = i
                break

        self.tasklist[index]["completed"] = True
        task = self.tasklist[index]

        return ToDo_List.task_to_str(task)
    
    def remove_task(self, id: int) -> str:
        """
        Removes a task from the tasklist by its ID.

        **Parameters:**
            `id` (int): The ID of the task to be removed.
        
        **Returns:**
            `str`: A formatted string representation of the removed task.
        
        **Raises:**
            `ValueError`: If the task ID is not present.
        
        **Example:**
            >>> todo = ToDo_List([
            ...     {"title": "Sample Task", "due_date": "2023-10-01", "due_time": "12:00", "priority": "high", "completed": False}
            ... ])
            >>> print(todo.remove_task(1))
            id: 1
            title: Sample Task
            due_date: 2023-10-01
            due_time: 12:00
            priority: high
            created_at: 2023-09-30 10:00
            completed: False
        """
        if id not in self.ids:
            raise ValueError(f"task with id {id} is not present.")
        
        for i in range(len(self.ids)):
            if id == self.tasklist[i]["id"]:
                index = i
                break

        task = self.tasklist.pop(index)
        self.ids.remove(id)

        return ToDo_List.task_to_str(task)

    def sort_tasks(self, attribute: Union[Literal["priority", "created_at", "completed"], List], ascending: bool = False) -> pd.DataFrame:
        """
        Sorts the tasks in the tasklist based on a specified attribute.

        **Parameters:**
            - `attribute` (Union[Literal["priority", "created_at", "completed"], List]): The attribute to sort by.
              It can be one of "priority", "created_at", "completed", or a list containing ["due_date", "due_time"].
            - `ascending` (bool, optional): Whether to sort in ascending order. Defaults to False.
        
        **Returns:**
            `pd.DataFrame`: A DataFrame containing the sorted tasklist.
        
        **Raises:**
            `ValueError`: If the attribute is not valid.
        
        **Example:**
            >>> todo = ToDo_List([
            ...     {"title": "Sample Task", "due_date": "2023-10-01", "due_time": "12:00", "priority": "high", "completed": False}
            ... ])
            >>> sorted_tasks = todo.sort_tasks("priority", ascending=True)
            >>> print(sorted_tasks)
        """

        if attribute not in [["due_date", "due_time"], "priority", "created_at", "completed"]:
            raise ValueError("attribute must be a value from [['due_date', 'due_time'], 'priority', 'created_at', 'completed']")
        
        tasklist = pd.DataFrame(self.tasklist, columns=list(ToDo_List.attributes.keys()))
        tasklist["priority"] = pd.Categorical(tasklist["priority"], categories=ToDo_List.priority_values, ordered=True)     # Converts priority to a categorical type for sorting

        tasklist = tasklist.sort_values(by=attribute, ascending=ascending)
        return tasklist
    
    def filter_tasks(self, attribute: Literal["due_date", "priority", "completed"], value, operator: str = "=") -> pd.DataFrame:
        """
        Filters tasks in the tasklist based on a specified attribute and value.

        **Parameters:**
            - `attribute` (Literal["due_date", "priority", "completed"]): The attribute to filter by.
            - `value`: The value to filter the tasks by.
            - `operator` (str, optional): The operator to use for filtering. Defaults to "=".
        
        **`Note:`** `operator` is used only for filtering pending tasks in this version. However, it can be used for other tasks upon modification.
        
        **Returns:**
            `pd.DataFrame`: A DataFrame containing the filtered tasks.
        
        **Raises:**
            - `ValueError`: If the attribute is not valid or if the value is not appropriate for the attribute.
            - `TypeError`: If the value is not of the expected type for the attribute.
        
        **Example:**
            >>> todo = ToDo_List([
            ...     {"title": "Sample Task", "due_date": "2023-10-01", "due_time": "12:00", "priority": "high", "completed": False}
            ... ])
            >>> filtered_tasks = todo.filter_tasks("priority", "high")
            >>> print(filtered_tasks)
        """
        if operator not in ["=", ">", "<", ">=", "<=", "!="]:
            raise ValueError("operator must be one of ['=', '>', '<', '>=', '<=', '!=']")
        
        if attribute not in ["due_date", "priority", "completed"]:
            raise ValueError("attribute must be a value from ['due_date', 'priority', 'completed']")
        
        if attribute == "priority" and value not in ToDo_List.priority_values:
            raise ValueError(f"{attribute} can only have values {ToDo_List.priority_values}")
        
        if attribute == "completed" and value not in [True, False]:
            raise ValueError(f"{attribute} can only have values [True, False]")
        
        if attribute == "due_date":
            if isinstance(value, str):     # Checks if the value is in the correct format for due_date
                try:
                    value = datetime.strptime(value, "%Y-%m-%d").date()
                except Exception:
                    raise ValueError("due_date must be in YYYY-MM-DD format.")
            elif not isinstance(value, date):
                raise TypeError(f"{attribute} must be of type {date}") 
        

        tasklist = pd.DataFrame(self.tasklist, columns=list(ToDo_List.attributes.keys()))

        if operator == "=":  # Filters the tasklist based on the attribute and value
            tasklist = tasklist[tasklist[attribute] == value]
        elif operator == "<":   # For checking tasks whose due_date has passed (pending tasks)
            tasklist = tasklist[tasklist[attribute] < value]

        return tasklist

    @staticmethod
    def tasks_to_csv(tasklist: List[Dict[str, Any]], filename: str) -> None:
        """
        Writes the tasklist to a CSV file.

        **Parameters:**
            - `tasklist` (List[Dict[str, Any]]): A list of tasks, where each task is a dictionary containing task attributes.
            - `filename` (str): The name of the CSV file to write the tasks to.
        
        **Raises:**
            `TypeError`: If the filename is not a string.
        """
        if not isinstance(filename, str):
            raise TypeError("filename must be a string")
        
        f = open(filename, mode="w", newline="")

        writer = csv.writer(f)
        header = list(ToDo_List.attributes.keys())      # List of columns for header
        writer.writerow(header)     # Writing header to the file
        task_list, row = [], []

        for task in tasklist:
            for attr in ToDo_List.attributes:
                row.append(task[attr])
            task_list.append(row)       # Preparing the tasklist for writing to the file
            row = []

        writer.writerows(task_list)
        f.close()

    @staticmethod
    def csv_to_tasks(filename: str) -> List[Dict[str, Any]]:
        """
        Reads tasks from a CSV file and returns them as a list of dictionaries.

        **Parameters:**
            `filename` (str): The name of the CSV file to read tasks from.

        **Returns:**
            `List[Dict[str, Any]]`: A list of tasks, where each task is a dictionary containing task attributes.
        
        **Raises:**
            - `FileNotFoundError`: If the specified file does not exist.
            - `TypeError`: If the filename is not a string.
            - `ValueError`: If the attributes in the file do not match the expected attributes.
        """
        if not isinstance(filename, str):
            raise TypeError("filename must be a string")

        if os.path.exists(filename):    # Checking if the file exists

            if os.path.getsize(filename) == 0:      # Checking if the file is empty
                print("The file is empty. Initialising empty tasklist... ")
                tasklist = []

            else:       # If the file is not empty, read the tasks from the file
                f = open(filename, mode="r", newline="")
                reader = csv.reader(f)
                tasklist, task = [], {}

                reader = list(reader)
                header = reader[0]

                if header != list(ToDo_List.attributes.keys()):      # Checking if the header matches the attributes
                    raise ValueError(f"Attributes in the file do not match the expected attributes: {list(ToDo_List.attributes.keys())}")

                for row in reader[1:]:  # Constructing a list of dictionaries from the file - tasklist
                    for (attr, element) in zip(ToDo_List.attributes, row):
                        task[attr] = element
                    tasklist.append(task)
                    task = {}
            
            f.close()
            return tasklist
        
        else:
            raise FileNotFoundError(f"{filename} does not exist. Please check the file path.")
                