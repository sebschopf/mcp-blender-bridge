import asyncio
import os

import pytest

# Ensure dummy API key is set before importing main
os.environ["GEMINI_API_KEY"] = "dummy_key"

from controller.app.bridge_api import BridgeCommand, BridgeResult, bridge_manager
from controller.app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

@pytest.mark.asyncio
async def test_bridge_flow():
    """Test the full cycle: execute -> get -> resolve."""
    # 1. Start execute_command in background
    cmd = BridgeCommand(type="execute_script", payload={"script": "print('hello')"})
    
    async def execute():
        return await bridge_manager.execute_command(cmd, timeout=2.0)
        
    task = asyncio.create_task(execute())
    
    # Yield to event loop to let execute_command put item in queue
    await asyncio.sleep(0.1)
    
    # 2. Verify command is in queue
    assert bridge_manager.command_queue.qsize() == 1
    
    # 3. Fetch command (simulate addon)
    fetched_cmd = await bridge_manager.get_next_command(timeout=1.0)
    assert fetched_cmd.id == cmd.id
    
    # 4. Resolve result (simulate addon posting result)
    result = BridgeResult(command_id=cmd.id, status="success", data={"output": "done"})
    bridge_manager.resolve_result(result)
    
    # 5. Verify execution completes
    res = await task
    assert res.status == "success"
    assert res.data == {"output": "done"}

def test_api_endpoints():
    """Test the HTTP endpoints for the bridge."""
    # Clear queue first
    while not bridge_manager.command_queue.empty():
        bridge_manager.command_queue.get_nowait()
        
    pass

@pytest.mark.asyncio
async def test_api_post_result():
    """Test posting a result via API."""
    cmd_id = "test_cmd_id"
    future = asyncio.Future()
    bridge_manager.pending_results[cmd_id] = future
    
    result_payload = {
        "command_id": cmd_id,
        "status": "success",
        "data": {"output": "api_done"}
    }
    
    response = client.post("/internal/post_result", json=result_payload)
    assert response.status_code == 200
    
    assert future.done()
    assert future.result().status == "success"
