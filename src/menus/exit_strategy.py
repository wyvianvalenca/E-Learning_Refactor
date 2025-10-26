from typing import Any
from typing_extensions import override

from src.menus.strategy_interface import MenuActionStrategy

from src.inicial import console


class ExitStrategy(MenuActionStrategy):
    """ STRATEGY PATTERN - Estratégia para sair de qualquer menu """

    @override
    def get_label(self) -> str:
        return "Sair"

    @override
    def execute(self, context: dict[str, Any]) -> None:
        console.print("\nRetornando...")
        context['continue'] = False  # Sinaliza para parar o loop
        return None
