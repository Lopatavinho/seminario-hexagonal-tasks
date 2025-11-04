import pytest
from unittest.mock import Mock, call
from src.core.domain.task import Task, TaskStatus
from src.core.ports.task_repository_port import TaskRepositoryPort
from src.core.services.task_service import TaskService
from src.core.exceptions.task_exceptions import TaskNotInValidStateForDeletionError, TaskNotFoundError

# Fixture para criar uma instância Mock da Porta de Repositório
@pytest.fixture
def mock_repository() -> Mock:
    return Mock(spec=TaskRepositoryPort)

# Fixture para criar a instância do Serviço, injetando o Mock
@pytest.fixture
def task_service(mock_repository: Mock) -> TaskService:
    return TaskService(repository=mock_repository)

# --- Teste da Regra de Negócio Crítica: Bloqueio de Exclusão ---

def test_delete_task_allowed_when_pending(task_service: TaskService, mock_repository: Mock):
    # 1. Arrange (Configuração)
    task_id = "123"
    task_pending = Task(id=task_id, title="Test", status=TaskStatus.PENDING)
    mock_repository.find_by_id.return_value = task_pending

    # 2. Act (Execução)
    task_service.delete_task(task_id)

    # 3. Assert (Verificação)
    # O Core DEVE chamar a exclusão do Repositório.
    mock_repository.delete_by_id.assert_called_once_with(task_id)

def test_delete_task_allowed_when_completed(task_service: TaskService, mock_repository: Mock):
    # 1. Arrange
    task_id = "456"
    task_completed = Task(id=task_id, title="Test", status=TaskStatus.COMPLETED)
    mock_repository.find_by_id.return_value = task_completed

    # 2. Act
    task_service.delete_task(task_id)

    # 3. Assert
    mock_repository.delete_by_id.assert_called_once_with(task_id)

def test_delete_task_blocked_when_in_progress(task_service: TaskService, mock_repository: Mock):
    # 1. Arrange
    task_id = "789"
    task_in_progress = Task(id=task_id, title="Test", status=TaskStatus.IN_PROGRESS)
    mock_repository.find_by_id.return_value = task_in_progress

    # 2. Act & 3. Assert (Esperamos uma exceção)
    # A exceção deve ser levantada PELO CORE.
    with pytest.raises(TaskNotInValidStateForDeletionError):
        task_service.delete_task(task_id)

    # O Core NÃO DEVE chamar a exclusão no Repositório (Mock).
    mock_repository.delete_by_id.assert_not_called()

# --- Teste de Erro (Task Not Found) ---
def test_delete_task_not_found(task_service: TaskService, mock_repository: Mock):
    # 1. Arrange
    task_id = "unknown"
    mock_repository.find_by_id.return_value = None # Repositório retorna None

    # 2. Act & 3. Assert (Esperamos a exceção TaskNotFoundError)
    with pytest.raises(TaskNotFoundError):
        task_service.delete_task(task_id)

    mock_repository.delete_by_id.assert_not_called()