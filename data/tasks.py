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


