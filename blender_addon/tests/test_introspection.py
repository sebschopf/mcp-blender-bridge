import importlib
import os
import sys

import bpy

# Path setup to find the addon modules
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)


def test_introspection():
    print("\n--- Testing Blender Introspection ---")

    # Debug: List some MESH_OT types
    print("DEBUG: Listing first 10 MESH_OT types in bpy.types:")
    count = 0
    for name in dir(bpy.types):
        if name.startswith("MESH_OT"):
            print(f"  {name}")
            count += 1
            if count >= 10:
                break

    try:
        # Ensure addon modules are loaded
        import blender_addon.introspection as introspection

        importlib.reload(introspection)

        # Test 1: Valid Operator
        tool_name = "bpy.ops.mesh.primitive_cube_add"
        print(f"Testing valid operator: {tool_name}")
        result = introspection.extract_properties(tool_name)

        if not result:
            print("FAIL: No result returned for valid operator.")
            return False

        if result["name"] != "Add Cube" and result["name"] != "Primitive Cube Add":
            print(f"FAIL: Unexpected name: {result['name']}")
            return False

        # Check for 'size' property
        size_prop = next((p for p in result["properties"] if p["identifier"] == "size"), None)
        if not size_prop:
            print("FAIL: 'size' property not found.")
            return False

        print("PASS: Valid operator introspection successful.")

        # Test 2: Invalid Operator
        invalid_tool = "bpy.ops.mesh.non_existent_operator"
        print(f"Testing invalid operator: {invalid_tool}")
        result_invalid = introspection.extract_properties(invalid_tool)

        if result_invalid is not None:
            print("FAIL: Result should be None for invalid operator.")
            return False

        print("PASS: Invalid operator handled correctly.")

        return True

    except Exception as e:
        print(f"ERROR: Exception during test: {e}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_introspection()
    if not success:
        sys.exit(1)
