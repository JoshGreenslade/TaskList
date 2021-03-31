from django.test import TestCase
from django.urls import reverse
from mixer.backend.django import mixer


class TestViewsProjectsUnpopulated(TestCase):

    def get_response(self, view_name):
        path = reverse(view_name)
        response = self.client.get(path)
        return response

    def test_no_projects(self):
        response = self.get_response('index')

        self.assertContains(
            response, 'Use the button at the top to create a project.')

    def test_project_no_tasks(self):
        project = mixer.blend('projects.Project', name='Test Project')
        response = self.get_response('index')

        self.assertContains(response, '<p>No tasks found</p>')

    def test_project_tasks(self):
        project = mixer.blend('projects.Project', name='Test Project')
        task = mixer.blend('projects.Task', project=project, name='Test Task')
        response = self.get_response('index')

        self.assertContains(response, 'Test Task')
