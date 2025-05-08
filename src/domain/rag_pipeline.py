from abc import ABC, abstractmethod


class IRAGPipeline(ABC):
    @abstractmethod
    async def process(self, user_message: str):
        pass
