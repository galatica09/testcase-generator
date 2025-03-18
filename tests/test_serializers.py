```python
import pytest
from rest_framework import serializers
from testingapp2.models import Task
from testingapp2.serializers import TaskSerializer

pytestmark = pytest.mark.django_db

@pytest.fixture
def task_data():
    return {
        'title': 'Test Task',
        'description': 'This is a test task.',
        'completed': False,
    }

@pytest.fixture
def task(task_data):
    return Task.objects.create(**task_data)


def test_task_serializer_happy_path(task, task_data):
    serializer = TaskSerializer(task)
    assert serializer.data == task_data

def test_task_serializer_create_happy_path(task_data):
    serializer = TaskSerializer(data=task_data)
    assert serializer.is_valid() == True
    task_instance = serializer.save()
    assert task_instance.title == task_data['title']
    assert task_instance.description == task_data['description']
    assert task_instance.completed == task_data['completed']


def test_task_serializer_update_happy_path(task, task_data):
    new_data = {
        'title': 'Updated Task',
        'description': 'This is an updated task.',
        'completed': True,
    }
    serializer = TaskSerializer(task, data=new_data)
    assert serializer.is_valid() == True
    updated_task = serializer.save()
    assert updated_task.title == new_data['title']
    assert updated_task.description == new_data['description']
    assert updated_task.completed == new_data['completed']


def test_task_serializer_missing_title(task_data):
    missing_title_data = {
        'description': 'Missing title',
        'completed': False,
    }
    serializer = TaskSerializer(data=missing_title_data)
    assert serializer.is_valid() == False
    assert 'title' in serializer.errors

def test_task_serializer_invalid_completed_field(task_data):
    invalid_completed_data = {
        'title': 'Invalid Completed',
        'description': 'Test',
        'completed': 'yes', #Invalid, should be boolean
    }
    serializer = TaskSerializer(data=invalid_completed_data)
    assert serializer.is_valid() == False
    assert 'completed' in serializer.errors

def test_task_serializer_empty_data():
    serializer = TaskSerializer(data={})
    assert serializer.is_valid() == False
    assert len(serializer.errors) > 0

```