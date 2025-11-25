import pytest

from app.models import Tool, ToolParameter
from app.tool_index import ToolIndex


@pytest.fixture
def tool_index():
    return ToolIndex()


@pytest.fixture
def sample_tools():
    return {
        "mesh": {
            "mesh.create_cube": Tool(
                name="mesh.create_cube",
                label="Create Cube",
                description="Creates a new cube mesh.",
                tags=["primitive", "geometry"],
                params={"size": ToolParameter(type="float", description="Size")},
            ),
            "mesh.create_sphere": Tool(
                name="mesh.create_sphere",
                label="Create Sphere",
                description="Creates a new sphere mesh.",
                tags=["primitive", "geometry", "round"],
                params={"radius": ToolParameter(type="float", description="Radius")},
            ),
        },
        "transform": {
            "transform.rotate": Tool(
                name="transform.rotate",
                label="Rotate Object",
                description="Rotates the active object.",
                tags=["manipulate", "spin"],
                params={"angle": ToolParameter(type="float", description="Angle")},
            )
        },
    }


def test_build_index(tool_index, sample_tools):
    tool_index.build_index(sample_tools)
    assert "mesh.create_cube" in tool_index.metadata
    assert "transform.rotate" in tool_index.metadata
    assert "cube" in tool_index.index
    assert "mesh.create_cube" in tool_index.index["cube"]


def test_search_exact_name(tool_index, sample_tools):
    tool_index.build_index(sample_tools)
    results = tool_index.search("create_cube")
    assert len(results) > 0
    assert results[0].name == "mesh.create_cube"


def test_search_tag(tool_index, sample_tools):
    tool_index.build_index(sample_tools)
    results = tool_index.search("round")
    assert len(results) > 0
    assert results[0].name == "mesh.create_sphere"


def test_search_description(tool_index, sample_tools):
    tool_index.build_index(sample_tools)
    results = tool_index.search("rotates")
    assert len(results) > 0
    assert results[0].name == "transform.rotate"


def test_search_scoring(tool_index, sample_tools):
    tool_index.build_index(sample_tools)
    # "primitive" is in both cube and sphere tags
    # But if we search "cube primitive", cube should win
    results = tool_index.search("cube primitive")
    assert results[0].name == "mesh.create_cube"


def test_signature_generation(tool_index, sample_tools):
    tool_index.build_index(sample_tools)
    res = tool_index.search("cube")
    assert "size: float" in res[0].usage
