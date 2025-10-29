from typing_extensions import override

from src.inicial import logs
from src.logging.base_decorator_strategy import BaseDecoratorStrategy


class LoggingDecoratorStrategy(BaseDecoratorStrategy):
    @override
    def execute(self, context: dict[str, str]) -> None:
        with open(logs, "a") as log_file:
            log_file.write(f"{context['user']} choose {type(self.strategy).__name__}\n")

        self.strategy.execute(context)