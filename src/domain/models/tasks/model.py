from datetime import date, datetime
from typing import Optional

from sqlalchemy import Enum, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from src.domain.enums.tasks.enum import TaskPriorityEnum, TaskStatusEnum
from src.domain.models.orm_base.model import Base


class TaskModel(Base):
    __tablename__ = 'tasks'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(100))
    description: Mapped[Optional[str]] = mapped_column(Text)
    status: Mapped[str] = mapped_column(Enum(TaskStatusEnum))
    priority: Mapped[str] = mapped_column(
        Enum(TaskPriorityEnum), default=TaskPriorityEnum.MEDIUM
    )
    deadline: Mapped[Optional[date]]
    created_at: Mapped[datetime] = mapped_column(default=datetime.now())
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.now(), onupdate=datetime.now()
    )
