from django import forms
from .models import *


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Board
        fields = ["name"]


class ColumnForm(forms.ModelForm):
    class Meta:
        model = BoardColumn
        fields = ["name"]