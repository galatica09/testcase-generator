```python
import pytest
from testingapp2.models import Task
from testingapp2.actions import mark_task_completed
from django.core.exceptions import ObjectDoesNotExist

@pytest.mark.django_db
def test_mark_task_completed_happy_path(task):
    """Test marking a task as completed successfully."""
    updated_task = mark_task_completed(task.id)
    assert updated_task.completed is True
    assert updated_task.id == task.id

@pytest.mark.django_db
def test_mark_task_completed_task_not_found():
    """Test handling a non-existent task ID."""
    with pytest.raises(ObjectDoesNotExist):
        mark_task_completed(999) # Assume ID 999 does not exist


@pytest.fixture
def task(db):
    """Fixture to create a task for testing."""
    task = Task.objects.create(description="Test Task", completed=False)
    return task

```