# Generated by Django 3.1.7 on 2021-03-21 21:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_auto_20210321_2058'),
    ]

    operations = [
        migrations.RenameField(
            model_name='task',
            old_name='completd',
            new_name='completed',
        ),
    ]
