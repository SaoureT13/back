from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify


class Board(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Board, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class BoardColumn(models.Model):
    name = models.CharField(max_length=255)
    color = models.CharField(max_length=100, null=True)
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='columns')


class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255, null=True, blank=True)
    board_column = models.ForeignKey(BoardColumn, on_delete=models.CASCADE, related_name='tasks')
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} - {self.description[15]}"


class Subtask(models.Model):
    title = models.CharField(max_length=255)
    task_parent = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='subtasks')
    is_completed = models.BooleanField(default=False)

    # def save(self, *args, **kwargs):
    #     parent_subtasks = self.task_parent.subtasks.all()
    #
    #     if all(subtask.is_completed for subtask in parent_subtasks):
    #         self.task_parent.is_completed = True
    #         self.task_parent.save()
    #
    #     super(Subtask, self).save(*args, **kwargs)

    def __str__(self):
        return self.title