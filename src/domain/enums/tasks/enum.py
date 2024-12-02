from enum import StrEnum


class TaskStatusEnum(StrEnum):
    TODO = 'TODO'
    DOING = 'DOING'
    DONE = 'DONE'


class TaskPriorityEnum(StrEnum):
    LOW = 'LOW'
    MEDIUM = 'MEDIUM'
    HIGH = 'HIGH'
