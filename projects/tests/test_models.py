from django.test import TestCase
from mixer.backend.django import mixer
from django.utils import timezone
from datetime import timedelta
from datetime import datetime
from projects.models import Task


class TestModelsProjects(TestCase):

    def test_project_str_is_name(self):
        project = mixer.blend('projects.Project', name='Test Project')

        self.assertEqual(str(project), 'Test Project')

    def test_is_tasklist_empty_True(self):
        project = mixer.blend('projects.Project')

        self.assertTrue(project.is_tasklist_empty())

    def test_is_tasklist_empty_False(self):
        project = mixer.blend('projects.Project')
        task = mixer.blend('projects.Task')
        task.project = project
        task.save()

        self.assertFalse(project.is_tasklist_empty())

    def test_overdue_tasks_none(self):
        project = mixer.blend('projects.Project')
        due_date = datetime.now() + timedelta(hours=5)
        mixer.cycle(4).blend('projects.Task',
                             project=project, due_date=due_date)
        overdue_tasks = project.get_overdue_tasks()
        n_overdue_tasks = overdue_tasks.count()

        self.assertEqual(n_overdue_tasks, 0)

    def test_overdue_tasks_mixed(self):
        n_tasks_overdue = 2
        n_tasks_not_overdue = 3
        project = mixer.blend('projects.Project')
        due_date_yesterday = datetime.now() - timedelta(days=1)
        due_date_tomorrow = datetime.now() + timedelta(days=1)
        mixer.cycle(n_tasks_overdue).blend('projects.Task',
                                           project=project, due_date=due_date_yesterday)
        mixer.cycle(n_tasks_not_overdue).blend('projects.Task',
                                               project=project, due_date=due_date_tomorrow)
        overdue_tasks = project.get_overdue_tasks()
        n_overdue_tasks = overdue_tasks.count()

        self.assertEqual(n_overdue_tasks, n_tasks_overdue)


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

    def test_overdue_true_overdue(self):
        due_date = timezone.now() - timedelta(days=1)
        task = mixer.blend('projects.Task', completed=False, due_date=due_date)

        self.assertEqual(task.is_overdue(), True)

    def test_overdue_false_completed(self):
        due_date = timezone.now() - timedelta(days=1)
        task = mixer.blend('projects.Task', completed=True, due_date=due_date)

        self.assertEqual(task.is_overdue(), False)

    def test_overdue_false_tomorrow(self):
        due_date = timezone.now() + timedelta(days=1)
        task = mixer.blend('projects.Task', completed=True, due_date=due_date)

        self.assertEqual(task.is_overdue(), False)

    def test_completed_recently_true(self):
        completed_date = timezone.now() - Task.recently_completed_time + \
            timedelta(seconds=1)
        task = mixer.blend('projects.Task',
                           completed=True)
        task.completed_date = completed_date
        self.assertEqual(task.completed_recently(), True)

    def test_completed_recently_false(self):
        completed_date = timezone.now() - Task.recently_completed_time + \
            timedelta(seconds=-10)
        task = mixer.blend('projects.Task',
                           completed=True)
        task.completed_date = completed_date

        self.assertEqual(task.completed_recently(), False)

    def test_due_soon_true(self):
        due_date = timezone.now() + Task.due_soon_time + \
            timedelta(seconds=-10)
        task = mixer.blend('projects.Task',
                           due_date=due_date)

        self.assertEqual(task.due_soon(), True)

    def test_due_soon_false_completed(self):
        due_date = timezone.now() + Task.due_soon_time + \
            timedelta(seconds=-10)
        task = mixer.blend('projects.Task',
                           due_date=due_date,
                           completed=True)

        self.assertEqual(task.due_soon(), False)

    def test_due_soon_false_due_date_far(self):
        due_date = timezone.now() + Task.due_soon_time + \
            timedelta(seconds=+10)
        task = mixer.blend('projects.Task',
                           due_date=due_date)

        self.assertEqual(task.due_soon(), False)

    def test_due_soon_false_overdue(self):
        due_date = timezone.now() + timedelta(seconds=-10)
        task = mixer.blend('projects.Task',
                           due_date=due_date,
                           completed=False)

        self.assertEqual(task.due_soon(), False)
