import importlib


# Try to use pydantic's BaseModel when available, otherwise use a lightweight fallback.
try:
    _pydantic_module = importlib.import_module("pydantic")
    _PydanticBaseModel = _pydantic_module.BaseModel
except (ImportError, ModuleNotFoundError):
    _PydanticBaseModel = None


# Fallback lightweight BaseModel when pydantic is not available (for editor/type-checker errors)
class _FallbackBaseModel:
    def __init__(self, **data):
        for k, v in data.items():
            setattr(self, k, v)

    def dict(self):
        return self.__dict__.copy()

    def json(self):
        import json

        return json.dumps(self.dict())


# Use pydantic BaseModel if available, else the fallback
BaseModel: type = _PydanticBaseModel if _PydanticBaseModel is not None else _FallbackBaseModel


class Job(BaseModel):
    id: int | None = None
    title: str
    company: str
    location: str
    created_at: str | None = None
    status: str = "Aktivní"

    salary: str | None = None
    url: str | None = None
    contact: str | None = None
    note: str | None = None
    
class JobStatus(BaseModel):
    status: str    