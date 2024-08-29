import random
from django.shortcuts import get_object_or_404

from .models import *
from ninja import NinjaAPI, Form
from typing import List
from .schema import *
from .forms import *

api = NinjaAPI()


def generate_hex_color():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return f'#{r:02x}{g:02x}{b:02x}'


@api.get("/all_boards", response=List[BoardSchemaOut])
def get_boards(request):
    queryset = Board.objects.all().prefetch_related("columns")
    return list(queryset)


@api.post('/create_board', response=BoardSchemaOut)
def create_board(request, payload: BoardSchemaIn):
    board = Board.objects.create(name=payload.name)
    for column in payload.columns:
        color = generate_hex_color()
        BoardColumn.objects.create(name=column.name, color=color, board=board)

    return board

#Update board name and board columns(name)
@api.put("/update_board", response=BoardSchemaOut)
def update_board(request, payload: BoardUpdateSchema):
    board = get_object_or_404(Board, pk=payload.id)
    board.name = payload.name.capitalize()
    board.save()

    if payload.columns:
        column_id_list = [column.id for column in payload.columns if column.id and column.id is not None]

        board.columns.exclude(id__in=column_id_list).delete()

        for column_data in payload.columns:
            if column_data.id is not None:
                column = get_object_or_404(BoardColumn, pk=column_data.id)
                column.name = column_data.name.capitalize()
                column.save()
            else:
                BoardColumn.objects.create(name=column_data.name.capitalize(), board=board, color=generate_hex_color())
    else:
        board.columns.all().delete()

    return board


@api.delete("/delete_board")
def delete_board(request, board_id: int):
    board = get_object_or_404(Board, pk=board_id)
    board.delete()

    return {"success": True}

#Mark task as completed
@api.put("/update_subtask")
def update_subtask(request, subtask_id: int):
    subtask = get_object_or_404(Subtask, pk=subtask_id)
    subtask.is_completed = not subtask.is_completed
    subtask.save()

    task = get_object_or_404(Task, pk=subtask.task_parent_id)
    if all(subtask.is_completed for subtask in task.subtasks.all()):
        task.is_completed = True
    else:
        task.is_completed = False
    task.save()

    return {"success": True, "task": {"is_completed": task.is_completed, "id": task.id}}

@api.post("/create_task", response=TaskSchemaOut)
def create_task(request, payload: TaskSchemaIn):
    print(payload)
    column = get_object_or_404(BoardColumn, pk=payload.board_column)

    if column:
        new_task = Task.objects.create(title=payload.title, board_column=column)
        if payload.description and not payload.description.lower() == "string":
            new_task.description = payload.description
        new_task.save()

        if payload.subtasks and len(payload.subtasks) > 0:
            for subtask in payload.subtasks:
                new_sub_task = Subtask.objects.create(title=subtask.title, task_parent_id=new_task.id)
                new_sub_task.save()

        return new_task

    return api.create_response(request, {"errors": "Status(column) not found"}, status=400)

#Change column of task
@api.put("/update_task_column", response=TaskSchemaOut)
def update_task_column(request, task_id: int, column_id: int):
    task = get_object_or_404(Task, pk=task_id)
    board_column = get_object_or_404(BoardColumn, pk=column_id)

    task.board_column = board_column
    task.save()
    return task

@api.delete("/delete_task")
def delete_task(request, task_id:int):
    task = get_object_or_404(Task, pk=task_id)
    task.delete()

    return {"success": True}


@api.put("/update_task", response=TaskSchemaOut)
def update_task(request, payload: TaskUpdateSchema):
    task = get_object_or_404(Task, pk=payload.id)
    board_column = get_object_or_404(BoardColumn, pk=payload.board_column)
    task.title = payload.title
    if payload.description and payload.description is not None:
        task.description = payload.description
    task.board_column = board_column
    task.save()

    if payload.subtasks:
        task_id_list = [subtask.id for subtask in payload.subtasks if subtask.id and subtask.id is not None]

        task.subtasks.exclude(id__in=task_id_list).delete()

        for subtask_data in payload.subtasks:
            if subtask_data.id is not None:
                subtask = get_object_or_404(Subtask, pk=subtask_data.id)
                subtask.title = subtask_data.title
                subtask.save()
            else:
                Subtask.objects.create(title=subtask_data.title, task_parent=task)
    else:
        task.subtasks.all().delete()

    return task