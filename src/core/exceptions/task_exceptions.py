# Exceção base para todas as exceções de negócio da Task
class TaskDomainException(Exception):
    pass

# Exceção 1: Usada quando tentamos deletar uma tarefa em status inválido.
class TaskNotInValidStateForDeletionError(TaskDomainException):
    """Erro levantado quando uma tarefa está em um status que impede sua exclusão."""
    def __init__(self, task_id: str, current_status: str):
        self.task_id = task_id
        self.current_status = current_status
        super().__init__(f"A tarefa ID '{task_id}' não pode ser excluída. Status atual: '{current_status}'. Deve estar 'Pendente' ou 'Concluído'.")

# Exceção 2: Usada quando uma tarefa não é encontrada.
class TaskNotFoundError(TaskDomainException):
    """Erro levantado quando uma tarefa não é encontrada."""
    def __init__(self, task_id: str):
        self.task_id = task_id
        super().__init__(f"Tarefa com ID '{task_id}' não encontrada.")