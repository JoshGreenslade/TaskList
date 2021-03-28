from django.contrib import admin
from .models import Project
from .models import Task

# Register your models here.


class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'project',  'created_date',
                    'due_date', 'completed')
    list_editable = ('completed',)


admin.site.register(Project)
admin.site.register(Task, TaskAdmin)
