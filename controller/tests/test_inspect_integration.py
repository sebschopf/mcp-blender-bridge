import pytest

from controller.validators import bpy_validator


def fake_inspect_caller_known(op_name: str):
    # Return a simple dict to indicate operator exists
    return {"name": op_name, "properties": []}


def fake_inspect_caller_unknown(op_name: str):
    raise Exception("Operator not found")


def test_verify_operators_with_inspect_all_known():
    ops = ["mesh.primitive_cube_add", "object.delete"]
    res = bpy_validator.verify_operators_with_inspect(ops, fake_inspect_caller_known)
    assert all(r[1] for r in res)


def test_verify_operators_with_inspect_some_unknown():
    ops = ["mesh.primitive_cube_add", "mesh.nonexistent_op"]
    def mixed_caller(op):
        if "nonexistent" in op:
            raise Exception("Operator not found")
        return {"name": op}

    res = bpy_validator.verify_operators_with_inspect(ops, mixed_caller)
    assert any(not r[1] for r in res)
