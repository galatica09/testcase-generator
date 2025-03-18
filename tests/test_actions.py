```python
import pytest
from django.core.exceptions import ObjectDoesNotExist
from testingapp2.models import Task
from testingapp2.actions import mark_task_completed


# Fixtures
@pytest.fixture
def create_task(db):
    """Fixture to create a task."""
    def _create_task(completed=False, **kwargs):
        task = Task(**kwargs, completed=completed)
        task.save()
        return task
    return _create_task


# Test Cases

def test_mark_task_completed_happy_path(create_task):
    """Test successful completion marking."""
    task = create_task(description="Test Task")
    updated_task = mark_task_completed(task.id)
    assert updated_task.completed is True
    assert updated_task.id == task.id


def test_mark_task_completed_task_not_found(create_task):
    """Test handling of non-existent task."""
    with pytest.raises(ObjectDoesNotExist):
        mark_task_completed(9999)  # Non-existent task ID


def test_mark_task_completed_already_completed(create_task):
    """Test marking an already completed task."""
    task = create_task(description="Already Completed Task", completed=True)
    updated_task = mark_task_completed(task.id)
    assert updated_task.completed is True
    assert updated_task.id == task.id


def test_mark_task_completed_with_description(create_task):
    """Test marking a task as complete while preserving its description."""
    task = create_task(description="Test Task with Description")
    updated_task = mark_task_completed(task.id)
    assert updated_task.completed is True
    assert updated_task.description == "Test Task with Description"

```

This test suite includes:

* **`test_mark_task_completed_happy_path`**:  A positive test case verifying that a task's `completed` status changes correctly.
* **`test_mark_task_completed_task_not_found`**: A negative test case demonstrating the correct exception handling when trying to complete a non-existent task.
* **`test_mark_task_completed_already_completed`**: A negative test case checking that attempting to mark an already completed task doesn't cause errors.
* **`test_mark_task_completed_with_description`**:  This verifies that other fields (like description) are preserved when marking a task complete.

The `create_task` fixture simplifies task creation for the test cases, making the tests cleaner and more readable.  The tests are modular and cover both happy path and error scenarios, adhering to the specified guidelines.  No mocking is needed as the function interacts directly with the database via Django's ORM.