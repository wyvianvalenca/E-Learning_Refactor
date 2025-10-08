from abc import ABC, abstractmethod
from typing import Any

# STRATEGY INTERFACE


class MenuActionStrategy(ABC):
    @abstractmethod
    def execute(self, context: Any) -> None:
        pass

    @abstractmethod
    def get_label(self) -> str:
        pass

    def can_execute(self, context: Any) -> bool:
        return True
