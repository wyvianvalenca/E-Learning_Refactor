from typing import Any
import questionary
from rich.console import Console
from rich.panel import Panel

from src.menus.strategy_interface import MenuActionStrategy

# STRATEGY CONTEXT


class MenuManager:
    def __init__(self, console: Console, title: str):
        self.console = console
        self.title = title
        self.strategies: list[MenuActionStrategy] = []

    def add_strategy(self, strategy: MenuActionStrategy) -> 'MenuManager':
        """Adiciona uma estratégia ao menu"""
        self.strategies.append(strategy)
        return self

    def run(self, context: dict[str, Any]) -> None:
        """Executa o loop do menu"""
        context['continue'] = True

        while context.get('continue', True):
            self.console.print(Panel.fit(self.title, style="dark_cyan"))
            self.console.print()

            # Filtra apenas estratégias que podem ser executadas
            available_strategies = {
                s.get_label(): s for s in self.strategies if s.can_execute(context)
            }

            if not available_strategies:
                self.console.print("Nenhuma ação disponível no momento.")
                break

            # Monta as opções do menu
            choices = list(available_strategies.keys())

            # Pede para o usuário escolher uma opção do menu
            chosen_label: str = questionary.select(
                "Escolha uma opção:",
                choices=choices
            ).ask()

            # Executa a estratégia escolhida
            available_strategies[chosen_label].execute(context)
