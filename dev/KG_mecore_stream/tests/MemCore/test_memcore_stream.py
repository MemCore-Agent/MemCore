import unittest
import os
from datetime import datetime, timedelta
from src.MemCore import MemCoreStream
from src.MemCore.types import MemCoreItem

class TestMemCoreStream(unittest.TestCase):
    def setUp(self):
        self.file_name = "tests/MemCore/test_MemCore.json"
        self.MemCore_stream = MemCoreStream(file_name=self.file_name)

    def tearDown(self):
        # Clean up test file after each test
        try:
            os.remove(self.file_name)
        except FileNotFoundError:
            pass

    def test_add_MemCore(self):
        data = [MemCoreItem("test_entity", datetime.now().replace(microsecond=0))]
        self.MemCore_stream.add_MemCore(data)
        self.assertEqual(len(self.MemCore_stream), 1)
        self.assertEqual(self.MemCore_stream.get_MemCore()[0], data[0])

    def test_remove_old_MemCore(self):
        past_date = datetime.now().replace(microsecond=0) - timedelta(days=10)
        self.MemCore_stream.add_MemCore([MemCoreItem("old_entity", past_date)])
        self.MemCore_stream.remove_old_MemCore(5)
        self.assertEqual(len(self.MemCore_stream.get_MemCore()), 0)

    def test_save_and_load_MemCore(self):
        data = [MemCoreItem("test_entity", datetime.now().replace(microsecond=0))]
        self.MemCore_stream.add_MemCore(data)
        self.MemCore_stream.save_MemCore()
        new_MemCore_stream = MemCoreStream(file_name=self.file_name)
        self.assertEqual(len(new_MemCore_stream), len(self.MemCore_stream))
        self.assertEqual(new_MemCore_stream.get_MemCore(), self.MemCore_stream.get_MemCore())

    def test_get_MemCore_by_index(self):
        data = [MemCoreItem("entity1", datetime.now().replace(microsecond=0)), MemCoreItem("entity2", datetime.now().replace(microsecond=0))]
        self.MemCore_stream.add_MemCore(data)
        self.assertEqual(self.MemCore_stream.get_MemCore_by_index(1), data[1])

    def test_remove_MemCore_by_index(self):
        data = [MemCoreItem("entity1", datetime.now().replace(microsecond=0)), MemCoreItem("entity2", datetime.now().replace(microsecond=0))]
        self.MemCore_stream.add_MemCore(data)
        self.MemCore_stream.remove_MemCore_by_index(0)
        self.assertEqual(len(self.MemCore_stream), 1)
        self.assertEqual(self.MemCore_stream.get_MemCore()[0], data[1])

if __name__ == '__main__':
    unittest.main()
