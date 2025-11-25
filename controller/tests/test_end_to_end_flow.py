import pytest
import asyncio

from controller.app import preview_bpy


@pytest.mark.asyncio
async def test_preview_flow_success():
    sample = """
```python
import bpy
def create_cube():
    bpy.ops.mesh.primitive_cube_add(size=1)

if __name__ == '__main__':
    create_cube()
```
"""
    res = await preview_bpy.preview_bpy("format-to-bpy", sample)
    assert res.get("status") in ("ok", "sandbox_failed")
    assert "extracted_script" in res
    assert res.get("syntax_ok") is True
