import json
import logging

from ailive.MemCore import BaseMemCore
from ailive.MemCore.types import KnowledgeMemCoreItem, MemCoreItem


class EntityKnowledgeStore(BaseMemCore):

    def __len__(self):
        """Returns the number of items in the MemCore."""
        return len(self.knowledge_MemCore)

    def init_MemCore(self):
        """Initializes MemCore.
        self.entity_MemCore: list[EntityMemCoreItem]
        """
        self.load_MemCore_from_file()
        if self.entity:
            self.add_MemCore(self.entity)

    @property
    def return_MemCore(self):
        return self.knowledge_MemCore


    def load_MemCore_from_file(self):
        try:
            with open(self.file_name, 'r') as file:
                self.knowledge_MemCore = [
                    KnowledgeMemCoreItem.from_dict(item)
                    for item in json.load(file)
                ]
            logging.info(
                f"Entity Knowledge MemCore loaded from {self.file_name} successfully."
            )
        except FileNotFoundError:
            logging.info(
                "File not found. Starting with an empty entity knowledge MemCore."
            )

    def add_MemCore(self, MemCore_stream: list[MemCoreItem]):
        """To add new MemCore to the entity knowledge store
        we should convert the MemCore to knowledge MemCore and then update the knowledge MemCore

        Args:
            MemCore_stream (list): list of MemCoreItem
        """
        knowledge_meory = self._convert_MemCore_to_knowledge_MemCore(
            MemCore_stream)
        self._update_knowledge_MemCore(knowledge_meory)


    def _update_knowledge_MemCore(self, knowledge_MemCore: list):
        """update self.knowledge MemCore with new knowledge MemCore items

        Args:
            knowledge_MemCore (list): list of KnowledgeMemCoreItem
        """
        for item in knowledge_MemCore:
            for i, entity in enumerate(self.knowledge_MemCore):
                if entity.entity == item.entity:
                    self.knowledge_MemCore[i].date = item.date
                    self.knowledge_MemCore[i].count += item.count
                    break
            else:
                self.knowledge_MemCore.append(item)

    def _convert_MemCore_to_knowledge_MemCore(
            self, MemCore_stream: list) -> list[KnowledgeMemCoreItem]:
        """Converts MemCore to knowledge MemCore

        Returns:
            knowledge_MemCore (list): list of KnowledgeMemCoreItem
        """
        knowledge_MemCore = []

        entities = set([item.entity for item in MemCore_stream])
        for entity in entities:
            MemCore_dates = [
                item.date for item in MemCore_stream if item.entity == entity
            ]
            knowledge_MemCore.append(
                KnowledgeMemCoreItem(entity, len(MemCore_dates),
                                    max(MemCore_dates)))
        return knowledge_MemCore

    def get_MemCore(self) -> list[KnowledgeMemCoreItem]:
        return self.knowledge_MemCore

    
    
