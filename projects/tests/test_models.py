from django.test import TestCase
from mixer.backend.django import mixer
from django.utils import timezone
from datetime import timedelta
from datetime import datetime


class TestModelsProjects(TestCase):

    def test_project_str_is_name(self):
        project = mixer.blend('projects.Project', name='Test Project')
        self.assertEqual(str(project), 'Test Project')


class TestModelsTasks(TestCase):

    def test_task_str_is_name(self):
        task = mixer.blend('projects.Task', name='Test Task')
        self.assertEqual(str(task), 'Test Task')

    def test_toggling_complete_true_sets_completion_date(self):
        task = mixer.blend('projects.Task', completed=False)
        self.assertEqual(task.completed, False)
        self.assertEqual(task.completed_date, None)
        task.completed = True
        task.save()
        self.assertEqual(task.completed, True)
        self.assertAlmostEqual(task.completed_date,
                               timezone.now(), delta=timedelta(seconds=1))

    def test_toggling_complete_false_unsets_completion_date(self):
        task = mixer.blend('projects.Task', completed=True)
        self.assertEqual(task.completed, True)
        self.assertAlmostEqual(task.completed_date,
                               timezone.now(), delta=timedelta(seconds=1))
        task.completed = False
        task.save()
        self.assertEqual(task.completed, False)
        self.assertEqual(task.completed_date, None)
