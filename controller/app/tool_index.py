"""Tool Indexing and Search functionality."""
import logging
import re
from collections import Counter, defaultdict
from typing import Dict, List, Set

from .models import Tool, ToolMetadata, ToolSearchResult

logger = logging.getLogger(__name__)


class ToolIndex:
    """Inverted index for efficient tool searching."""
    def __init__(self):
        """Initialize the ToolIndex."""
        self.index: Dict[str, Set[str]] = defaultdict(set)  # token -> set of tool_names
        self.metadata: Dict[str, ToolMetadata] = {}
        self.signatures: Dict[str, str] = {}  # name -> usage string

    def _tokenize(self, text: str) -> Set[str]:
        """Extracts searchable tokens from text."""
        if not text:
            return set()
        clean_text = text.lower().replace(".", " ").replace("_", " ")
        tokens = re.findall(r"\b[a-z0-9]{2,}\b", clean_text)
        return set(tokens)

    def _generate_signature(self, tool: Tool) -> str:
        """Generates a python-like signature for the tool."""
        params_str = []
        for name, param in tool.params.items():
            default_val = f"={param.default}" if param.default is not None else ""
            # Display required params first
            if param.required:
                params_str.insert(0, f"{name}: {param.type}")
            else:
                params_str.append(f"{name}: {param.type}{default_val}")
        return f"{tool.name}({', '.join(params_str)})"

    def build_index(self, tools: Dict[str, Dict[str, Tool]]):
        """Builds the inverted index from a nested dictionary of tools.

        Structure: { category: { tool_name: Tool } }.
        """
        logger.info("Building Tool Index...")
        count = 0
        self.index.clear()
        self.metadata.clear()
        self.signatures.clear()

        for category, cat_tools in tools.items():
            for name, tool in cat_tools.items():
                label = tool.label or name.split(".")[-1].replace("_", " ").title()

                meta = ToolMetadata(
                    name=tool.name,
                    label=label,
                    description=tool.description,
                    tags=tool.tags + tool.keywords,
                    category=category,
                )
                self.metadata[name] = meta
                self.signatures[name] = self._generate_signature(tool)

                # Indexing with weights
                # Name tokens (high weight)
                name_tokens = self._tokenize(tool.name)
                for token in name_tokens:
                    self.index[token].add(name)

                # Label tokens (medium-high weight)
                label_tokens = self._tokenize(label)
                for token in label_tokens:
                    self.index[token].add(name)

                # Tag tokens (medium weight)
                for tag in meta.tags:
                    tag_tokens = self._tokenize(tag)
                    for token in tag_tokens:
                        self.index[token].add(name)

                # Description tokens (low weight)
                desc_tokens = self._tokenize(tool.description)
                for token in desc_tokens:
                    self.index[token].add(name)

                count += 1

        logger.info(f"Indexed {count} tools.")

    def search(self, query: str, limit: int = 5) -> List[ToolSearchResult]:
        """Searches for tools matching the query using an improved scoring system."""
        query_tokens = self._tokenize(query)
        if not query_tokens:
            return []

        # Collect all tools that match *any* query token
        candidate_tool_names: Set[str] = set()
        for token in query_tokens:
            if token in self.index:
                candidate_tool_names.update(self.index[token])

        if not candidate_tool_names:
            return []

        scores: Counter = Counter()
        match_reasons: Dict[str, List[str]] = defaultdict(list)

        for tool_name in candidate_tool_names:
            meta = self.metadata[tool_name]
            current_tool_score = 0

            # Scoring based on matches with query tokens
            for token in query_tokens:
                # Name match (highest priority)
                if token in self._tokenize(tool_name):
                    current_tool_score += 10
                    match_reasons[tool_name].append(f"Name token '{token}'")

                # Label match
                if token in self._tokenize(meta.label):
                    current_tool_score += 7
                    match_reasons[tool_name].append(f"Label token '{token}'")

                # Tag match
                for tag in meta.tags:
                    if token in self._tokenize(tag):
                        current_tool_score += 5
                        match_reasons[tool_name].append(f"Tag token '{token}'")
                        break  # Only count once per tag

                # Description match
                if token in self._tokenize(meta.description):
                    current_tool_score += 2
                    match_reasons[tool_name].append(f"Description token '{token}'")

            scores[tool_name] = current_tool_score

        # Filter out tools with zero score (if a token matched but scored 0 due to logic above)
        scored_tools = {name: score for name, score in scores.items() if score > 0}

        # Sort by score desc
        top_tools = Counter(scored_tools).most_common(limit)

        results = []
        for tool_name, score in top_tools:
            meta = self.metadata[tool_name]
            results.append(
                ToolSearchResult(
                    name=meta.name,
                    description=meta.description,
                    usage=self.signatures.get(tool_name, f"{tool_name}(...)"),
                    match_reason=f"Score: {score}. Matches: {', '.join(match_reasons[tool_name][:3])}",
                )
            )

        return results
