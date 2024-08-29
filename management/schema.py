from ninja import Schema, ModelSchema
from .models import *
from typing import List, Optional

# Unused
"""class UserSchemaIn(Schema):
    first_name: str
    last_name: str
    username: str
    password: str


class UserSchemaOut(Schema):
    id: int
    first_name: str
    last_name: str
    username: str"""

class ColumnUpdateSchema(ModelSchema):
    class Meta:
        model = BoardColumn
        fields = ["name", "id"]
        fields_optional = ["id"]


class BoardUpdateSchema(ModelSchema):
    columns: Optional[List[ColumnUpdateSchema]] = None

    class Meta:
        model = Board
        fields = "__all__"
        exclude = ["slug"]


class SubtaskUpdateSchema(ModelSchema):
    class Meta:
        model = Subtask
        fields = ["title", "id"]
        fields_optional = ["id"]

class TaskUpdateSchema(ModelSchema):
    subtasks: Optional[List[SubtaskUpdateSchema]] = None
    class Meta:
        model = Task
        fields = "__all__"
        exclude = ["is_completed"]


class ColumnSchemaIn(ModelSchema):
    class Meta:
        model = BoardColumn
        fields = ["name"]


class BoardSchemaIn(ModelSchema):
    columns: Optional[List[ColumnSchemaIn]] = None

    class Meta:
        model = Board
        fields = "__all__"
        exclude = ["id", "slug"]


class SubTaskSchemaIn(ModelSchema):
    class Meta:
        model = Subtask
        fields = "__all__"
        fields_optional = ["task_parent"]
        exclude = ["is_completed", "id"]


class SubTaskSchema(Schema):
    title: str


class TaskSchemaIn(ModelSchema):
    subtasks: Optional[List[SubTaskSchema]] = None

    class Meta:
        model = Task
        fields = "__all__"
        fields_optional = ["description"]
        exclude = ["id", "is_completed"]


class SubTaskSchemaOut(ModelSchema):
    class Meta:
        model = Subtask
        fields = "__all__"


class TaskSchemaOut(ModelSchema):
    subtasks: List[SubTaskSchemaOut] = None

    class Meta:
        model = Task
        fields = "__all__"


class ColumnSchemaOut(ModelSchema):
    tasks: List[TaskSchemaOut] = None

    class Meta:
        model = BoardColumn
        fields = "__all__"


class BoardSchemaOut(ModelSchema):
    columns: List[ColumnSchemaOut] = None

    class Meta:
        model = Board
        fields = "__all__"