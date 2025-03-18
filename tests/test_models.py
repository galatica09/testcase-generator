```python
import pytest
from django.utils import timezone
from testingapp2.models import Task

@pytest.fixture
def create_task():
    def _create_task(title="Test Task", description="Test description", completed=False):
        return Task.objects.create(title=title, description=description, completed=completed)
    return _create_task

def test_create_task(create_task):
    task = create_task()
    assert task.title == "Test Task"
    assert task.description == "Test description"
    assert task.completed == False
    assert task.created_at <= timezone.now()
    assert task.updated_at <= timezone.now()

def test_create_task_without_description(create_task):
    task = create_task(description="")
    assert task.description == ""

def test_create_task_completed(create_task):
    task = create_task(completed=True)
    assert task.completed == True

def test_create_task_with_long_title(create_task):
    long_title = "a" * 256
    with pytest.raises(Exception) as e:
        create_task(title=long_title)
    assert "value is too long" in str(e.value)


def test_str_representation(create_task):
    task = create_task()
    assert str(task) == "Test Task"

def test_update_task(create_task):
    task = create_task()
    original_updated_at = task.updated_at
    task.title = "Updated Task"
    task.save()
    assert task.title == "Updated Task"
    assert task.updated_at > original_updated_at


def test_update_task_completed_status(create_task):
    task = create_task()
    task.completed = True
    task.save()
    assert task.completed == True

def test_task_creation_with_invalid_title(create_task):
    with pytest.raises(Exception) as e:
        Task.objects.create(title=None)
    assert "This field cannot be blank." in str(e.value)

```