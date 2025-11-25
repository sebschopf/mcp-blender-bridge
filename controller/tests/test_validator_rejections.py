import pytest

from controller.validators import bpy_validator


def test_reject_forbidden_imports():
    script = """
import os
import bpy
"""
    ok, errors, warnings = bpy_validator.validate_script(script)
    assert not ok
    assert any("os" in e for e in errors)


def test_reject_forbidden_calls_open_exec_eval():
    script = """
code = open('/tmp/secret.txt', 'r')
eval('2+2')
"""
    ok, errors, warnings = bpy_validator.validate_script(script)
    assert not ok
    # Should flag open and eval
    assert any("open" in e or "eval" in e for e in errors)


def test_allow_bpy_only_script():
    script = """
import bpy
bpy.ops.mesh.primitive_cube_add(size=1)
"""
    ok, errors, warnings = bpy_validator.validate_script(script)
    assert ok
