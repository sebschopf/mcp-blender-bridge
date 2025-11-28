import pytest
import yaml
from controller.app.knowledge_engine import KnowledgeEngine


@pytest.fixture
def mock_dirs(tmp_path):
    """Creates temporary directories with sample YAML files for testing."""
    capabilities = tmp_path / "capabilities"
    capabilities.mkdir()
    knowledge_base = tmp_path / "knowledge_base"
    knowledge_base.mkdir()
    
    # Create sample tool
    tool_data = {
        "Modeling": {
            "description": "Modeling tools",
            "tools": [
                {
                    "name": "create_cube",
                    "description": "Creates a cube",
                    "params": {}
                }
            ]
        }
    }
    with open(capabilities / "modeling.yaml", "w") as f:
        yaml.dump(tool_data, f)
        
    # Create sample recipe
    recipe_data = {
        "name": "Make Cube",
        "category": "Modeling",
        "version": "1.0",
        "description": "Creates a basic cube",
        "tags": ["modeling", "basic"],
        "parameters": [],
        "steps": [
            {
                "operation": "create_cube",
                "params": {"size": 2.0}
            }
        ]
    }
    with open(knowledge_base / "cube_recipe.yaml", "w") as f:
        yaml.dump(recipe_data, f)
        
    return capabilities, knowledge_base

def test_load_inventories(mock_dirs):
    """Test loading tools and recipes from files."""
    cap_dir, kb_dir = mock_dirs
    engine = KnowledgeEngine(str(cap_dir), str(kb_dir))
    engine.load_inventories()
    
    assert "Modeling" in engine.tools
    assert "create_cube" in engine.tools["Modeling"]
    assert "Make Cube" in engine.recipes

def test_search_tools(mock_dirs):
    """Test tool search functionality."""
    cap_dir, kb_dir = mock_dirs
    engine = KnowledgeEngine(str(cap_dir), str(kb_dir))
    engine.load_inventories()
    
    results = engine.search_tools("cube")
    assert len(results) > 0
    assert results[0].name == "create_cube"

def test_search_recipes(mock_dirs):
    """Test recipe search functionality."""
    cap_dir, kb_dir = mock_dirs
    engine = KnowledgeEngine(str(cap_dir), str(kb_dir))
    engine.load_inventories()
    
    results = engine.search_recipes("basic")
    assert len(results) == 1
    assert results[0].name == "Make Cube"

def test_execute_recipe(mock_dirs):
    """Test recipe execution logic."""
    cap_dir, kb_dir = mock_dirs
    engine = KnowledgeEngine(str(cap_dir), str(kb_dir))
    engine.load_inventories()
    
    steps = engine.execute_recipe("Make Cube", {})
    assert len(steps) == 1
    assert steps[0]["operation"] == "create_cube"
    assert steps[0]["params"]["size"] == 2.0
