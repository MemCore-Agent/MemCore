from typing import Optional, List

from ailive.agent.base_agent import Agent
import logging


class ChatAgent(Agent):
    """ChatAgent currently able to support Llama3 running on Ollama (default) and gpt-3.5-turbo for llm models,
    and LLaVA running on Ollama (default) and gpt-4-vision-preview for the vision tool.
    """

    def __init__(
        self,
        name,
        MemCore_stream_json,
        entity_knowledge_store_json,
        system_persona_txt,
        user_persona_txt,
        past_chat_json,
        llm_model_name="llama3",
        vision_model_name="llava",
        include_from_defaults=["search", "locate", "vision", "stocks"],
    ):
        super().__init__(
            name,
            MemCore_stream_json,
            entity_knowledge_store_json,
            system_persona_txt,
            user_persona_txt,
            past_chat_json,
            llm_model_name,
            vision_model_name,
            include_from_defaults,
        )

    def add_chat(self, role: str, content: str, entities: Optional[List[str]] = None):
        """Add a chat to the agent's MemCore.

        Args:
            role (str): 'system' or 'user'
            content (str): content of the chat
            entities (Optional[List[str]], optional): entities from MemCore systems. Defaults to None.
        """
        # Add a chat to the agent's MemCore.
        self._add_contexts_to_llm_message(role, content)

        if entities:
            self.MemCore_stream.add_MemCore(entities)
            self.MemCore_stream.save_MemCore()
            self.entity_knowledge_store.add_MemCore(self.MemCore_stream.get_MemCore())
            self.entity_knowledge_store.save_MemCore()

        self._replace_MemCore_from_llm_message()
        self._replace_eks_to_from_message()

    def get_chat(self):
        return self.contexts

    def clearMemCore(self):
        """Clears Neo4j database and MemCore stream/entity knowledge store."""

        logging.info("Deleting MemCore stream and entity knowledge store...")
        self.MemCore_stream.clear_MemCore()
        self.entity_knowledge_store.clear_MemCore()

        logging.info("Deleting nodes from Neo4j...")
        try:
            self.graph_store.query("MATCH (n) DETACH DELETE n")
        except Exception as e:
            logging.error(f"Error deleting nodes: {e}")
        logging.info("Nodes deleted from Neo4j.")

    def _replace_MemCore_from_llm_message(self):
        """Replace the MemCore_stream from the llm_message."""
        self.message.llm_message["MemCore_stream"] = self.MemCore_stream.get_MemCore()

    def _replace_eks_to_from_message(self):
        """Replace the entity knowledge store from the llm_message.
        eks = entity knowledge store"""

        self.message.llm_message["knowledge_entity_store"] = (
            self.entity_knowledge_store.get_MemCore()
        )
