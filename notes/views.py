from django.views.generic import ListView, DetailView, CreateView, DeleteView
from django.http import Http404
from django.urls import reverse_lazy
from django.shortcuts import redirect

from .models import Note, Task
from .forms import NoteForm, TaskForm


class NoteList(ListView):

    model = Note
    template_name = 'notes/notes_list.html'
    context_object_name = 'notes'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return self.model.objects.filter(user=self.request.user)


class NoteDetail(DetailView):

    model = Note
    context_object_name = 'note'

    def get_object(self):
        note = super().get_object()

        if note.user != self.request.user:
            raise Http404
        return note

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['form'] = TaskForm()

        all_note_tasks = context_data['note'].tasks.all()

        tasks = []
        for category in ('Yellow', 'Red', 'Green', 'Black'):
            tasks += list(all_note_tasks.filter(category__name__iexact=category))

        context_data['tasks'] = tasks

        return context_data

    def post(self, request, **kwargs):
        form = TaskForm(request.POST)
        note = self.get_object()
        
        if form.is_valid():
            task = form.save()
            task.note = note
            task.save()

        return redirect('note_detail', slug=note.slug)


class NoteCreate(CreateView):

    form_class = NoteForm
    template_name = 'notes/note_create.html'

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        return super().form_valid(form)


class NoteDelete(DeleteView):

    model = Note
    success_url = reverse_lazy('notes_list')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def get_objects(self, queryset=None):
        obj = super().get_objects()
        
        if obj.user != self.request.user:
            raise Http404
        return obj


class TaskDelete(DeleteView):

    model = Task

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def get_objects(self, queryset=None):
        task = super().get_objects()

        if task != self.request.user:
            raise Http404
        return task

    def get_success_url(self):
        return self.get_object().note.get_absolute_url()
