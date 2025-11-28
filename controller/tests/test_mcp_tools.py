import os
import sys
from unittest.mock import AsyncMock, patch

import pytest

# Add controller to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from controller.app.inject_bpy import inject_bpy_script
from controller.app.preview_bpy import preview_bpy


@pytest.mark.asyncio
async def test_inject_bpy_script_valid():
    """Test inject_bpy_script with a valid script."""
    script = "import bpy\nbpy.ops.mesh.primitive_cube_add()"
    
    # Mock dependencies
    with patch("controller.app.inject_bpy.extract_script_from_response", return_value=script), \
         patch("controller.app.inject_bpy.validate_syntax", return_value=(True, None)), \
         patch("controller.app.inject_bpy.detect_forbidden_imports", return_value=None), \
         patch("controller.app.inject_bpy.find_bpy_operators", return_value=["bpy.ops.mesh.primitive_cube_add"]), \
         patch("controller.app.inject_bpy.mcp_inspect_tool", new_callable=AsyncMock) as mock_inspect, \
         patch("controller.app.inject_bpy.run_in_sandbox", return_value={"success": True}) as mock_sandbox:
        
        mock_inspect.return_value = "OK"
        
        result = await inject_bpy_script("format-to-bpy", script)
        
        assert "Sandbox execution succeeded" in result
        mock_sandbox.assert_called_once()


@pytest.mark.asyncio
async def test_inject_bpy_script_invalid_syntax():
    """Test inject_bpy_script with invalid syntax."""
    script = "import bpy\nthis is not python"
    
    with patch("controller.app.inject_bpy.extract_script_from_response", return_value=script), \
         patch("controller.app.inject_bpy.validate_syntax", return_value=(False, "Syntax Error")), \
         patch("controller.app.inject_bpy.audit_record"):
        
        result = await inject_bpy_script("format-to-bpy", script)
        
        assert "Validation failed" in result
        assert "Syntax Error" in result


@pytest.mark.asyncio
async def test_preview_bpy_valid():
    """Test preview_bpy with a valid script."""
    script = "import bpy\nbpy.ops.mesh.primitive_cube_add()"
    
    with patch("controller.app.preview_bpy.extract_script_from_response", return_value=script), \
         patch("controller.app.preview_bpy.validate_syntax", return_value=(True, None)), \
         patch("controller.app.preview_bpy.detect_forbidden_imports", return_value=None), \
         patch("controller.app.preview_bpy.find_bpy_operators", return_value=["bpy.ops.mesh.primitive_cube_add"]), \
         patch("controller.app.mcp_server.inspect_tool", new_callable=AsyncMock) as mock_inspect, \
         patch("controller.app.preview_bpy.run_in_sandbox", return_value={"success": True}) as mock_sandbox:
        
        mock_inspect.return_value = "OK"
        
        result = await preview_bpy("format-to-bpy", script)
        
        assert result["status"] == "ok"
        assert result["syntax_ok"] is True
        assert result["operators_detected"] == ["bpy.ops.mesh.primitive_cube_add"]
        mock_sandbox.assert_called_once()

@pytest.mark.asyncio
async def test_preview_bpy_forbidden():
    """Test preview_bpy with forbidden imports."""
    script = "import os\nos.system('calc')"
    
    with patch("controller.app.preview_bpy.extract_script_from_response", return_value=script), \
         patch("controller.app.preview_bpy.validate_syntax", return_value=(True, None)), \
         patch("controller.app.preview_bpy.detect_forbidden_imports", return_value=["os"]):
        
        result = await preview_bpy("format-to-bpy", script)
        
        assert result["status"] == "invalid"
        assert result["forbidden_imports"] == ["os"]
