# 📝 ToDo List CLI Application

A command-line ToDo list manager built with Python.  
This project allows users to manage tasks interactively through a CLI or programmatically using a class. Task data is saved in CSV format.

-----

## 🧠 How This Project Works

This project is a command-line based ToDo list manager that helps users create, manage, and organize tasks efficiently. Below is a detailed overview of how the core logic and components function:

---

### 📦 Data Structure

1. **Task Format**  
   Each task is stored as a **dictionary**, with attributes such as:
   - `id`: Unique integer identifier
   - `title`: Task title
   - `due_date`: Due date (`datetime.date`)
   - `due_time`: Due time (`datetime.time`)
   - `priority`: Priority level (`low`, `moderate`, `high`)
   - `created_at`: Timestamp when the task was created (`datetime.datetime`)
   - `completed`: Boolean indicating if task is done

2. **Task List**  
   All task dictionaries are stored in a **list** called `tasklist`, representing the entire ToDo list.

3. **ID Tracking**  
   The `id` values of all tasks are stored separately in a list called `ids`, to allow for quick validation of existing tasks.

---

### ⚙️ Supported Operations

The application supports the following task operations:

- ✅ **Add** a new task
- ❌ **Remove** an existing task
- ✏️ **Modify** attributes of a task
- ☑️ **Check off** a task as completed
- 👁️ **View** tasks with flexible filtering and sorting

---

### 📊 Task Viewing with Pandas

Tasks are converted into a **pandas DataFrame** for display. This allows for elegant viewing with built-in support for sorting and filtering.

---

### ➕ Adding Tasks

- Prompts the user to enter task details: title, due date, due time, and priority.
- Automatically assigns a unique `id` and sets the current timestamp as `created_at` (if not supplied).
- Performs datatype validation on each field and raises an error on mismatch.
- Appends the validated task to the `tasklist`.

---

### ❌ Removing Tasks

- Displays all tasks (categorized as overdue, pending, or completed).
- Asks the user to enter the `id` of the task to remove.
- Verifies if the given `id` exists.
- If valid, removes the task from `tasklist` and updates `ids`.

---

### ✏️ Modifying Tasks

- Displays all tasks grouped by status.
- Prompts for the task `id` and the attribute to modify.
- Checks if the task with the given `id` is present.
- Attributes that can be modified: `title`, `due_date`, `due_time`, `priority`.
- Asks for the new value, checks its type, and applies the update if valid.

---

### ☑️ Checking Off Tasks

- Displays all tasks grouped by category.
- Prompts the user for the `id` of the task to be marked as completed.
- Checks if the task is already marked.
- If not, updates the `completed` attribute to `True`.

---

### 🔍 Viewing Tasks

- Offers multiple **sorting options** (ascending/descending):
  - By due date
  - By priority
  - By completed status
  - By creation time

- Offers powerful **filtering options**:
  - By priority (`low`, `moderate`, `high`)
  - By status: overdue, pending, or completed
  - Tasks due **by today**

---

### 📥 Importing from CSV

- The app can load tasks from a CSV file.
- Expects the same structure and headers as the task attributes.
- Parses date and time fields into Python datetime objects.

---

### 💾 Saving to CSV

- Tasks can be saved back to a CSV file after modifications.
- Ensures all task data is written with consistent structure and formatting.

---

### 🎨 Enhanced CLI with Colorama

The **Colorama** library is used to colorize console outputs. This improves user experience by:
- Highlighting success/error messages
- Differentiating task types
- Making the interface visually appealing and easier to use

-----

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

## 🛠 Technologies Used

- `pandas` — for handling tabular task data
- `datetime`, `dateutil` — for parsing and managing date/time fields
- `csv`, `os`, `typing` — for file and type operations
- `colorama` - for coloured output (text) on the terminal 

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