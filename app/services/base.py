from abc import ABC, abstractmethod


class AsyncNotificationService(ABC):
    @abstractmethod
    async def send(self, to: str, message: str) -> bool:
        """Return True if success, False if fail"""
        pass
