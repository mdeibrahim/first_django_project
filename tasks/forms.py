from django import forms
from tasks.models import Task

class TaskModelForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = '__all__'
        # fields = ['title', 'description', 'completed']
