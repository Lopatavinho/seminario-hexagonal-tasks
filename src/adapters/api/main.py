from fastapi import FastAPI, HTTPException, status
from src.core.domain.task import Task, TaskStatus 
from src.core.services.task_service import TaskService
from src.core.exceptions.task_exceptions import TaskNotFoundError, TaskNotInValidStateForDeletionError


from src.adapters.repositories.in_memory_task_repository import InMemoryTaskRepository 


task_repository = InMemoryTaskRepository()
task_service = TaskService(repository=task_repository)


app = FastAPI(
    title="Gerenciador de Tarefas Hexagonal",
    description="Demo de Arquitetura Hexagonal com Python e FastAPI."
)



@app.post("/tasks", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task_endpoint(title: str, description: str | None = None):
    """Cria uma nova tarefa no sistema."""
    try:
        return task_service.create_task(title, description)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/tasks", response_model=list[Task])
def get_all_tasks_endpoint():
    """Lista todas as tarefas existentes."""
    return task_service.get_all_tasks()

@app.patch("/tasks/{task_id}/status", response_model=Task)
def update_task_status_endpoint(task_id: str, new_status: TaskStatus):
    """Atualiza o status de uma tarefa (Pendente, Em Progresso, Concluído)."""
    try:
        return task_service.update_task_status(task_id, new_status)
    except TaskNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task_endpoint(task_id: str):
    """Exclui uma tarefa. BLOQUEADO se estiver 'Em Progresso' (Regra de Negócio)."""
    try:
        task_service.delete_task(task_id)
        return {"message": "Tarefa excluída com sucesso."}
    except TaskNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except TaskNotInValidStateForDeletionError as e:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=str(e)
        )