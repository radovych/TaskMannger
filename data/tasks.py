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
        "due_date": "2025-03-20",
        "priority": "low"
    },
    {
        "id": 2,
        "title": "Здати контрольну роботу",
        "description": "Завершити та завантажити контрольну роботу до системи",
        "completed": False,
        "due_date": "2025-03-21",
        "priority": "high"
    },
    {
        "id": 3,
        "title": "Вивчити вірш",
        "description": "Вивчити вірш до уроку літератури",
        "completed": False,
        "due_date": "2025-03-22",
        "priority": "medium"
    },
    {
        "id": 4,
        "title": "Зустріч з другом",
        "description": "Піти на каву о 17:00",
        "completed": False,
        "due_date": "2025-03-23",
        "priority": "low"
    }
]

