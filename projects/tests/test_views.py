from django.test import TestCase
from django.urls import reverse
from mixer.backend.django import mixer
import json

class TestViewsProjects(TestCase):

    def get_response(self, view_name):
        path = reverse(view_name)
        response = self.client.get(path)
        return response

    def post_response(self, view_name, data):
        path = reverse(view_name)
        response = self.client.post(path, data=data)
        return response

    ###################################
    #  Project Index
    ###################################
    def test_project_list(self):
        response = self.get_response('projects:project_list')

        self.assertEqual(response.status_code, 200)

    def test_project_list_empty(self):
        response = self.get_response('projects:project_list')

        self.assertContains(response, 'To create a new project, click the button in the navbar.')

    def test_project_list_project(self):
        project_name = 'Test Project'
        
        project = mixer.blend('projects.Project', name=project_name)
        response = self.get_response('projects:project_list')

        self.assertContains(response, project_name)

    ###################################
    #  Project create
    ###################################
    def test_project_create_GET(self):
        expected_response_contains = '<form method="post" action="/projects/create/" class="js-project-create-form">'
        
        response = self.get_response('projects:project_create')
        json_response = json.loads(response.content)

        self.assertIn(expected_response_contains, json_response['html_form'])

    def test_project_create_POST(self):
        expected_response_contains_1 = '<button class="btn btn-outline-dark js-update-project" data-url="/projects/1/update">'
        expected_response_contains_2 = 'Test Project'
        
        
        data = {'name': expected_response_contains_2}

        response = self.post_response('projects:project_create', data=data)
        json_response = json.loads(response.content)

        self.assertTrue(json_response['form_is_valid'], json_response['html_form'])
        self.assertTrue(json_response['html_project_list'])
        self.assertIn(expected_response_contains_1, json_response['html_project_list'])
        self.assertIn(expected_response_contains_2, json_response['html_project_list'])

    ###################################
    #  Project update
    ###################################
    def test_project_update_GET(self):
        expected_response_contains = '<form method="post" action="/projects/1/update" class="js-project-update-form">'
        
        project = mixer.blend('projects.Project')
        path = reverse('projects:project_update', args=[1])
        response = self.client.get(path)
        json_response = json.loads(response.content)

        self.assertIn(expected_response_contains, json_response['html_form'])

    def test_project_update_POST(self):
        project_old_name = 'Old Test Project'
        project_new_name = 'New Test Project'

        project = mixer.blend('projects.Project', name=project_old_name)
        path = reverse('projects:project_update', args=[1])
        data = {'name': project_new_name}
        response = self.client.post(path, data=data)
        json_response = json.loads(response.content)

        self.assertTrue(json_response['form_is_valid'], json_response['html_form'])
        self.assertTrue(json_response['html_project_list'])
        self.assertNotIn(project_old_name, json_response['html_project_list'])
        self.assertIn(project_new_name, json_response['html_project_list'])

    ###################################
    #  Project Delete
    ###################################
    def test_project_delete(self):        
        project_name = 'My test project'

        project = mixer.blend('projects.Project')
        path = reverse('projects:project_delete', args=[1])
        response = self.client.get(path)
        json_response = json.loads(response.content)

        self.assertTrue(json_response['html_project_list'])
        self.assertNotIn(project_name, json_response['html_project_list'])

    ###################################
    #  Task create
    ###################################
    def test_task_create_GET(self):
        expected_response_contains = '<form method="post" action="/projects/1/update" class="js-project-update-form">'
        
        project = mixer.blend('projects.Project')
        path = reverse('projects:project_update', args=[1])
        response = self.client.get(path)
        json_response = json.loads(response.content)

        self.assertIn(expected_response_contains, json_response['html_form'])
