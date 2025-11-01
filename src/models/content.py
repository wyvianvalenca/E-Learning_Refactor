from __future__ import annotations

import os
import sys
import subprocess

from typing_extensions import override
from abc import ABC, abstractmethod

import questionary

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

from src.models import Quiz


class Conteudo(ABC):
    """Classe abstrata que representa um conteúdo do curso"""

    def __init__(self, console: Console,
                 titulo: str, tipo: str, duracao_minutos: int):
        self.console: Console = console
        self.titulo: str = titulo.lower()
        self.tipo: str = tipo.lower()  # pode ser omitido...
        self.duracao_minutos: int = duracao_minutos

    @override
    def __repr__(self) -> str:
        return f"[{self.tipo.upper()}] {self.titulo.title()} ({self.duracao_minutos} min)"

    @override
    def __str__(self) -> str:
        return self.__repr__()

    @abstractmethod
    def apresentar(self) -> bool:
        '''Apresenta o conteudo e retorna se ele foi consumido ou nao'''
        pass

    @staticmethod
    def abrir_arquivo(filename: str) -> None:
        if sys.platform == "win32":
            os.startfile(filename)
        else:
            opener = "open" if sys.platform == "darwin" else "xdg-open"
            _ = subprocess.call([opener, filename])


class Externo(Conteudo):
    """Classe que representa conteúdo externo (PDF, vídeo, etc.)"""

    def __init__(self, console: Console,
                 titulo: str, tipo: str, duracao: int, caminho: str) -> None:
        super().__init__(console, titulo, tipo, duracao)
        self.caminho: str = caminho

    @override
    def apresentar(self) -> bool:
        self.abrir_arquivo(self.caminho)
        return True


class Texto(Conteudo):
    """Classe que representa conteúdo de texto"""

    def __init__(self, console: Console,
                 titulo: str, tipo: str, duracao: int, texto: str) -> None:
        super().__init__(console, titulo, tipo, duracao)
        self.texto: str = texto

    @override
    def apresentar(self) -> bool:
        self.console.print(Panel.fit(Markdown(self.texto)))
        return True


class Questionario(Conteudo):
    """Classe que representa um questionário/quiz"""

    def __init__(self, console: Console,
                 titulo: str, tipo: str, duracao: int, quiz: 'Quiz') -> None:
        super().__init__(console, titulo, tipo, duracao)
        self.quiz: 'Quiz' = quiz

    @override
    def apresentar(self) -> bool:
        self.console.print(f"\n--- Iniciando Quiz: {self.quiz.titulo.title()}")
        respostas: dict[str, str] = questionary.prompt(
            self.quiz.criar_formulario())

        corretas: int = self.quiz.nota(respostas)
        total: int = len(self.quiz.perguntas)

        self.console.print("\n--- Resultado do Quiz ---")
        self.console.print(f"Você acertou {corretas} de {total} perguntas.")

        return corretas == total
