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

def test_task_serializer_happy_path(task_data):
    serializer = TaskSerializer(data=task_data)
    assert serializer.is_valid()
    assert serializer.validated_data == task_data
    instance = serializer.save()
    assert instance.title == task_data['title']
    assert instance.description == task_data['description']
    assert instance.completed == task_data['completed']


def test_task_serializer_missing_title(task_data):
    del task_data['title']
    serializer = TaskSerializer(data=task_data)
    assert not serializer.is_valid()
    assert 'title' in serializer.errors


def test_task_serializer_invalid_completed(task_data):
    task_data['completed'] = 'invalid'
    serializer = TaskSerializer(data=task_data)
    assert not serializer.is_valid()
    assert 'completed' in serializer.errors

def test_task_serializer_update(task):
    updated_data = {
        'title': 'Updated Task',
        'description': 'This is an updated task.',
        'completed': True,
    }
    serializer = TaskSerializer(instance=task, data=updated_data)
    assert serializer.is_valid()
    updated_task = serializer.save()
    assert updated_task.title == updated_data['title']
    assert updated_task.description == updated_data['description']
    assert updated_task.completed == updated_data['completed']


def test_task_serializer_empty_data():
    serializer = TaskSerializer(data={})
    assert not serializer.is_valid()
    assert 'title' in serializer.errors
    assert 'description' in serializer.errors
    assert 'completed' in serializer.errors

```