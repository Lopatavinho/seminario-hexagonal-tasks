from datetime import datetime
# Importamos Pydantic para criar nosso modelo (Entity)
from pydantic import BaseModel, Field
from enum import Enum
import uuid

# 1. Enum para Status: Garante que só existam estados válidos.
class TaskStatus(str, Enum):
    PENDING = "Pendente"
    IN_PROGRESS = "Em Progresso"
    COMPLETED = "Concluído"

# 2. Modelo de Domínio (Entidade Task)
# Esta classe DEFINE a Task, independente de como ela será armazenada
class Task(BaseModel):
    # Usamos Field para defaults e validação
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str = Field(min_length=3, max_length=100)
    description: str | None = None
    status: TaskStatus = Field(default=TaskStatus.PENDING)
    created_at: str = Field(default_factory=lambda: str(datetime.now())) # Usaremos datetime.now

    # Configuração para Pydantic (opcional)
    class Config:
        use_enum_values = True