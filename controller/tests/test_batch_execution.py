import asyncio
import os
import sys
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

# Add controller to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from controller.app.bridge_api import bridge_manager
from controller.app.mcp_server import submit_script


@pytest.mark.asyncio
async def test_submit_script_valid():
    """Test submitting a valid script."""
    valid_script = """
import bpy
bpy.ops.mesh.primitive_cube_add()
bpy.ops.transform.translate(value=(0, 0, 1))
"""
    # Mock the bridge response
    mock_response = MagicMock()
    mock_response.status = "success"
    mock_response.data = {"output": "Success: Executed batch script"}
    
    # Patch the execute_command method on the singleton instance
    with patch.object(bridge_manager, 'execute_command', new_callable=AsyncMock) as mock_exec:
        mock_exec.return_value = mock_response
        
        result = await submit_script(valid_script)
        
        # Verify result
        assert "Success" in result
        
        # Verify bridge was called with correct payload
        mock_exec.assert_called_once()
        call_args = mock_exec.call_args[0][0]
        assert call_args.type == "execute_script"
        assert call_args.payload["script"] == valid_script

@pytest.mark.asyncio
async def test_submit_script_malicious():
    """Test submitting a malicious script (should be blocked by validator)."""
    malicious_script = """
import bpy
import os
os.system('calc')
"""
    # Patch the execute_command method on the singleton instance
    with patch.object(bridge_manager, 'execute_command', new_callable=AsyncMock) as mock_exec:
        result = await submit_script(malicious_script)
        
        # Verify result indicates error
        assert "Error" in result
        assert "Import of 'os' is not allowed" in result
        
        # Verify bridge was NOT called
        mock_exec.assert_not_called()

if __name__ == "__main__":
    # Helper to run async tests manually if needed
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    print("Running Valid Script Test...")
    loop.run_until_complete(test_submit_script_valid())
    print("Running Malicious Script Test...")
    loop.run_until_complete(test_submit_script_malicious())
    loop.close()
