from django import forms
from .models import Task, TaskFile, Tag, TaskGroup


class TaskForm(forms.ModelForm):
    tag = forms.ModelChoiceField(
        queryset=Tag.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    file = forms.FileField(required=False)

    due_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model = Task
        fields = ['name', 'description', 'group', 'due_date', 'urgency_level', 'tag', 'is_completed']


class TaskGroupForm(forms.ModelForm):

    class Meta:
        model = TaskGroup
        fields = ['name', 'description']
