"""Pydantic models for the MCP Controller."""
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    """Model for a chat message."""
    source: str  # 'USER' or 'AI'
    content: str


class ToolCall(BaseModel):
    """Model for a tool call."""
    ToolName: str
    Parameters: Dict[str, Any]


class BpyCommand(BaseModel):
    """Model for a Blender Python command."""
    CommandType: str
    Script: str
    RequiresConfirmation: bool = False


# New models for Dynamic Command Generation
class ActionStep(BaseModel):
    """Model for a single step in an action plan."""
    operation: str
    params: Optional[Dict[str, Any]] = Field(default_factory=dict)


class ActionPlan(BaseModel):
    """Model for a multi-step action plan."""
    steps: List[ActionStep]


# Updated request and response models
class CommandRequest(BaseModel):
    """Model for a command request from the user."""
    SessionID: str
    Message: str
    action_plan: Optional[ActionPlan] = None
    mode: str = "contextual"  # Default mode


class CommandResponse(BaseModel):
    """Model for a command response to the user."""
    AiMessage: str
    Commands: List[BpyCommand]  # Kept for backward compatibility or simple commands
    status: str = "COMPLETED"  # Status for Action Plan execution


# Models for Dual Inventory Architecture
class ToolParameter(BaseModel):
    """Model for a tool parameter."""
    type: str
    description: str
    required: bool = False
    default: Any | None = None


class Tool(BaseModel):
    """Model for a tool definition."""
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
    """Model for a tool category."""
    description: str
    tools: list[Tool]


class RecipeParameter(BaseModel):
    """Model for a recipe parameter."""
    name: str
    type: str
    description: str
    default: Any


class RecipeStep(BaseModel):
    """Model for a recipe step."""
    operation: str
    params: dict[str, Any] = {}


class Recipe(BaseModel):
    """Model for a recipe definition."""
    name: str
    category: str
    version: str
    tags: list[str] = []
    description: str
    parameters: list[RecipeParameter] = []
    steps: list[RecipeStep]


# Search Models
class ToolMetadata(BaseModel):
    """Model for tool metadata."""
    name: str
    label: str
    description: str
    tags: List[str]
    category: str


class ToolSearchResult(BaseModel):
    """Model for a tool search result."""
    name: str
    description: str
    usage: str  # e.g. "create_cube(size=1.0)"
    match_reason: str  # Debug info


class ExecuteCommandRequest(BaseModel):
    """Model for an execute command request."""
    tool_name: str = Field(..., description="The exact name of the tool to execute (e.g., 'mesh.create_cube')")
    params: Dict[str, Any] = Field(default_factory=dict, description="Parameters for the tool")


class SaveRecipeRequest(BaseModel):
    """Model for a save recipe request."""
    name: str = Field(..., description="Name of the recipe")
    description: str = Field(..., description="What the recipe does")
    steps: List[Dict[str, Any]] = Field(..., description="List of steps (operation, params)")
