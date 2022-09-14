from typing import Any

from pydantic import BaseModel


class BaseResponseSwagger(BaseModel):
    code: int
    data: Any
    msg: str


class PageCaseResponseSwagger(BaseResponseSwagger):
    pass
