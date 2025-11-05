from datetime import datetime

from pydantic import BaseModel, Field
from enum import Enum
import uuid


class TaskStatus(str, Enum):
    PENDING = "Pendente"
    IN_PROGRESS = "Em Progresso"
    COMPLETED = "Concluído"


class Task(BaseModel):
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str = Field(min_length=3, max_length=100)
    description: str | None = None
    status: TaskStatus = Field(default=TaskStatus.PENDING)
    created_at: str = Field(default_factory=lambda: str(datetime.now())) 

    
    class Config:
        use_enum_values = True