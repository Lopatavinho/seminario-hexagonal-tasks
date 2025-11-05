from abc import ABC, abstractmethod
from typing import List
from src.core.domain.task import Task 


class TaskRepositoryPort(ABC):
    
    @abstractmethod
    def save(self, task: Task) -> Task:
        """Salva ou atualiza uma tarefa."""
        pass

    @abstractmethod
    def find_all(self) -> List[Task]:
        """Retorna todas as tarefas."""
        pass

    @abstractmethod
    def find_by_id(self, task_id: str) -> Task | None:
        """Busca uma tarefa por ID."""
        pass

    @abstractmethod
    def delete_by_id(self, task_id: str) -> None:
        """Exclui uma tarefa por ID."""
        pass