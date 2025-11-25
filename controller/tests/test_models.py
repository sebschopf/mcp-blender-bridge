from app.models import (
    BpyCommand,
    ChatMessage,
    CommandRequest,
    CommandResponse,
    ToolCall,
)


def test_chat_message_model():
    msg = ChatMessage(source="USER", content="Hello")
    assert msg.source == "USER"
    assert msg.content == "Hello"


def test_tool_call_model():
    tool = ToolCall(ToolName="create_cube", Parameters={"size": 2.0})
    assert tool.ToolName == "create_cube"
    assert tool.Parameters["size"] == 2.0


def test_bpy_command_model():
    cmd = BpyCommand(CommandType="EXECUTE_BPY", Script="bpy.ops.mesh.primitive_cube_add()")
    assert cmd.CommandType == "EXECUTE_BPY"
    assert cmd.Script == "bpy.ops.mesh.primitive_cube_add()"
    assert cmd.RequiresConfirmation is False


def test_command_request_model():
    req = CommandRequest(SessionID="test-session", Message="create a sphere")
    assert req.SessionID == "test-session"
    assert req.Message == "create a sphere"


def test_command_response_model():
    cmd = BpyCommand(CommandType="EXECUTE_BPY", Script="bpy.ops.mesh.primitive_cube_add()")
    res = CommandResponse(AiMessage="OK", Commands=[cmd], status="EXECUTING")
    assert res.AiMessage == "OK"
    assert len(res.Commands) == 1
    assert res.status == "EXECUTING"
