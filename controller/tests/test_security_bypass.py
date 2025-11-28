import os
import sys

# Add controller to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from controller.app.validation import validate_bpy_script


def test_bypass():
    print("Running Security Bypass Tests (Red Team)...")

    # Attack 1: getattr bypass
    # Trying to access __builtins__ via getattr
    getattr_attack = """
import bpy
builtins = getattr(bpy, "__builtins__")
# If we get here, we might be able to get 'eval' or 'open'
"""
    valid, errors = validate_bpy_script(getattr_attack)
    if valid:
        print("[FAIL] getattr attack PASSED validation! (Vulnerability confirmed)")
    else:
        print(f"[PASS] getattr attack blocked: {errors}")

    # Attack 2: __subclasses__ gadget chain
    # Trying to find 'os' or 'subprocess' via object traversal
    subclasses_attack = """
import bpy
# Get object class
classes = (1).__class__.__base__.__subclasses__()
# Try to find a dangerous class (simplified check)
print(classes)
"""
    valid, errors = validate_bpy_script(subclasses_attack)
    if valid:
        print("[FAIL] __subclasses__ attack PASSED validation! (Vulnerability confirmed)")
    else:
        print(f"[PASS] __subclasses__ attack blocked: {errors}")

    # Attack 3: Accessing __class__
    class_attack = """
import bpy
t = (1).__class__
"""
    valid, errors = validate_bpy_script(class_attack)
    if valid:
        print("[FAIL] __class__ access PASSED validation! (Vulnerability confirmed)")
    else:
        print(f"[PASS] __class__ access blocked: {errors}")

if __name__ == "__main__":
    test_bypass()
