import os
import sys

# Add controller to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from controller.app.validation import validate_bpy_script


def test_security():
    print("Running Security Validation Tests...")

    # Test Case 1: Safe Script
    safe_script = """
import bpy
import math
from mathutils import Vector

def create_cube():
    bpy.ops.mesh.primitive_cube_add(size=2)
    vec = Vector((1, 2, 3))
    print(f"Created cube at {vec}")

create_cube()
"""
    valid, errors = validate_bpy_script(safe_script)
    if valid:
        print("[PASS] Safe script passed.")
    else:
        print(f"[FAIL] Safe script failed: {errors}")

    # Test Case 2: Malicious Import (os)
    malicious_import = """
import bpy
import os

os.system('echo "Hacked"')
"""
    valid, errors = validate_bpy_script(malicious_import)
    if not valid and "Import of 'os' is not allowed" in str(errors):
        print("[PASS] Malicious import (os) blocked.")
    else:
        print(f"[FAIL] Malicious import (os) NOT blocked correctly. Valid: {valid}, Errors: {errors}")

    # Test Case 3: Malicious Function (eval)
    malicious_eval = """
import bpy
x = "print('hacked')"
eval(x)
"""
    valid, errors = validate_bpy_script(malicious_eval)
    if not valid and "Call to banned function 'eval' is not allowed" in str(errors):
        print("[PASS] Malicious function (eval) blocked.")
    else:
        print(f"[FAIL] Malicious function (eval) NOT blocked correctly. Valid: {valid}, Errors: {errors}")

    # Test Case 4: Malicious Attribute (__builtins__)
