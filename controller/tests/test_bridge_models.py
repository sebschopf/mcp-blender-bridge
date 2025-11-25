import pytest
from pydantic import ValidationError

from app.bridge_models import BridgeCommand, BridgeResult


def test_bridge_command_model_valid():
    command = BridgeCommand(type="execute_script", payload={"script": "print()"})
    assert command.type == "execute_script"
    assert command.payload["script"] == "print()"

    command_get_state = BridgeCommand(type="get_state", payload={})
    assert command_get_state.type == "get_state"
    assert command_get_state.payload == {}


def test_bridge_command_model_invalid_type():
    with pytest.raises(ValidationError):
        BridgeCommand(type="invalid_type", payload={})


def test_bridge_command_model_missing_payload():
    with pytest.raises(ValidationError):
        # Payload is required by Pydantic Model
        BridgeCommand(type="execute_script")  # type: ignore


def test_bridge_result_model_valid_success():
    result = BridgeResult(command_id="123", status="success", data={"output": "Success!"})
    assert result.command_id == "123"
    assert result.status == "success"
    assert result.data["output"] == "Success!"


def test_bridge_result_model_valid_error():
    result = BridgeResult(command_id="456", status="error", error_message="Something went wrong")
    assert result.command_id == "456"
    assert result.status == "error"
    assert result.error_message == "Something went wrong"


def test_bridge_result_model_invalid_status():
    with pytest.raises(ValidationError):
        BridgeResult(command_id="789", status="invalid_status")  # type: ignore
