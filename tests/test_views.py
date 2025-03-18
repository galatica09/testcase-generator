```python
import pytest
from rest_framework import status
from rest_framework.test import APIClient
from testingapp2.models import Task

pytestmark = pytest.mark.django_db

@pytest.fixture
def create_task():
    def _create_task(description="Test Task", completed=False):
        return Task.objects.create(description=description, completed=completed)
    return _create_task

@pytest.fixture
def api_client():
    return APIClient()

def test_task_creation(api_client, create_task):
    data = {'description': 'New Task'}
    response = api_client.post('/tasks/', data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert Task.objects.count() == 1
    assert Task.objects.get(description='New Task').completed == False

def test_task_creation_missing_data(api_client):
    response = api_client.post('/tasks/', {}, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_mark_task_complete(api_client, create_task):
    task = create_task()
    url = f'/tasks/{task.id}/complete/'
    response = api_client.post(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'status': 'Task marked as completed'}
    task.refresh_from_db()
    assert task.completed is True

def test_mark_task_complete_not_found(api_client):
    url = '/tasks/999/complete/'  # Non-existent task ID
    response = api_client.post(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_list_tasks(api_client, create_task):
    create_task()
    create_task(description="Another Task")
    response = api_client.get('/tasks/')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 2

def test_retrieve_task(api_client, create_task):
    task = create_task()
    response = api_client.get(f'/tasks/{task.id}/')
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['description'] == task.description


def test_update_task(api_client, create_task):
    task = create_task()
    data = {'description': 'Updated Task Description'}
    response = api_client.put(f'/tasks/{task.id}/', data, format='json')
    assert response.status_code == status.HTTP_200_OK
    task.refresh_from_db()
    assert task.description == 'Updated Task Description'

def test_delete_task(api_client, create_task):
    task = create_task()
    response = api_client.delete(f'/tasks/{task.id}/')
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Task.objects.count() == 0

def test_delete_task_not_found(api_client):
    response = api_client.delete('/tasks/999/')
    assert response.status_code == status.HTTP_404_NOT_FOUND

```