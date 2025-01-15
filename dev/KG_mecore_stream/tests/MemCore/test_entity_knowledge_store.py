import unittest
import os
from datetime import datetime
from src.MemCore import EntityKnowledgeStore
from src.MemCore.types import KnowledgeMemCoreItem, MemCoreItem


class TestEntityKnowledgeStore(unittest.TestCase):

    def setUp(self):
        self.file_name = "tests/MemCore/test_knowledge_MemCore.json"
        self.entity_knowledge_store = EntityKnowledgeStore(
            file_name=self.file_name)

    def tearDown(self):
        # Clean up test file after each test
        try:
            os.remove(self.file_name)
        except FileNotFoundError:
            pass

    def test_add_MemCore(self):
        data = [
            MemCoreItem("test_entity",
                       datetime.now().replace(microsecond=0))
        ]
        self.entity_knowledge_store.add_MemCore(data)
        assert len(self.entity_knowledge_store.knowledge_MemCore) == 1
        assert isinstance(self.entity_knowledge_store.knowledge_MemCore[0],
                          KnowledgeMemCoreItem)

    def test_convert_MemCore_to_knowledge_MemCore(self):
        data = [
            MemCoreItem("test_entity",
                       datetime.now().replace(microsecond=0))
        ]
        converted_data = self.entity_knowledge_store._convert_MemCore_to_knowledge_MemCore(
            data)
        assert len(converted_data) == 1
        assert isinstance(converted_data[0], KnowledgeMemCoreItem)

    def test_update_knowledge_MemCore(self):
        data = [
            KnowledgeMemCoreItem("knowledge_entity", 1,
                                datetime.now().replace(microsecond=0))
        ]
        self.entity_knowledge_store._update_knowledge_MemCore(data)
        assert len(self.entity_knowledge_store.knowledge_MemCore) == 1
        assert self.entity_knowledge_store.knowledge_MemCore[0] == data[0]
