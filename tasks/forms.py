from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description']

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if not title:
            raise forms.ValidationError("Title cannot be empty")
        if len(title) < 3:
            raise forms.ValidationError("Title must be at least 3 characters")
        return title
