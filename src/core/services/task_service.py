from typing import List
from src.core.domain.task import Task, TaskStatus
from src.core.ports.task_service_port import TaskServicePort
from src.core.ports.task_repository_port import TaskRepositoryPort
from src.core.exceptions.task_exceptions import TaskNotInValidStateForDeletionError, TaskNotFoundError


class TaskService(TaskServicePort):

    def __init__(self, repository: TaskRepositoryPort):
        self._repository = repository


    def create_task(self, title: str, description: str | None) -> Task:
        new_task = Task(title=title, description=description)
        return self._repository.save(new_task)

    def get_all_tasks(self) -> List[Task]:
        return self._repository.find_all()

    def update_task_status(self, task_id: str, new_status: TaskStatus) -> Task:
        task = self._repository.find_by_id(task_id)
        if not task:
            raise TaskNotFoundError(task_id)
        
        task.status = new_status
        return self._repository.save(task)

    
    def delete_task(self, task_id: str) -> None:
        task_to_delete = self._repository.find_by_id(task_id)

        if not task_to_delete:
            
            raise TaskNotFoundError(task_id)

        
        if task_to_delete.status == TaskStatus.IN_PROGRESS:
            raise TaskNotInValidStateForDeletionError(task_id, task_to_delete.status)
        

        self._repository.delete_by_id(task_id)