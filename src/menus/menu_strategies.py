from abc import ABC, abstractmethod
from typing import Any

from rich.panel import Panel
import questionary

from src.inicial import console


# STRATEGY INTERFACE


class MenuActionStrategy(ABC):
    @staticmethod
    def cabecalho(titulo: str) -> None:
        console.print()
        console.print(
            Panel.fit(f"--- {titulo} ---",
                      style="gray62"))
        console.print()

    @staticmethod
    def retornar() -> None:
        console.print()
        _ = questionary.press_any_key_to_continue(
            "Pressione qualquer tecla para retornar...").ask()
        return None

    @abstractmethod
    def get_label(self) -> str:
        pass

    def can_execute(self, context: Any) -> bool:
        return True

    @abstractmethod
    def execute(self, context: Any) -> None:
        pass


class ExitStrategy(MenuActionStrategy):
    def get_label(self) -> str:
        return "Sair"

    def execute(self, context: dict[str, Any]) -> None:
        console.print("\nRetornando...")
        context['continue'] = False  # Sinaliza para parar o loop
        return None
