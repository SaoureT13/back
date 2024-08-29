from django.core.management.base import BaseCommand
import json
from management.models import *


class Command(BaseCommand):
    held = "Seed database with data in json file"

    def handle(self, *args, **options):
        with open("management/data.json") as json_file:
            data = json.load(json_file)
            for board in data["boards"]:
                b = Board.objects.create(name=board["name"])
                # print(f"Board name: {board["name"]}")
                # print(board["columns"])
                for column in board["columns"]:
                    c = BoardColumn.objects.create(name=column["name"], color=column["color"], board=b)
                    # print(f"Board column name: {column["name"]}")

                    for task in column["tasks"]:
                        # print(f"Column task name: {task["title"]}")

                        t = Task.objects.create(
                            title=task["title"],
                            description=task["description"] if task["description"] else None,
                            board_column=c,
                        )

                        if task["subtasks"]:
                            for subtask in task["subtasks"]:
                                # print(f"Column task, subtasks number: {len(task["subtasks"])}")

                                subtask = Subtask.objects.create(
                                    title=subtask["title"],
                                    is_completed=subtask["isCompleted"],
                                    task_parent=t
                                )
                # print("\n")
