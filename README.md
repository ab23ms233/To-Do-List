# 📝 ToDo List CLI Application

A command-line ToDo list manager built with Python.  
This project allows users to manage tasks interactively through a CLI or programmatically using a class. Task data is saved in CSV format.

This project uses a list of dictionaries to store the tasklist. The attributes of a task are:

- `id` (int): Unique identifier for the task.
- `title` (str): Title of the task.
- `due_date` (date): Due date of the task in YYYY-MM-DD format.
- `due_time` (time): Due time of the task in 24 hr format (HH:MM). 'NA' if no time is set.
- `priority` (str): Priority of the task. Must be one of (high, moderate, low).
- `created_at` (datetime): Creation time of the task.
- `completed` (bool): Indicates whether the task is completed or not.

Each element of the list is a task (dictionary) with the above mentioned keys

---

## 📂 Project Structure

- `Class_ToDo_List.py`  
  Contains the `ToDo_List` class, which provides functions to:
  - Add, remove, modify, and check off tasks
  - Sort and filter tasks
  - Read/write tasks from/to CSV files

- `Program_ToDo_List.py`  
  A CLI-based program using the `ToDo_List` class. Users can interactively:
  - Import tasks from a file or create a new list
  - Perform all task management operations
  - Save tasks back to a file

- `Demo.ipynb`  
  A Jupyter notebook to explore and test the `ToDo_List` class programmatically.

- `tasks.csv`  
  An example task file in CSV format. Can be loaded to test functionality.

- `requirements.txt`  
  Lists required Python packages (for `pip` users).

- `environment.yaml`  
  Defines a conda environment for easier setup.

---

## 🚀 How to Run

### Option 1: Using Conda

```bash
conda env create -f environment.yaml
conda activate task_manager_env
python Program_ToDo_List.py
```

### Option 2: Using Pip

```bash
pip install -r requirements.txt
python Program_ToDo_List.py
```

---

## 📋 Features

- Add and remove tasks
- Modify task attributes (`title`, `due_date`, `due_time`, `priority`)
- Mark tasks as completed
- View tasks with sorting (e.g., by due date or priority) and filtering (e.g., completed, high priority)
- Store task data in a CSV file

---

## 🛠 Technologies Used

- `pandas` — for handling tabular task data
- `datetime`, `dateutil` — for parsing and managing date/time fields
- `csv`, `os`, `typing` — for file and type operations

---

## 👩‍🔬 Demo & Testing

Use `Demo.ipynb` to interactively test and validate the class methods with preloaded test cases and assertions.

---

## 📎 License

This project is open-source and free to use.

---

## 🙋‍♂️ Author

**Arya Basak**  
Student | Python & ML Enthusiast  
Feel free to contribute, suggest improvements, or raise issues!
