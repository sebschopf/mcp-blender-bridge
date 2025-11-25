import time

import pytest

from app.models import Tool
from app.tool_index import ToolIndex


@pytest.fixture
def massive_tool_index():
    index = ToolIndex()
    tools = {"benchmarking": {}}

    # Create 2000 dummy tools
    for i in range(2000):
        name = f"benchmark.tool_{i}"
        desc = f"This is a benchmark tool number {i} for testing search performance. It handles cubes and spheres."
        tools["benchmarking"][name] = Tool(
            name=name, label=f"Tool {i}", description=desc, tags=["benchmark", "performance", "test"], params={}
        )

    index.build_index(tools)
    return index


def test_search_performance(massive_tool_index):
    start_time = time.time()
    # Perform 100 searches
    for _ in range(100):
        results = massive_tool_index.search("cube performance", limit=5)
        assert len(results) > 0

    end_time = time.time()
    total_time = end_time - start_time
    avg_time = total_time / 100

    print(f"\nAverage search time: {avg_time:.6f}s")

    # Fail if average search is slower than 50ms (it should be sub-millisecond for this scale)
    assert avg_time < 0.05
