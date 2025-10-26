from abc import ABC, abstractmethod
from typing_extensions import override
from pathlib import Path

from src.inicial import console
from src.models.models import Conteudo, Externo


class ValidationResult:
    """ CHAIN OF RESPONSABILITY PATTERN - Resultado de validação individual """

    def __init__(self, is_valid: bool, message: str, validator_name: str):
        self.is_valid: bool = is_valid
        self.message: str = message
        self.validator_name: str = validator_name

    @override
    def __str__(self):
        status: str = "✓" if self.is_valid else "✗"
        color: str = "green" if self.is_valid else "red"
        return f"[{self.validator_name}] [{color}]{status} {self.message}[/]"


class Handler(ABC):
    """ CHAIN OF RESPONSABILITY PATTERN - Handler abstrato para validações """

    _next_handler: 'Handler | None' = None

    def set_next(self, handler: 'Handler') -> 'Handler':
        self._next_handler = handler
        return handler

    @abstractmethod
    def get_name(self) -> str:
        pass

    @abstractmethod
    def handle(self, content: Conteudo) -> ValidationResult:
        if self._next_handler:
            return self._next_handler.handle(content)

        # quando não houver mais validadores, a cadeia acabou e o conteúdo é válido
        return ValidationResult(
            is_valid=True,
            message="Todas as validações passaram!",
            validator_name="Cadeia de Validações"
        )


class TitleLengthValidation(Handler):
    """ CHAIN OF RESPONSABILITY PATTERN - Validador concreto de tamanho do título """

    def __init__(self, min_size: int = 3, max_size: int = 100):
        self.__min_size: int = min_size
        self.__max_size: int = max_size

    @override
    def get_name(self) -> str:
        return "Validação do Tamanho"

    @override
    def handle(self, content: Conteudo) -> ValidationResult:
        title_size: int = len(content.titulo)

        if title_size < self.__min_size:
            return ValidationResult(
                is_valid=False,
                message=f"O título tem menos do que {
                    self.__min_size} caracteres.",
                validator_name=self.get_name()
            )

        if title_size > self.__max_size:
            return ValidationResult(
                is_valid=False,
                message=f"O título tem mais do que {
                    self.__max_size} caracteres.",
                validator_name=self.get_name()
            )

        console.print(ValidationResult(
            is_valid=True,
            message=f"O título do conteúdo está entre {
                self.__min_size} e {self.__max_size}!",
            validator_name=self.get_name()
        ))

        return super().handle(content)


class TitleWordsValidation(Handler):
    """ CHAIN OF RESPONSABILITY PATTERN - Validador concreto de legibilidade do título """

    @override
    def get_name(self) -> str:
        return "Validação de Legibilidade"

    @override
    def handle(self, content: Conteudo) -> ValidationResult:
        if len(content.titulo.split()) < 2:
            return ValidationResult(
                is_valid=False,
                message="O título tem apenas 1 palavra (dificulta a leitura)",
                validator_name=self.get_name()
            )

        console.print(ValidationResult(
            is_valid=True,
            message="O título está legível.",
            validator_name=self.get_name()
        ))

        return super().handle(content)


class FileFormatValidation(Handler):
    """ CHAIN OF RESPONSABILITY PATTERN - Validador concreto de formato de arquivo """

    def __init__(self):
        self.valid_formats: dict[str, list[str]] = {
            'vídeo': ['.mp4', '.avi'],
            'pdf': ['.pdf'],
            'powerpoint': ['.ppt', '.pptx']
        }

    @override
    def get_name(self) -> str:
        return "Validação de Formato de Arquivo"

    @override
    def handle(self, content: Conteudo) -> ValidationResult:
        if not isinstance(content, Externo):
            return ValidationResult(
                is_valid=True,
                message="Não é conteúdo externo, pulando validação...",
                validator_name=self.get_name()
            )

        file_path = Path(content.caminho)
        file_extension = file_path.suffix.lower()

        if file_extension not in self.valid_formats[content.tipo]:
            return ValidationResult(
                is_valid=False,
                message=f"Extensão {
                    file_extension} não suportada para conteúdos do tipo {content.tipo}",
                validator_name=self.get_name()
            )

        console.print(ValidationResult(
            is_valid=True,
            message=f"O formato {
                file_extension} é válido para o tipo {content.tipo}.",
            validator_name=self.get_name()
        ))

        return super().handle(content)


class FileExistenceValidation(Handler):
    """ CHAIN OF RESPONSABILITY PATTERN - Validador concreto de existência de arquivo """

    @override
    def get_name(self) -> str:
        return "Validação de Existência de Arquivo"

    @override
    def handle(self, content: Conteudo) -> ValidationResult:
        if not isinstance(content, Externo):
            return ValidationResult(
                is_valid=True,
                message="Não é conteúdo externo, pulando validação...",
                validator_name=self.get_name()
            )

        file_path = Path(content.caminho)

        if not file_path.exists():
            return ValidationResult(
                is_valid=False,
                message=f"Arquivo '{file_path}' não encontrado.",
                validator_name=self.get_name()
            )

        if not file_path.is_file():
            return ValidationResult(
                is_valid=False,
                message=f"Caminho '{file_path}' não é um arquivo válido.",
                validator_name=self.get_name()
            )

        console.print(ValidationResult(
            is_valid=True,
            message=f"O arquivo {file_path} existe.",
            validator_name=self.get_name()
        ))

        return super().handle(content)
