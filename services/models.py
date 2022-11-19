from abc import ABC, abstractmethod


class HandleKafkaTopic(ABC):
    def __init__(self, msg):
        self.msg = msg

    def get_entities(self):
        return self.model.from_json(self.msg)
    
    @abstractmethod
    def execute(self):
        print(f"Message from {self.__class__.__name__} received.")