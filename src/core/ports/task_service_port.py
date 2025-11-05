from abc import ABC, abstractmethod
from typing import List
from src.core.domain.task import Task, TaskStatus


class TaskServicePort(ABC):
    
    @abstractmethod
    def create_task(self, title: str, description: str | None) -> Task:
        """Cria uma nova tarefa."""
        pass

    @abstractmethod
    def get_all_tasks(self) -> List[Task]:
        """Retorna todas as tarefas."""
        pass

    @abstractmethod
    def update_task_status(self, task_id: str, new_status: TaskStatus) -> Task:
        """Atualiza o status de uma tarefa."""
        pass

    @abstractmethod
    def delete_task(self, task_id: str) -> None:
        """Exclui uma tarefa. (Aqui estará a regra de negócio!)"""
        pass