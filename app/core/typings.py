from typing import TypeVar

from pydantic import BaseModel

from app.core.db import ModelBase


ModelType = TypeVar("ModelType", bound=ModelBase)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
