from django import forms
from .models import Task, TaskFile, Tag, TaskGroup


class TaskForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )
    file = forms.FileField(required=False)

    class Meta:
        model = Task
        fields = ['name', 'description', 'group', 'due_date', 'urgency_level', 'tags', 'is_completed']


class TaskGroupForm(forms.ModelForm):

    class Meta:
        model = TaskGroup
        fields = ['name', 'description']
