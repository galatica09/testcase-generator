```python
import pytest
from testingapp2.models import Task
from testingapp2.actions import mark_task_completed
from django.core.exceptions import ObjectDoesNotExist

# Fixtures
@pytest.fixture
def create_task(db):
    def _create_task(completed=False):
        task = Task.objects.create(description="Test Task", completed=completed)
        return task
    return _create_task


# Test Cases

def test_mark_task_completed_happy_path(create_task):
    task = create_task()
    updated_task = mark_task_completed(task.id)
    assert updated_task.completed is True
    assert updated_task.id == task.id


def test_mark_task_completed_task_not_found():
    with pytest.raises(ObjectDoesNotExist):
        mark_task_completed(9999) # Non-existent task ID


def test_mark_task_completed_already_completed(create_task):
    task = create_task(completed=True)
    updated_task = mark_task_completed(task.id)
    assert updated_task.completed is True
    assert updated_task.id == task.id

```