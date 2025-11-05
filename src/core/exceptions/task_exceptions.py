
class TaskDomainException(Exception):
    pass


class TaskNotInValidStateForDeletionError(TaskDomainException):
    """Erro levantado quando uma tarefa está em um status que impede sua exclusão."""
    def __init__(self, task_id: str, current_status: str):
        self.task_id = task_id
        self.current_status = current_status
        super().__init__(f"A tarefa ID '{task_id}' não pode ser excluída. Status atual: '{current_status}'. Deve estar 'Pendente' ou 'Concluído'.")


class TaskNotFoundError(TaskDomainException):
    """Erro levantado quando uma tarefa não é encontrada."""
    def __init__(self, task_id: str):
        self.task_id = task_id
        super().__init__(f"Tarefa com ID '{task_id}' não encontrada.")