import pytest

from app import globals
from app.mcp_server import mcp, register_tools


@pytest.mark.asyncio
async def test_mcp_tools_registered():
    # Ensure initialized
    globals.initialize_knowledge_engine()
    register_tools()

    tools = await mcp.list_tools()
    # If no tools in capabilities, this might fail, but we assume capabilities exist from verify_prerequisites
    # We saw transforms.yaml in capabilities/object

    tool_names = [t.name for t in tools]
    # Check for meta-tools
    if "search_tools" in tool_names and "execute_command" in tool_names:
        assert True
    else:
        # Fail if meta-tools are missing
        assert False, f"Meta-tools missing. Found: {tool_names}"

    # At least check register_tools didn't crash
    assert mcp is not None


@pytest.mark.asyncio
async def test_mcp_resource_registered():
    resources = await mcp.list_resources()
    resource_uris = [str(r.uri) for r in resources]
    assert "blender://scene/objects" in resource_uris
