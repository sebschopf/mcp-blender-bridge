# controller/test_e2e.py
import subprocess
import sys
import time

import requests

BASE_URL = "http://127.0.0.1:8000"


def run_test(test_function):
    """Helper function to run a test and print its status."""
    test_name = "Unknown Test"
    try:
        test_name = test_function.__name__
        print(f"--- Running test: {test_name} ---")
        if test_function():
            print(f"✓ PASS: {test_name}")
            return True
        else:
            print(f"✗ FAIL: {test_name}")
            return False
    except Exception as e:
        print(f"✗ FAIL: {test_name} - An exception occurred: {e}")
        return False


def test_capabilities_endpoint():
    """Tests if the capabilities endpoint returns a valid palette."""
    response = requests.get(f"{BASE_URL}/api/mcp/capabilities", timeout=5)
    if response.status_code != 200:
        print(f"  Error: Status code was {response.status_code}")
        return False
    data = response.json()
    if not isinstance(data, dict) or "bpy.ops.mesh.primitive_cube_add" not in data:
        print(f"  Error: Response data is not a valid capability palette. Got: {data}")
        return False
    return True


def test_valid_action_plan():
    """Tests if a valid ActionPlan is correctly processed."""
    request_data = {
        "SessionID": "e2e-test-session",
        "Message": "e2e test",
        "action_plan": {
            "steps": [
                {
                    "operation": "bpy.ops.mesh.primitive_cube_add",
                    "params": {"size": 1.5},
                }
            ]
        },
    }
    response = requests.post(f"{BASE_URL}/api/chat", json=request_data, timeout=5)
    if response.status_code != 200:
        print(f"  Error: Status code was {response.status_code}")
        return False
    data = response.json()
    if data.get("status") != "EXECUTING" or not data.get("Commands"):
        print(f"  Error: Response did not indicate execution. Got: {data}")
        return False
    return True


def test_invalid_action_plan():
    """Tests if an invalid ActionPlan is correctly rejected."""
    request_data = {
        "SessionID": "e2e-test-session",
        "Message": "e2e test invalid",
        "action_plan": {"steps": [{"operation": "bpy.ops.mesh.do_something_bad", "params": {}}]},
    }
    response = requests.post(f"{BASE_URL}/api/chat", json=request_data, timeout=5)
    if response.status_code != 200:
        print(f"  Error: Status code was {response.status_code}")
        return False
    data = response.json()
    if data.get("status") != "ERROR":
        print(f"  Error: Response did not indicate an error. Got: {data}")
        return False
    return True


def main():
    """Main function to run the E2E test suite."""
    server_process = None
    all_tests_passed = False
    try:
        print("Starting FastAPI server for E2E tests...")
        # Start the server as a background process
        server_process = subprocess.Popen(["uvicorn", "app.main:app"])
        # Give the server a moment to start up
        time.sleep(5)
        print("Server started. Running tests...")

        results = [
            run_test(test_capabilities_endpoint),
            run_test(test_valid_action_plan),
            run_test(test_invalid_action_plan),
        ]

        all_tests_passed = all(results)

    finally:
        if server_process:
            print("Shutting down FastAPI server...")
            server_process.terminate()
            server_process.wait()
            print("Server shut down.")

    if all_tests_passed:
        print("\n✓ All E2E tests passed successfully!")
        sys.exit(0)
    else:
        print("\n✗ Some E2E tests failed.")
        sys.exit(1)


if __name__ == "__main__":
    main()
