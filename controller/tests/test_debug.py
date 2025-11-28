from controller.app.models import ToolParameter


def test_tp():
    tp = ToolParameter(type="float", description="desc")
    assert tp.type == "float"
