import pytest

from app.knowledge_engine import KnowledgeEngine

# Sample YAML data for testing
CAPABILITIES_YAML = """
transforms:
  description: "Tools for transforming objects."
  tools:
    - name: "transform.translate"
      description: "Moves an object."
      params:
        object_name:
          type: "string"
          description: "The name of the object to move."
        value:
          type: "list"
          description: "The (x, y, z) translation vector."
"""

RECIPE_YAML = """
name: "Simple Chair"
category: "furniture"
version: "1.0"
tags: ["furniture", "chair"]
description: "Creates a simple chair."
parameters:
  - name: "leg_height"
    type: "float"
    description: "The height of the chair legs."
    default: 0.5
steps:
  - operation: "mesh.create_cube"
    params:
      name: "Seat"
"""


@pytest.fixture
def mock_fs(tmp_path):
    capabilities_dir = tmp_path / "capabilities"
    capabilities_dir.mkdir()
    (capabilities_dir / "transforms.yaml").write_text(CAPABILITIES_YAML)

    knowledge_base_dir = tmp_path / "knowledge_base"
    knowledge_base_dir.mkdir()
    (knowledge_base_dir / "chair.yaml").write_text(RECIPE_YAML)

    return tmp_path


def test_load_inventories(mock_fs):
    engine = KnowledgeEngine(
        capabilities_dir=str(mock_fs / "capabilities"), knowledge_base_dir=str(mock_fs / "knowledge_base")
    )
    engine.load_inventories()

    assert "transforms" in engine.tools
    assert "transform.translate" in engine.tools["transforms"]
    assert engine.tools["transforms"]["transform.translate"].description == "Moves an object."

    assert "Simple Chair" in engine.recipes
    assert engine.recipes["Simple Chair"].category == "furniture"


def test_load_refactored_tools(tmp_path):
    # Create a mock filesystem with the refactored capabilities
    capabilities_dir = tmp_path / "capabilities"
    capabilities_dir.mkdir()
    object_dir = capabilities_dir / "object"
    object_dir.mkdir()
    mesh_dir = capabilities_dir / "mesh"
    mesh_dir.mkdir()

    (object_dir / "transforms.yaml").write_text("""
    transform:
      description: "Tools for manipulating existing objects."
      tools:
        - name: "bpy.ops.transform.translate"
          description: "Moves the currently active object."
    """)
    (mesh_dir / "primitives.yaml").write_text("""
    mesh:
      description: "Tools for creating new 3D objects."
      tools:
        - name: "bpy.ops.mesh.primitive_cube_add"
          description: "Creates a new cube mesh."
    """)
    (object_dir / "modifiers.yaml").write_text("""
    modifiers:
        description: "Tools for applying non-destructive modifications."
        tools:
            - name: "bpy.ops.object.modifier_add"
              description: "Adds a modifier to the active object."
    """)
    (object_dir / "management.yaml").write_text("""
    object:
        description: "Tools for managing whole objects."
        tools:
            - name: "object.rename"
              description: "Renames the currently active object."
    """)

    engine = KnowledgeEngine(
        capabilities_dir=str(capabilities_dir),
        knowledge_base_dir=str(tmp_path / "knowledge_base"),  # Empty for this test
    )
    engine.load_inventories()

    assert "transform" in engine.tools
    assert "bpy.ops.transform.translate" in engine.tools["transform"]
    assert "mesh" in engine.tools
    assert "bpy.ops.mesh.primitive_cube_add" in engine.tools["mesh"]
    assert "modifiers" in engine.tools
    assert "bpy.ops.object.modifier_add" in engine.tools["modifiers"]
    assert "object" in engine.tools
    assert "object.rename" in engine.tools["object"]


def test_search_recipes(mock_fs):
    engine = KnowledgeEngine(
        capabilities_dir=str(mock_fs / "capabilities"), knowledge_base_dir=str(mock_fs / "knowledge_base")
    )
    engine.load_inventories()
    results = engine.search_recipes("chair")
    assert len(results) == 1
    assert results[0].name == "Simple Chair"


def test_execute_recipe(mock_fs):
    engine = KnowledgeEngine(
        capabilities_dir=str(mock_fs / "capabilities"), knowledge_base_dir=str(mock_fs / "knowledge_base")
    )
    engine.load_inventories()
    steps = engine.execute_recipe("Simple Chair", {"leg_height": 0.6})
    assert len(steps) == 1
    assert steps[0]["operation"] == "mesh.create_cube"
    # This is a simplified test; a more robust test would check parameter injection
    assert steps[0]["params"]["name"] == "Seat"


