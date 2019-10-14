from django import forms

from .models import Note, Task


class NoteForm(forms.ModelForm):

    class Meta:
        model = Note
        fields = ('title',)


class TaskForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = ('text', 'category')