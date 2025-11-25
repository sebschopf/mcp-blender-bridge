from controller.app.validation import validate_bpy_script


def test_valid_syntax():
    script = "import bpy\nbpy.ops.mesh.primitive_cube_add()"
    valid, errors = validate_bpy_script(script)
    assert valid
    assert not errors


def test_invalid_syntax():
    script = "import bpy\nif True"  # Incomplete statement causing SyntaxError
    valid, errors = validate_bpy_script(script)
    assert not valid
    assert "Syntax Error" in errors[0]


def test_missing_bpy():
    script = "print('hello')"
    valid, errors = validate_bpy_script(script)
    assert not valid
    assert "does not appear to use 'bpy'" in errors[0]
