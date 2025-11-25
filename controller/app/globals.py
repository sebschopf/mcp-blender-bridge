import os

from .knowledge_engine import KnowledgeEngine

# Singleton instance
knowledge_engine: KnowledgeEngine = None  # type: ignore


def initialize_knowledge_engine():
    global knowledge_engine
    # The capabilities and knowledge_base dirs are relative to the controller app folder
    current_dir = os.path.dirname(os.path.abspath(__file__))
    controller_dir = os.path.dirname(current_dir)

    knowledge_engine = KnowledgeEngine(
        capabilities_dir=os.path.join(controller_dir, "capabilities"),
        knowledge_base_dir=os.path.join(controller_dir, "knowledge_base"),
    )
    knowledge_engine.load_inventories()


def get_knowledge_engine():
    global knowledge_engine
    if knowledge_engine is None:
        initialize_knowledge_engine()
    return knowledge_engine
