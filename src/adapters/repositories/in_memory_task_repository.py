from typing import List, Dict
from src.core.domain.task import Task
from src.core.ports.task_repository_port import TaskRepositoryPort


class InMemoryTaskRepository(TaskRepositoryPort):

    
    _tasks: Dict[str, Task] = {}

    def save(self, task: Task) -> Task:
       
        task_data = task.model_dump() 
        self._tasks[task.id] = Task(**task_data)
        return self._tasks[task.id]

    def find_all(self) -> List[Task]:
        
        return list(self._tasks.values())

    def find_by_id(self, task_id: str) -> Task | None:
        task = self._tasks.get(task_id)
        
        return task if task else None

    def delete_by_id(self, task_id: str) -> None:
        if task_id in self._tasks:
            del self._tasks[task_id]