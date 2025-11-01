from typing import Any
from typing_extensions import override

from src.inicial import logs
from src.models import Usuario
from src.logging.base_decorator_strategy import BaseDecoratorStrategy


class LoggingDecoratorStrategy(BaseDecoratorStrategy):
    """ DECORATOR PATTERN - Decorador para adicionar logs das opções de menu seleciondas pelos usuários """

    @override
    def execute(self, context: dict[str, Any]) -> None:
        user: Usuario = context['user']
        with open(logs, "a") as log_file:
            _ = log_file.write(f"{user.nome} choose {
                               type(self.strategy).__name__}\n")

        self.strategy.execute(context)
