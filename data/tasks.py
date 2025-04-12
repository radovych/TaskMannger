import json
import os
from datetime import datetime

TASKS_FILE_PATH = 'data/tasks.json'


# Завантаження задач з файлу
def load_tasks():
    if os.path.exists(TASKS_FILE_PATH):
        with open(TASKS_FILE_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []


# Збереження задач в файл
def save_tasks(tasks):
    with open(TASKS_FILE_PATH, 'w', encoding='utf-8') as f:
        json.dump(tasks, f, ensure_ascii=False, indent=4)


# Видалення задачі по id
def delete_task(task_id):
    tasks = load_tasks()
    tasks = [task for task in tasks if task["id"] != task_id]

    # Оновлення id після видалення задачі
    for index, task in enumerate(tasks):
        task["id"] = index + 1

    save_tasks(tasks)


# Оновлення статусу задачі (завершена/не завершена)
def update_task_status(task_id, completed):
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["completed"] = completed
            break
    save_tasks(tasks)


# Оновлення поля 'due_date' для задачі
def update_due_date(task_id, new_due_date):
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["due_date"] = new_due_date
            break
    save_tasks(tasks)


# Додавання нової задачі
def add_task(title, description, due_date, priority="low"):
    tasks = load_tasks()
    new_task = {
        "id": len(tasks) + 1,
        "title": title,
        "description": description,
        "completed": False,
        "due_date": due_date,
        "priority": priority
    }
    tasks.append(new_task)
    save_tasks(tasks)


# Перевірка задач на відповідність поточному часу
def check_overdue_tasks():
    tasks = load_tasks()
    now = datetime.now()

    overdue_tasks = []
    for task in tasks:
        # Формат дати "YYYY-MM-DD-HH:MM"
        try:
            due_datetime = datetime.strptime(task["due_date"], "%Y-%m-%d-%H:%M")
        except ValueError:
            print(f"⚠️ Некоректний формат дати у завданні: {task}")
            continue

        # Якщо задача прострочена і не завершена
        if now >= due_datetime and not task["completed"]:
            overdue_tasks.append(task)

    return overdue_tasks


# Пример задач
tasks = [
    {
        "id": 1,
        "title": "Випити вітаміни",
        "description": "Випити вітаміни після сніданку",
        "completed": False,
        "due_date": "2025-03-20-08:00",  # Додано час
        "priority": "low"
    },
    {
        "id": 2,
        "title": "Здати контрольну роботу",
        "description": "Завершити та завантажити контрольну роботу до системи",
        "completed": False,
        "due_date": "2025-03-21-23:59",  # Додано час
        "priority": "high"
    },
    {
        "id": 3,
        "title": "Вивчити вірш",
        "description": "Вивчити вірш до уроку літератури",
        "completed": False,
        "due_date": "2025-03-22-10:00",  # Додано час
        "priority": "medium"
    },
    {
        "id": 4,
        "title": "Зустріч з другом",
        "description": "Піти на каву о 17:00",
        "completed": False,
        "due_date": "2025-03-23-17:00",  # Додано час
        "priority": "low"
    }
]

# # Якщо tasks.json не існує, зберігаємо початкові дані
# if not os.path.exists(TASKS_FILE_PATH):
#     save_tasks(tasks)

# import json
# import os
#
# TASKS_FILE_PATH = 'data/tasks.json'
#
# def load_tasks():
#     if os.path.exists(TASKS_FILE_PATH):
#         with open(TASKS_FILE_PATH, 'r', encoding='utf-8') as f:
#             return json.load(f)
#     return []
#
# def save_tasks(tasks):
#     with open(TASKS_FILE_PATH, 'w', encoding='utf-8') as f:
#         json.dump(tasks, f, ensure_ascii=False, indent=4)
#
# def delete_task(task_id):
#     tasks = load_tasks()
#     tasks = [task for task in tasks if task["id"] != task_id]
#
#     #Онов id після видалення 1.04
#     for index, task in enumerate(tasks):
#         task["id"] = index + 1
#
#     save_tasks(tasks)
#
#
#
# tasks = [
#     {
#         "id": 1,
#         "title": "Випити вітаміни",
#         "description": "Випити вітаміни після сніданку",
#         "completed": False,
#         "due_date": "2025-03-20-08:00",  # Додано час
#         "priority": "low"
#     },
#     {
#         "id": 2,
#         "title": "Здати контрольну роботу",
#         "description": "Завершити та завантажити контрольну роботу до системи",
#         "completed": False,
#         "due_date": "2025-03-21-23:59",  # Додано час
#         "priority": "high"
#     },
#     {
#         "id": 3,
#         "title": "Вивчити вірш",
#         "description": "Вивчити вірш до уроку літератури",
#         "completed": False,
#         "due_date": "2025-03-22-10:00",  # Додано час
#         "priority": "medium"
#     },
#     {
#         "id": 4,
#         "title": "Зустріч з другом",
#         "description": "Піти на каву о 17:00",
#         "completed": False,
#         "due_date": "2025-03-23-17:00",  # Додано час
#         "priority": "low"
#     }
# ]



# import json
# from datetime import datetime
#
# TASKS_FILE = "data/tasks.json"
#
# def get_tasks():
#     try:
#         with open(TASKS_FILE, "r", encoding="utf-8") as file:
#             tasks = json.load(file)
#         return tasks
#     except Exception as e:
#         print(f"Помилка при отриманні задач: {e}")
#         return []
#
# def update_overdue_tasks():
#     tasks = get_tasks()  # Отримуємо задачі
#     today = datetime.today().date()
#
#     for task in tasks:
#         due_date = datetime.strptime(task["due_date"], "%Y-%m-%d").date()
#         task["overdue"] = due_date < today
#
#     with open(TASKS_FILE, "w", encoding="utf-8") as file:
#         json.dump(tasks, file, indent=4, ensure_ascii=False)


