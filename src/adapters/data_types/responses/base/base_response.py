from http import HTTPStatus

from pydantic import BaseModel

from src.domain.enums.http_response.enum import InternalCodeEnum


class BaseResponse(BaseModel):
    success: bool = False
    internal_code: InternalCodeEnum = InternalCodeEnum.SUCCESS
    message: str = None
    status: HTTPStatus = None

    @classmethod
    def get_swagger_schema(cls):
        schema = cls.model_json_schema()

        if '$defs' in schema:
            schema['definitions'] = schema.pop('$defs')

        def fix_refs(obj):
            if isinstance(obj, dict):
                for key, value in obj.items():
                    if key == '$ref':
                        obj[key] = obj[key].replace('/$defs/', '/definitions/')
                    else:
                        fix_refs(value)
            elif isinstance(obj, list):
                for item in obj:
                    fix_refs(item)

        fix_refs(schema)
        return schema
