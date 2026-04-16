import json
import os
import csv
from datetime import datetime, date, timedelta
from typing import List


class Task:
    _next_id = 1

    def __init__(self, title, due_date, description="", priority=2, category="Личное"):
        self.id = Task._next_id
        Task._next_id += 1

        self.title = title
        self.description = description
        self.due_date = due_date
        self.priority = priority
        self.category = category
        self.created_at = datetime.now()
        self.completed = False

    def days_left(self):
        return (self.due_date - date.today()).days

    def is_overdue(self):
        return self.due_date < date.today() and not self.completed

    def is_today(self):
        return self.due_date == date.today()

    def is_urgent(self):
        return 0 <= self.days_left() <= 3 and not self.completed

    def status(self):
        if self.completed:
            return "✅"
        if self.is_overdue():
            return "❌"
        if self.is_today():
            return "📅"
        if self.is_urgent():
            return "⚠️"
        return "🕒"

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "due_date": self.due_date.strftime("%Y-%m-%d"),
            "priority": self.priority,
            "category": self.category,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "completed": self.completed
        }

    @classmethod
    def from_dict(cls, d):
        t = cls(
            d["title"],
            datetime.strptime(d["due_date"], "%Y-%m-%d").date(),
            d.get("description", ""),
            d.get("priority", 2),
            d.get("category", "Личное")
        )
        t.id = d["id"]
        t.created_at = datetime.strptime(d["created_at"], "%Y-%m-%d %H:%M:%S")
        t.completed = d.get("completed", False)

        if t.id >= cls._next_id:
            cls._next_id = t.id + 1

        return t

    def __str__(self):
        return f"{self.id}. {self.status()} {self.title} ({self.category})"


class TaskTracker:
    def __init__(self, file="tasks.json"):
        self.file = file
        self.tasks: List[Task] = []
        self.load()

    def add_task(self, title, due_date, description="", priority=2, category="Личное"):
        self.tasks.append(Task(title, due_date, description, priority, category))
        self.save()

    def delete_task(self, task_id):
        self.tasks = [t for t in self.tasks if t.id != task_id]
        self.save()

    def complete_task(self, task_id):
        for t in self.tasks:
            if t.id == task_id:
                t.completed = True
        self.save()

    def get_today(self):
        return [t for t in self.tasks if t.is_today() and not t.completed]

    def get_overdue(self):
        return [t for t in self.tasks if t.is_overdue()]

    def get_urgent(self):
        return [t for t in self.tasks if t.is_urgent()]

    def high_priority_urgent(self):
        return [t for t in self.tasks if t.priority == 3 and 0 <= t.days_left() <= 2]

    def weekly_report(self):
        today = date.today()
        week_ago = today - timedelta(days=7)
        next_week = today + timedelta(days=7)

        done = [t for t in self.tasks if t.completed and week_ago <= t.due_date <= today]
        upcoming = [t for t in self.tasks if today < t.due_date <= next_week and not t.completed]

        total = len(self.tasks)
        completed = len([t for t in self.tasks if t.completed])

        print("\n📊 ОТЧЕТ")
        print("Выполнено за неделю:", len(done))
        print("Планы на следующую неделю:")
        for t in upcoming:
            print("•", t.title)

        if total:
            print("Процент выполнения:", round(completed / total * 100, 1), "%")

    def export_csv(self):
        with open("tasks.csv", "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["ID", "Название", "Дата", "Приоритет", "Категория", "Статус"])
            for t in self.tasks:
                w.writerow([t.id, t.title, t.due_date, t.priority, t.category, t.completed])

    def save(self):
        with open(self.file, "w", encoding="utf-8") as f:
            json.dump([t.to_dict() for t in self.tasks], f, ensure_ascii=False, indent=2)

    def load(self):
        if not os.path.exists(self.file):
            self.create_demo()
            return
        with open(self.file, "r", encoding="utf-8") as f:
            data = json.load(f)
            self.tasks = [Task.from_dict(d) for d in data]

    def create_demo(self):
        today = date.today()
        self.add_task("Сдать лабораторную работу", today, priority=3)
        self.add_task("Подготовиться к экзамену", today + timedelta(days=2), priority=3)
        self.add_task("Сделать презентацию", today - timedelta(days=1), priority=2)

    def reminders(self):
        print("\n" + "=" * 60)
        print("📢 НАПОМИНАНИЯ")
        print("=" * 60)

        overdue = self.get_overdue()
        if overdue:
            print("\n❌ ПРОСРОЧЕННЫЕ:")
            for t in overdue:
                print("•", t.title, f"(+{abs(t.days_left())} дн.)")

        today = self.get_today()
        if today:
            print("\n📅 НА СЕГОДНЯ:")
            for t in today:
                print("•", t.title)

        urgent = self.get_urgent()
        if urgent:
            print("\n⚠️ СРОЧНЫЕ:")
            for t in urgent:
                print("•", t.title, f"({t.days_left()} дн.)")


def input_date():
    while True:
        s = input("Введите дату (дд.мм.гггг): ")
        try:
            return datetime.strptime(s, "%d.%m.%Y").date()
        except:
            print("Ошибка формата")


def menu():
    print("\n" + "=" * 50)
    print("📋 ТРЕКЕР ЗАДАЧ")
    print("=" * 50)
    print("1. Добавить")
    print("2. Все задачи")
    print("3. Сегодня")
    print("4. Срочные")
    print("5. Просроченные")
    print("6. Выполнить")
    print("7. Удалить")
    print("8. Напоминания")
    print("9. Статистика")
    print("10. Отчет")
    print("11. Важные срочные")
    print("12. Экспорт CSV")
    print("0. Выход")


def main():
    t = TaskTracker()

    print("=" * 60)
    print("ДОБРО ПОЖАЛОВАТЬ В ТРЕКЕР ЗАДАЧ!")
    print("=" * 60)

    t.reminders()

    while True:
        menu()
        c = input("Выбор: ")

        if c == "1":
            title = input("Название: ")
            d = input_date()
            p = int(input("Приоритет 1-3: "))
            cat = input("Категория: ")
            t.add_task(title, d, priority=p, category=cat)

        elif c == "2":
            for x in t.tasks:
                print(x)

        elif c == "3":
            for x in t.get_today():
                print(x)

        elif c == "4":
            for x in t.get_urgent():
                print(x)

        elif c == "5":
            for x in t.get_overdue():
                print(x)

        elif c == "6":
            t.complete_task(int(input("ID: ")))

        elif c == "7":
            t.delete_task(int(input("ID: ")))

        elif c == "8":
            t.reminders()

        elif c == "9":
            print("Всего:", len(t.tasks))
            print("Выполнено:", len([x for x in t.tasks if x.completed]))

        elif c == "10":
            t.weekly_report()

        elif c == "11":
            for x in t.high_priority_urgent():
                print(x)

        elif c == "12":
            t.export_csv()

        elif c == "0":
            break


if __name__ == "__main__":
    main()

"""

"""