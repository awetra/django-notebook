from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

from pytils.translit import slugify


class Note(models.Model):
    
    title = models.CharField(max_length=150, blank=True, null=True)
    slug = models.SlugField(max_length=150, blank=True, null=True)
    created = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('note_detail', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('note_delete', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.title:
            self.title = datetime.now().strftime('%d-%m-%Y')

        self.slug = slugify(self.title)

        user_notes = Note.objects.filter(user=self.user, slug=self.slug)
        if user_notes:
            self.slug += '-' + str(user_notes.count() + 1)
        super().save(*args, **kwargs)


class Category(models.Model):
    
    name = models.CharField(max_length=150, blank=True, null=True)
    color = models.CharField(max_length=7, help_text='Enter the color as #ff0000')

    def __str__(self):
        if self.name:
            return '%s - %s' % (self.name, self.color)
        return self.color


class Task(models.Model):
    
    text = models.TextField(max_length=500)
    note = models.ForeignKey(Note, blank=True, null=True, on_delete=models.CASCADE, related_name='tasks')
    category = models.ForeignKey(Category, blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return '%s - %s' % (self.note.title, self.category)

    def get_delete_url(self):
        return reverse('task_delete', kwargs={'pk': self.id, 'slug': self.note.slug})