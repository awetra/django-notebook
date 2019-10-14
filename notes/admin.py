from django.contrib import admin

from .models import Note, Task, Category


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Task._meta.fields]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Category._meta.fields]


class TaskInline(admin.TabularInline):
    model = Task
    extra = 0


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Note._meta.fields]
    inlines = (TaskInline,)
    prepopulated_fields = {'slug': ('title',)}