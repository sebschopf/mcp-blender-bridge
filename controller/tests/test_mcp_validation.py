import pytest
from unittest.mock import MagicMock, AsyncMock, patch
from app.mcp_server import execute_command
from app.models import Tool, ToolParameter

@pytest.mark.asyncio
async def test_execute_command_validation_failure():
    # Mock KnowledgeEngine
    mock_ke = MagicMock()
    
    # Define a mock tool
    tool_def = Tool(
        name="test_tool",
        description="A test tool",
        params={
            "radius": ToolParameter(type="float", description="Radius"),
            "depth": ToolParameter(type="float", description="Depth")
        }
    )
    mock_ke.get_tool.return_value = tool_def
    
    # Mock globals.get_knowledge_engine
    with patch("app.globals.get_knowledge_engine", return_value=mock_ke):
        # execute_command is an mcp tool, so we call it directly as an async function
        
        # Test Case 1: Unknown parameter "size"
        result = await execute_command("test_tool", {"size": 2.0})
        
        assert "Error: The following parameters are not valid" in result
        assert "size" in result
        # Check that allowed params are listed (order might vary)
        assert "radius" in result
        assert "depth" in result

@pytest.mark.asyncio
async def test_execute_command_validation_success():
    # Mock KnowledgeEngine
    mock_ke = MagicMock()
    
    # Define a mock tool
    tool_def = Tool(
        name="test_tool",
        description="A test tool",
        params={
            "radius": ToolParameter(type="float", description="Radius")
        }
    )
    mock_ke.get_tool.return_value = tool_def
    
    # Mock execute_tool_logic to avoid bridge calls
    with patch("app.globals.get_knowledge_engine", return_value=mock_ke):
        with patch("app.mcp_server.execute_tool_logic", new_callable=AsyncMock) as mock_logic:
            mock_logic.return_value = "Success"
            
            # Test Case 2: Valid parameter
            result = await execute_command("test_tool", {"radius": 1.5})
            
            assert result == "Success"
            mock_logic.assert_called_once_with("test_tool", radius=1.5)
