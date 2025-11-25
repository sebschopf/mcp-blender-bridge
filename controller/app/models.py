from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    source: str  # 'USER' or 'AI'
    content: str


class ToolCall(BaseModel):
    ToolName: str
    Parameters: Dict[str, Any]


class BpyCommand(BaseModel):
    CommandType: str
    Script: str
    RequiresConfirmation: bool = False


# New models for Dynamic Command Generation
class ActionStep(BaseModel):
    operation: str
    params: Optional[Dict[str, Any]] = Field(default_factory=dict)


class ActionPlan(BaseModel):
    steps: List[ActionStep]


# Updated request and response models
class CommandRequest(BaseModel):
    SessionID: str
    Message: str
    action_plan: Optional[ActionPlan] = None
    mode: str = "contextual"  # Default mode


class CommandResponse(BaseModel):
    AiMessage: str
    Commands: List[BpyCommand]  # Kept for backward compatibility or simple commands
    status: str = "COMPLETED"  # Status for Action Plan execution


# Models for Dual Inventory Architecture
class ToolParameter(BaseModel):
    type: str
    description: str
    required: bool = False
    default: Any | None = None


class Tool(BaseModel):
    name: str
    description: str
    # Add optional fields for search support
    label: Optional[str] = None
    category: Optional[str] = None
    tags: List[str] = []
    keywords: List[str] = []
    requires_mode: Optional[str] = None
    params: dict[str, ToolParameter] = {}


class ToolCategory(BaseModel):
    description: str
    tools: list[Tool]


class RecipeParameter(BaseModel):
    name: str
    type: str
    description: str
    default: Any


class RecipeStep(BaseModel):
    operation: str
    params: dict[str, Any] = {}


class Recipe(BaseModel):
    name: str
    category: str
    version: str
    tags: list[str] = []
    description: str
    parameters: list[RecipeParameter] = []
    steps: list[RecipeStep]


# Search Models
class ToolMetadata(BaseModel):
    name: str
    label: str
    description: str
    tags: List[str]
    category: str


class ToolSearchResult(BaseModel):
    name: str
    description: str
    usage: str  # e.g. "create_cube(size=1.0)"
    match_reason: str  # Debug info


class ExecuteCommandRequest(BaseModel):
    tool_name: str = Field(..., description="The exact name of the tool to execute (e.g., 'mesh.create_cube')")
    params: Dict[str, Any] = Field(default_factory=dict, description="Parameters for the tool")


class SaveRecipeRequest(BaseModel):
    name: str = Field(..., description="Name of the recipe")
    description: str = Field(..., description="What the recipe does")
    steps: List[Dict[str, Any]] = Field(..., description="List of steps (operation, params)")