def test_save_recipe(tmp_path):
    engine = KnowledgeEngine(
        capabilities_dir=str(tmp_path / "capabilities"), knowledge_base_dir=str(tmp_path / "knowledge_base")
    )
    (tmp_path / "knowledge_base").mkdir()

    recipe_data = {
        "name": "Test Recipe",
        "category": "testing",
        "version": "1.0",
        "description": "A test recipe.",
        "steps": [{"operation": "test.op", "params": {}}],
    }

    assert engine.save_recipe(recipe_data)
    assert (tmp_path / "knowledge_base" / "Test Recipe.yaml").exists()


def test_execute_simple_table_recipe(tmp_path):
    # Setup mock capabilities and knowledge base
    capabilities_dir = tmp_path / "capabilities"
    capabilities_dir.mkdir()
    object_dir = capabilities_dir / "object"
    object_dir.mkdir()
    mesh_dir = capabilities_dir / "mesh"
    mesh_dir.mkdir()

    (object_dir / "transforms.yaml").write_text("""
    transform:
      description: "Tools for manipulating existing objects."
      tools:
        - name: "transform.resize"
          description: "Resizes an object."
          params:
            object_name: { type: "string", description: "The name of the object to resize.", required: true }
            value: { type: "list", description: "The [X, Y, Z] scale factors.", required: true }
        - name: "transform.translate"
          description: "Translates an object."
          params:
            object_name: { type: "string", description: "The name of the object to translate.", required: true }
            value: { type: "list", description: "The [X, Y, Z] translation vector.", required: true }
    """)
    (mesh_dir / "primitives.yaml").write_text("""
    modeling:
      description: "Tools for creating new 3D objects."
      tools:
        - name: "mesh.create_cube"
          description: "Creates a new cube mesh."
          params:
            name: { type: "string", description: "The name of the cube.", required: true }
    """)

    knowledge_base_dir = tmp_path / "knowledge_base"
    knowledge_base_dir.mkdir()
    furniture_dir = knowledge_base_dir / "furniture"
    furniture_dir.mkdir()
    tables_dir = furniture_dir / "tables"
    tables_dir.mkdir()

    (tables_dir / "simple_table.yaml").write_text("""
name: "Simple Wooden Table"
category: "furniture/tables"
version: "1.0"
tags: ["furniture", "table", "wood"]
description: "Creates a simple four-legged table with a rectangular top."

parameters:
  - name: "table_width"
    type: "float"
    description: "The width of the table."
    default: 1.5
  - name: "table_depth"
    type: "float"
    description: "The depth of the table."
    default: 0.8

steps:
  - operation: "mesh.create_cube"
    params:
      name: "TableTop"
  - operation: "transform.resize"
    params:
      object_name: "TableTop"
      value: ["{{ table_width }}", "{{ table_depth }}", 0.05]
  - operation: "mesh.create_cube"
    params:
      name: "Leg1"
  - operation: "transform.resize"
    params:
      object_name: "Leg1"
      value: [0.05, 0.05, 0.75]
  - operation: "transform.translate"
    params:
      object_name: "Leg1"
      value: ["{{ table_width / 2 - 0.025 }}", "{{ table_depth / 2 - 0.025 }}", -0.375]
  - operation: "mesh.create_cube"
    params:
      name: "Leg2"
  - operation: "transform.resize"
    params:
      object_name: "Leg2"
      value: [0.05, 0.05, 0.75]
  - operation: "transform.translate"
    params:
      object_name: "Leg2"
      value: ["{{ -table_width / 2 + 0.025 }}", "{{ table_depth / 2 - 0.025 }}", -0.375]
  - operation: "mesh.create_cube"
    params:
      name: "Leg3"
  - operation: "transform.resize"
    params:
      object_name: "Leg3"
      value: [0.05, 0.05, 0.75]
  - operation: "transform.translate"
    params:
      object_name: "Leg3"
      value: ["{{ table_width / 2 - 0.025 }}", "{{ -table_depth / 2 + 0.025 }}", -0.375]
  - operation: "mesh.create_cube"
    params:
      name: "Leg4"
  - operation: "transform.resize"
    params:
      object_name: "Leg4"
      value: [0.05, 0.05, 0.75]
  - operation: "transform.translate"
    params:
      object_name: "Leg4"
      value: ["{{ -table_width / 2 + 0.025 }}", "{{ -table_depth / 2 + 0.025 }}", -0.375]
    """)

    engine = KnowledgeEngine(capabilities_dir=str(capabilities_dir), knowledge_base_dir=str(knowledge_base_dir))
    engine.load_inventories()

    # Execute the recipe with custom parameters
    params = {"table_width": 2.0, "table_depth": 1.0}
    executed_steps = engine.execute_recipe("Simple Wooden Table", params)

    assert len(executed_steps) == 14
    # Verify parameter injection for a few steps
    assert executed_steps[1]["params"]["value"] == [2.0, 1.0, 0.05]
    assert executed_steps[4]["params"]["value"] == [0.975, 0.475, -0.375]
