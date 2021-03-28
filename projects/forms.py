from django import forms
from .models import Project
from .models import Task


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'tags', 'due_date']


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['project', 'name', 'description',
                  'tags', 'due_date']
        exclude = ("project",)

        widgets = {
            'due_date': forms.widgets.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
