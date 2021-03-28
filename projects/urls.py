from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path
from django.urls import re_path
from . import views

app_name = 'projects'
urlpatterns = [
    # path('', views.index, name='index'),
    # path('create_project/', views.create_project, name='create_project'),
    # path('add_task/', views.add_task, name='add_task'),
    # path('project/<int:pk>/', views.project, name='project'),
    re_path(r'^projects/$', views.project_list, name='project_list'),
    re_path(r'^projects/create/$', views.project_create, name='project_create'),
    path('projects/<int:pk>/update', views.project_update, name='project_update'),
    path('tasks/create/<int:project_pk>',
         views.task_create, name='task_create'),
    path('tasks/<int:pk>/update',
         views.task_update, name='task_update'),
    path('tasks/<int:pk>/toggle',
         views.task_toggle, name='task_toggle'),
]


urlpatterns += staticfiles_urlpatterns()
