from django.db import models
from django.utils import timezone
from datetime import timedelta
from taggit.managers import TaggableManager


class Project(models.Model):
    """ A large project composed of many sub-tasks
    """
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    tags = TaggableManager(blank=True)
    completed = models.BooleanField(default=False)

    created_date = models.DateField(auto_now_add=True)
    due_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.name

    def is_tasklist_empty(self):
        return len(self.task_set)


class Task(models.Model):
    """ An individual self-contained task
    """
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    tags = TaggableManager(blank=True)
    completed = models.BooleanField(default=False)

    created_date = models.DateField(auto_now_add=True)
    due_date = models.DateTimeField(blank=True, null=True)
    completed_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Set the completion date when we complete
        if self.completed == True:
            self.completed_date = timezone.now()
        else:
            self.completed_date = None
        super().save(*args, **kwargs)

    def is_overdue(self):
        if self.due_date is not None:
            if not self.completed:
                if timezone.now() > self.due_date:
                    return True
        return False

    def completed_recently(self):
        if self.completed:
            if timezone.now() - timedelta(days=1) < self.completed_date:
                return True
        return False
