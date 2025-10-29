from abc import abstractmethod
from typing import Any

from src.menus.strategy_interface import MenuActionStrategy


class BaseDecoratorStrategy(MenuActionStrategy):
    _strategy: MenuActionStrategy

    def __init__(self, component: MenuActionStrategy):
        self._strategy = component

    @property
    def strategy(self) -> MenuActionStrategy:
        return self._strategy

    def get_label(self) -> str:
        return self._strategy.get_label()

    @abstractmethod
    def execute(self, context: dict[str, Any]) -> None:
        self._strategy.execute(context)

    def can_execute(self, context: dict[str, Any]) -> bool:
        return self._strategy.can_execute(context)