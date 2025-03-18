```python
import pytest
from rest_framework import status
from rest_framework.test import APIClient
from testingapp2.models import Task

pytestmark = pytest.mark.django_db

@pytest.fixture
def create_task():
    def _create_task(title="Test Task", completed=False):
        return Task.objects.create(title=title, completed=completed)
    return _create_task

@pytest.fixture
def api_client():
    return APIClient()

def test_task_create(api_client, create_task):
    data = {'title': 'New Task'}
    response = api_client.post('/tasks/', data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert Task.objects.count() == 1
    assert Task.objects.get(title='New Task').completed == False

def test_task_create_missing_title(api_client):
    data = {}
    response = api_client.post('/tasks/', data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_task_retrieve(api_client, create_task):
    task = create_task()
    response = api_client.get(f'/tasks/{task.pk}/')
    assert response.status_code == status.HTTP_200_OK
    assert response.data['title'] == task.title

def test_task_retrieve_not_found(api_client):
    response = api_client.get('/tasks/999/')
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_task_complete(api_client, create_task):
    task = create_task()
    response = api_client.post(f'/tasks/{task.pk}/complete/')
    assert response.status_code == status.HTTP_200_OK
    assert response.data['status'] == 'Task marked as completed'
    task.refresh_from_db()
    assert task.completed is True

def test_task_complete_not_found(api_client):
    response = api_client.post('/tasks/999/complete/')
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_task_update(api_client, create_task):
    task = create_task()
    data = {'title': 'Updated Task', 'completed': True}
    response = api_client.put(f'/tasks/{task.pk}/', data, format='json')
    assert response.status_code == status.HTTP_200_OK
    task.refresh_from_db()
    assert task.title == 'Updated Task'
    assert task.completed is True

def test_task_update_missing_title(api_client, create_task):
    task = create_task()
    data = {'completed': True}
    response = api_client.put(f'/tasks/{task.pk}/', data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_task_delete(api_client, create_task):
    task = create_task()
    response = api_client.delete(f'/tasks/{task.pk}/')
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Task.objects.count() == 0


def test_task_delete_not_found(api_client):
    response = api_client.delete('/tasks/999/')
    assert response.status_code == status.HTTP_404_NOT_FOUND

```