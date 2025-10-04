from pydantic import BaseModel, Field
from enum import Enum
from datetime import datetime

# ---- Thêm model Gemini ----
class ModelName(str, Enum):
    GEMINI_FLASH = "gemini-2.5-flash"
    GEMINI_PRO = "gemini-2.5-pro"

class QueryInput(BaseModel):
    question: str
    session_id: str | None = Field(default=None)
    model: ModelName = Field(default=ModelName.GEMINI_FLASH)  # ✅ đổi mặc định sang Gemini

class QueryResponse(BaseModel):
    answer: str
    session_id: str
    model: ModelName

class DocumentInfo(BaseModel):
    id: int
    filename: str
    upload_timestamp: datetime

class DeleteFileRequest(BaseModel):
    file_id: int
