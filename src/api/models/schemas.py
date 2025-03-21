from pydantic import BaseModel

from pydantic import BaseModel

class QueryRequest(BaseModel):
    text: str  # Trường này phải có tên là "text" để khớp với request


class QueryResponse(BaseModel):
    response: str
