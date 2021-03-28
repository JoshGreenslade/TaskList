from django.test import TestCase
from django.urls import reverse


class TestUrlsProjects(TestCase):

    def test_project_index(self):
        path = reverse('index')
        response = self.client.get(path)
        self.assertEqual(response.status_code, 200)
