import json
import logging
from datetime import datetime

from ailive.MemCore import BaseMemCore
from ailive.MemCore.types import MemCoreItem

logging.basicConfig(level=logging.INFO)


class MemCoreStream(BaseMemCore):

    def __len__(self):
        """Returns the number of items in the MemCore."""
        return len(self.MemCore)

    def init_MemCore(self):
        """Initializes MemCore
        self.MemCore: list[MemCoreItem]
        """
        self.load_MemCore_from_file()
        if self.entity:
            self.add_MemCore(self.entity)

    @property
    def return_MemCore(self):
        return self.MemCore

    def add_MemCore(self, entities):
        self.MemCore.extend([
            MemCoreItem(str(entity),
                       datetime.now().replace(microsecond=0))
            for entity in entities
        ])

    def get_MemCore(self) -> list[MemCoreItem]:
        return self.MemCore
    

    def load_MemCore_from_file(self):
        try:
            with open(self.file_name, 'r') as file:
                self.MemCore = [
                    MemCoreItem.from_dict(item) for item in json.load(file)
                ]
            logging.info(f"MemCore loaded from {self.file_name} successfully.")
        except FileNotFoundError:
            logging.info("File not found. Starting with an empty MemCore.")
