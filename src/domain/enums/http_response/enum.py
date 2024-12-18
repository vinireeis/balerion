from enum import IntEnum


class InternalCodeEnum(IntEnum):
    SUCCESS = 0
    INVALID_PARAMS_ERROR = 10
    DATA_VALIDATION_ERROR = 20
    DATA_NOT_FOUND = 21
    STATUS_TRANSITION_ERROR = 22
    INFRASTRUCTURE_ERROR = 30
    INTERNAL_SERVER_ERROR = 99
