def mark_task_completed(task_id):
    task = get_object_or_404(Task, id=task_id)
    task.completed = True
    task.save()
    return task