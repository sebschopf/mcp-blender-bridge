import pytest

from controller.validators import bpy_validator


def test_detect_forbidden_imports():
    script = """
import bpy
import os
"""
    found = bpy_validator.detect_forbidden_imports(script)
    assert "os" in found
