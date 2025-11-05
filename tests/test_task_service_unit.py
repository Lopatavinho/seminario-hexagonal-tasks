import pytest
from unittest.mock import Mock, call
from src.core.domain.task import Task, TaskStatus
from src.core.ports.task_repository_port import TaskRepositoryPort
from src.core.services.task_service import TaskService
from src.core.exceptions.task_exceptions import TaskNotInValidStateForDeletionError, TaskNotFoundError


@pytest.fixture
def mock_repository() -> Mock:
    return Mock(spec=TaskRepositoryPort)


@pytest.fixture
def task_service(mock_repository: Mock) -> TaskService:
    return TaskService(repository=mock_repository)



def test_delete_task_allowed_when_pending(task_service: TaskService, mock_repository: Mock):
    
    task_id = "123"
    task_pending = Task(id=task_id, title="Test", status=TaskStatus.PENDING)
    mock_repository.find_by_id.return_value = task_pending

    
    task_service.delete_task(task_id)

    
    mock_repository.delete_by_id.assert_called_once_with(task_id)

def test_delete_task_allowed_when_completed(task_service: TaskService, mock_repository: Mock):
    
    task_id = "456"
    task_completed = Task(id=task_id, title="Test", status=TaskStatus.COMPLETED)
    mock_repository.find_by_id.return_value = task_completed

    
    task_service.delete_task(task_id)

    
    mock_repository.delete_by_id.assert_called_once_with(task_id)

def test_delete_task_blocked_when_in_progress(task_service: TaskService, mock_repository: Mock):
    
    task_id = "789"
    task_in_progress = Task(id=task_id, title="Test", status=TaskStatus.IN_PROGRESS)
    mock_repository.find_by_id.return_value = task_in_progress

    
    with pytest.raises(TaskNotInValidStateForDeletionError):
        task_service.delete_task(task_id)

    
    mock_repository.delete_by_id.assert_not_called()


def test_delete_task_not_found(task_service: TaskService, mock_repository: Mock):
   
    task_id = "unknown"
    mock_repository.find_by_id.return_value = None 

    
    with pytest.raises(TaskNotFoundError):
        task_service.delete_task(task_id)

    mock_repository.delete_by_id.assert_not_called()