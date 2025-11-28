import os
import sys
from unittest.mock import patch

import pytest

# Add controller to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from controller.app.mcp_server import search_tools
from controller.app.models import ToolSearchResult


@pytest.fixture
def mock_ke():
    with patch("controller.app.globals.get_knowledge_engine") as mock:
        yield mock.return_value

@pytest.mark.asyncio
async def test_search_tools(mock_ke):
    """Test the search_tools meta-tool."""
    mock_ke.search_tools.return_value = [
        ToolSearchResult(
            name="create_cube",
            description="Creates a cube",
            usage="create_cube(size=2.0)",
            match_reason="exact"
        )
    ]
    result = await search_tools("cube")
    assert "create_cube" in result
