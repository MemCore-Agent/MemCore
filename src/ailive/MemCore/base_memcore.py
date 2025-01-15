import json
import logging

from abc import ABC, abstractmethod
from datetime import datetime, timedelta


class BaseMemCore(ABC):

    def __init__(self, file_name: str, entity: str = None):
        """Initializes the MemCore storage."""
        self.file_name = file_name
        self.entity = entity
        self.MemCore = []
        self.knowledge_MemCore = []
        self.init_MemCore()

    @abstractmethod
    def __len__(self):
        """Returns the number of items in the MemCore."""
        pass

    @abstractmethod
    def init_MemCore(self):
        """Initializes MemCore."""
        pass

    @abstractmethod
    def load_MemCore_from_file(self):
        """Loads MemCore from a file."""
        pass

    @abstractmethod
    def add_MemCore(self, data):
        """Adds new MemCore data."""
        pass

    @abstractmethod
    def get_MemCore(self):
        pass

    @property
    def return_MemCore(self):
        return self.MemCore

    def remove_old_MemCore(self, days):
        """Removes MemCore items older than a specified number of days."""
        cutoff_date = datetime.now() - timedelta(days=days)
        self.MemCore = [
            item for item in self.return_MemCore if item.date >= cutoff_date
        ]
        logging.info("Old MemCore removed successfully.")

    def save_MemCore(self):
        if self.file_name:
            with open(self.file_name, 'w') as file:
                json.dump([item.to_dict() for item in self.return_MemCore],
                          file,
                          default=str,
                          indent=4)
                logging.info(f"MemCore saved to {self.file_name} successfully.")
        else:
            logging.info("No file name provided. MemCore not saved.")

    def get_MemCore_by_index(self, index):
        if 0 <= index < len(self.MemCore):
            return self.MemCore[index]
        else:
            return None

    def remove_MemCore_by_index(self, index):
        if 0 <= index < len(self.MemCore):
            del self.MemCore[index]
            logging.info("MemCore item removed successfully.")
            return True
        else:
            logging.info("Invalid index. MemCore item not removed.")
            return False

    def clear_MemCore(self):
        self.MemCore = []
        if self.file_name:
            with open(self.file_name, 'w') as file:
                json.dump([], file, indent=4) 
                logging.info(f"MemCore cleared and saved to {self.file_name} successfully.")
        else:
            logging.info("No file name provided. MemCore not cleared or saved.")
