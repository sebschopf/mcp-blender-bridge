import uuid
from typing import Any, Dict, Literal, Optional

from pydantic import BaseModel, Field


class BridgeCommand(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    type: Literal["execute_script", "get_state", "get_rna_info"]
    payload: Dict[str, Any]


class BridgeResult(BaseModel):
    command_id: str
    status: Literal["success", "error"]
    data: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None
