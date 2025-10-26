from typing_extensions import override
from abc import ABC, abstractmethod

import questionary
from rich.console import Console

from src.singleton_metaclass import SingletonABCMeta
from src.models.models import (
    Course,
    Conteudo,
    Externo,
    Texto,
    Questionario,
    Quiz,
    PerguntaQuiz
)
from src.functions.instructor_functions.content_validation import (
    Handler,
    FileExistenceValidation,
    FileFormatValidation,
    TitleWordsValidation,
    TitleLengthValidation,
    ValidationResult
)
from src.functions.instructor_functions.magic_validation import MagicPythonValidationAdapter


class GerenciadorConteudo(ABC, metaclass=SingletonABCMeta):
    """ FACTORY METHOD + SINGLETON PATTERN - Creator abstrato que define a interface para criação, validação e adição de conteúdo """

    def __init__(self, console: Console, tipo: str):
        self.console: Console = console
        self.tipo: str = tipo

    @abstractmethod
    def factory_method(self) -> Conteudo:
        pass

    @abstractmethod
    def validation_chain(self) -> Handler:
        pass

    def adicionar(self, curso_selecionado: Course) -> None:
        novo_conteudo: Conteudo = self.factory_method()

        self.console.print("\nIniciando validação do conteúdo...\n")

        result: ValidationResult = self.validation_chain().handle(novo_conteudo)

        if not result.is_valid:
            self.console.print(
                f"\n[bold][✗] Validação falhou:[/] {result.message}\n",
                style="red"
            )
            self.console.print(
                "O conteúdo [bold]NÃO[/] foi adicionado ao curso.\n",
                style="dark_orange"
            )

            return None

        self.console.print(result)

        self.console.print(
            f"\n✓ Conteúdo '{novo_conteudo.titulo}' adicionado com sucesso!\n",
            style="green"
        )

        curso_selecionado.conteudos.append(novo_conteudo)


class GerenciadorExterno(GerenciadorConteudo, metaclass=SingletonABCMeta):
    """ FACTORY METHOD + SINGLETON PATTERN - Creator concreto para Conteúdos Externos"""

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

    @override
    def validation_chain(self) -> Handler:
        # cria validações padrão
        title_size: Handler = TitleLengthValidation(min_size=10, max_size=100)
        title_case: Handler = TitleWordsValidation()

        # cria validações específicas
        file_existance: Handler = FileExistenceValidation()
        file_format: Handler = FileFormatValidation()
        file_real_type: Handler = MagicPythonValidationAdapter()

        # monta cadeia de validações
        _ = title_size.set_next(title_case) \
            .set_next(file_existance) \
            .set_next(file_format) \
            .set_next(file_real_type)

        # retorna primeira validação da cadeia
        return title_size


class GerenciadorTexto(GerenciadorConteudo, metaclass=SingletonABCMeta):
    """ FACTORY METHOD + SINGLETON PATTERN - Creator concreto para Conteúdo de Texto"""

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

    @override
    def validation_chain(self) -> Handler:
        # cria validações padrão
        title_size: Handler = TitleLengthValidation(min_size=10, max_size=100)
        title_case: Handler = TitleWordsValidation()

        # monta cadeia de validações
        _ = title_size.set_next(title_case)

        # retorna inicio da cadeia
        return title_size


class GerenciadorQuestionario(GerenciadorConteudo, metaclass=SingletonABCMeta):
    """ FACTORY METHOD + SINGLETON PATTERN - Creator concreto para Conteúdo de Quiz"""

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

    @override
    def validation_chain(self) -> Handler:
        # cria validações padrão
        title_size: Handler = TitleLengthValidation(min_size=10, max_size=100)
        title_case: Handler = TitleWordsValidation()

        # monta cadeia de validações
        _ = title_size.set_next(title_case)

        # retorna inicio da cadeia
        return title_size
