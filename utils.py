from datetime import datetime

def validate_deadline(deadline_str):
    try:
        # Перевірка, чи є введений дедлайн коректним
        datetime.strptime(deadline_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False
