from typing_extensions import override
from abc import ABC, abstractmethod

import questionary

from rich.console import Console

from singleton_metaclass import SingletonABCMeta, SingletonMeta

from models.models import (
    Course,
    Conteudo,
    Externo,
    Texto,
    Questionario,
    Quiz,
    PerguntaQuiz
)


""" FACTORY METHOD """


class GerenciadorConteudo(ABC, metaclass=SingletonABCMeta):
    """Criador Abstrato / Interface de Criador para os gerenciadores de conteúdo"""

    def __init__(self, console: Console, tipo: str):
        self.console: Console = console
        self.tipo: str = tipo

    @abstractmethod
    def factory_method(self) -> Conteudo:
        pass

    def adicionar(self, curso_selecionado: Course) -> None:
        novo_conteudo: Conteudo = self.factory_method()
        curso_selecionado.conteudos.append(novo_conteudo)


class GerenciadorExterno(GerenciadorConteudo, metaclass=SingletonABCMeta):
    """Criador concreto para Conteúdos Externos"""

    @override
    def factory_method(self) -> Conteudo:
        titulo: str = questionary.text(
            "Digite o título do conteúdo:").ask()

        duracao: str = questionary.text(
            "Informe a duração do conteúdo (em minutos):",
            validate=lambda text: True if int(text) > 0 else "A duração precisa ser positiva").ask()

        caminho: str = questionary.text(
            "Informe o caminho para o arquivo:").ask()

        novo_externo: Externo = Externo(self.console, titulo,
                                        self.tipo, int(duracao), caminho)

        return novo_externo


class GerenciadorTexto(GerenciadorConteudo, metaclass=SingletonABCMeta):
    """Criador concreto para Conteúdo de Texto"""

    @override
    def factory_method(self) -> Conteudo:
        titulo: str = questionary.text(
            "Digite o título do conteúdo:").ask()

        duracao: str = questionary.text(
            "Informe a duração do conteúdo (em minutos):",
            validate=lambda text: True if int(text) > 0 else "A duração precisa ser positiva").ask()

        texto: str = questionary.text(
            "Digite o texto completo:",
            multiline=True).ask()

        novo_texto: Texto = Texto(self.console, titulo,
                                  self.tipo, int(duracao), texto)

        return novo_texto


class GerenciadorQuestionario(GerenciadorConteudo, metaclass=SingletonABCMeta):
    """Criador concreto para Conteúdo de Quiz"""

    def criar_quiz(self) -> Quiz:
        self.console.print(f"\n--- CRIAR NOVO QUIZ ---\n")
        titulo_quiz: str = questionary.text("Digite o nome do quiz:").ask()

        perguntas: list[PerguntaQuiz] = []

        while True:
            self.console.print(f"\nPergunta {len(perguntas) + 1}:\n")

            enunciado: str = questionary.text(
                "Digite o enunciado da questão:").ask()

            alternativas: str = questionary.text(
                "Digite as alternativas (separadas por vírgula):").ask()
            opcoes: list[str] = [opt.strip() for opt in alternativas.split()]

            correta: str = questionary.select(
                "Selecione a alternativa correta:",
                choices=opcoes).ask()

            nova_pergunta: PerguntaQuiz = PerguntaQuiz(
                enunciado, opcoes, correta)

            perguntas.append(nova_pergunta)

            outra: bool = questionary.confirm(
                "Deseja adicionar outra pergunta?").ask()

            if not outra:
                break

        return Quiz(titulo_quiz, perguntas)

    @override
    def factory_method(self) -> Conteudo:
        titulo: str = questionary.text(
            "Digite o título do conteúdo:").ask()

        duracao: str = questionary.text(
            "Informe a duração do conteúdo (em minutos):",
            validate=lambda text: True if int(text) > 0 else "A duração precisa ser positiva").ask()

        # criar quiz
        quiz: Quiz = self.criar_quiz()

        novo_questionario: Questionario = Questionario(self.console, titulo,
                                                       self.tipo, int(duracao),
                                                       quiz)

        return novo_questionario