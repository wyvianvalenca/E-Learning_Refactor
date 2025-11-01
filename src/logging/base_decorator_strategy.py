from abc import ABC, abstractmethod
from typing import Any
from typing_extensions import override

from src.menus.strategy_interface import MenuActionStrategy


class BaseDecoratorStrategy(MenuActionStrategy, ABC):
    """ DECORATOR PATTERN - Base para decoradores de estratégias de menu """

    _strategy: MenuActionStrategy

    def __init__(self, component: MenuActionStrategy):
        self._strategy = component

    @property
    def strategy(self) -> MenuActionStrategy:
        return self._strategy

    @override
    def get_label(self) -> str:
        return self._strategy.get_label()

    @override
    @abstractmethod
    def execute(self, context: dict[str, Any]) -> None:
        self._strategy.execute(context)

    @override
    def can_execute(self, context: dict[str, Any]) -> bool:
        return self._strategy.can_execute(context)
