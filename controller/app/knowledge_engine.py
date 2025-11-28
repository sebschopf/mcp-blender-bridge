"""Knowledge Engine for managing tools and recipes."""
from pathlib import Path
from typing import Any, Dict, List

import yaml

from .models import Recipe, Tool, ToolCategory, ToolSearchResult
from .tool_index import ToolIndex


class KnowledgeEngine:
    """Core engine for loading, indexing, and retrieving tools and recipes."""
    def __init__(self, capabilities_dir: str, knowledge_base_dir: str):
        """Initialize the KnowledgeEngine."""
        self.capabilities_dir = Path(capabilities_dir)
        self.knowledge_base_dir = Path(knowledge_base_dir)
        self.tools: Dict[str, Dict[str, Tool]] = {}
        self.recipes: Dict[str, Recipe] = {}
        self.tool_index = ToolIndex()

    def load_inventories(self):
        """Loads all tools and recipes from the filesystem."""
        self._load_capabilities()
        self._load_knowledge_base()
        self.tool_index.build_index(self.tools)

    def _load_capabilities(self):
        """Scans the capabilities directory, loads, and validates all tools."""
        for yaml_file in self.capabilities_dir.rglob("*.yaml"):
            with open(yaml_file, "r") as f:
                data = yaml.safe_load(f)
                if data:
                    for category_name, category_data in data.items():
                        if category_name not in self.tools:
                            self.tools[category_name] = {}
                        category = ToolCategory(**category_data)
                        for tool in category.tools:
                            self.tools[category_name][tool.name] = tool

    def _load_knowledge_base(self):
        """Scans the knowledge_base directory, loads, and validates all recipes."""
        for yaml_file in self.knowledge_base_dir.rglob("*.yaml"):
            with open(yaml_file, "r") as f:
                data = yaml.safe_load(f)
                if data:
                    recipe = Recipe(**data)  # type: ignore
                    self.recipes[recipe.name] = recipe

    def get_tool_palette(self, category: str | None = None) -> Dict[str, Any]:
        """Returns a structured dictionary of available tools.

        If a category is specified, only tools from that category are returned.
        """
        if category:
            if category in self.tools:
                return {category: self.tools[category]}
            else:
                return {}
        return self.tools

    def get_tool_categories(self) -> List[str]:
        """Returns a list of all available tool category names."""
        return list(self.tools.keys())

    def search_tools(self, query: str, limit: int = 5) -> List[ToolSearchResult]:
        """Searches for tools using the ToolIndex."""
        return self.tool_index.search(query, limit=limit)

    def get_tool(self, tool_name: str) -> Tool | None:
        """Retrieves a specific tool by name."""
        # This is inefficient but sufficient for the current scale
        for category in self.tools.values():
            if tool_name in category:
                return category[tool_name]
        return None

    def search_recipes(self, query: str) -> List[Recipe]:
        """Searches for recipes based on a query."""
        results: List[Recipe] = []
        for recipe in self.recipes.values():
            if (
                query.lower() in recipe.name.lower()
                or query.lower() in recipe.description.lower()
                or any(query.lower() in tag.lower() for tag in recipe.tags)
            ):
                results.append(recipe)
        return results

    def execute_recipe(self, recipe_name: str, params: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Executes a recipe's steps."""
        if recipe_name not in self.recipes:
            return []

        recipe = self.recipes[recipe_name]
        executable_steps: List[Dict[str, Any]] = []

        for step in recipe.steps:
            # Deep copy the params to avoid modifying the original recipe
            step_params = step.params.copy()

            # Inject parameters
            for key, value in step_params.items():
                if isinstance(value, str) and value.startswith("{{") and value.endswith("}}"):
                    param_expression = value[2:-2].strip()
                    try:
                        # Create a local scope for eval with recipe parameters
                        local_scope = {p.name: params.get(p.name, p.default) for p in recipe.parameters}
                        # Also add the direct params for convenience
                        local_scope.update(params)
                        step_params[key] = eval(param_expression, {}, local_scope)
                    except (NameError, SyntaxError):
                        step_params[key] = value  # Keep original if evaluation fails
                elif isinstance(value, list):
                    new_list: List[Any] = []
                    for item in value:  # type: ignore
                        if isinstance(item, str) and item.startswith("{{") and item.endswith("}}"):
                            param_expression = item[2:-2].strip()
                            try:
                                local_scope = {p.name: params.get(p.name, p.default) for p in recipe.parameters}
                                local_scope.update(params)
                                new_list.append(eval(param_expression, {}, local_scope))
                            except (NameError, SyntaxError):
                                new_list.append(item)  # Keep original if evaluation fails
                        else:
                            new_list.append(item)
                    step_params[key] = new_list

            executable_steps.append({"operation": step.operation, "params": step_params})

        return executable_steps

    def save_recipe(self, recipe_data: Dict[str, Any]) -> bool:
        """Saves a new recipe to the knowledge base."""
        try:
            recipe = Recipe(**recipe_data)

            # Sanitize the recipe name to create a safe filename
            filename = "".join(c for c in recipe.name if c.isalnum() or c in (" ", "_")).rstrip()
            filepath = self.knowledge_base_dir / f"{filename}.yaml"

            with open(filepath, "w") as f:
                yaml.dump(recipe.model_dump(), f, sort_keys=False)

            # Add the new recipe to the in-memory store
            self.recipes[recipe.name] = recipe
            return True
        except Exception:
            return False
