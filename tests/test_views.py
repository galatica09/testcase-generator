```python
import pytest
from rest_framework import status
from rest_framework.test import APIClient
from testingapp2.models import Task

pytestmark = pytest.mark.django_db

@pytest.fixture
def create_task():
    def _create_task(description="Test Task", completed=False):
        task = Task.objects.create(description=description, completed=completed)
        return task
    return _create_task

@pytest.fixture
def api_client():
    return APIClient()

def test_task_create(api_client, create_task):
    url = '/tasks/'
    data = {'description': 'Test Task from API'}
    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert Task.objects.count() == 1
    assert Task.objects.get().description == data['description']

def test_task_create_missing_data(api_client):
    url = '/tasks/'
    data = {}
    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST

def test_task_retrieve(api_client, create_task):
    task = create_task()
    url = f'/tasks/{task.id}/'
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['id'] == task.id
    assert response.data['description'] == task.description

def test_task_retrieve_not_found(api_client):
    url = '/tasks/999/'
    response = api_client.get(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_task_complete(api_client, create_task):
    task = create_task()
    url = f'/tasks/{task.id}/complete/'
    response = api_client.post(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['status'] == 'Task marked as completed'
    task.refresh_from_db()
    assert task.completed is True

def test_task_complete_not_found(api_client):
    url = '/tasks/999/complete/'
    response = api_client.post(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_task_update(api_client, create_task):
    task = create_task()
    url = f'/tasks/{task.id}/'
    new_description = "Updated Task Description"
    response = api_client.patch(url, {'description': new_description}, format='json')
    assert response.status_code == status.HTTP_200_OK
    task.refresh_from_db()
    assert task.description == new_description

def test_task_delete(api_client, create_task):
    task = create_task()
    url = f'/tasks/{task.id}/'
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Task.objects.count() == 0

def test_task_delete_not_found(api_client):
    url = '/tasks/999/'
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND
```