import os
import sys
import subprocess

import questionary

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

from typing_extensions import override
from abc import ABC, abstractmethod


class Course:
    def __init__(self, titulo: str, descricao: str,
                 instrutor: 'Instructor',
                 conteudos: list['Conteudo'] | None = None,
                 students: list['Student'] | None = None,
                 preco: float = 0.0):

        self.titulo: str = titulo
        self.descricao: str = descricao
        self.instrutor: Instructor = instrutor
        self.conteudos: list[Conteudo] = conteudos if conteudos is not None else [
        ]
        self.students: list[Student] = students if students is not None else []

        # underline (convenção), indicando que é "privado"
        self.__preco: float = preco  # preco esta encapsulado

    @property  # getter só retorna o valor
    def preco(self) -> float:
        return self.__preco

    @preco.setter  # setter controla o valor definto
    def preco(self, novo_preco: float):

        if novo_preco >= 0:
            self.__preco = novo_preco
        else:
            print("Erro: O preço de um curso não pode ser negativo.")


# classe usuario criada para implementar herança
# assim, Student e Instructor herdam de Usuario
class Usuario(ABC):  # abstract base class
    def __init__(self, nome, senha):
        self.nome = nome
        self.__senha = senha  # senha está encapsulada

    @abstractmethod  # método que deve ser implementado por subclasses
    def exibir_menu(self, cursos: list[Course], posts: list['ForumPost']) -> None:
        pass


class Student(Usuario):
    def __init__(self, nome, senha, cursos_inscritos=None, cursos_pagos=None, progresso=None, notas_quizzes=None):
        super().__init__(nome, senha)  # chama o init da classe usuario
        self.cursos_inscritos: list[Course] = cursos_inscritos if cursos_inscritos is not None else [
        ]
        self.progresso: dict[str, list[str]
                             ] = progresso if progresso is not None else {}
        self.cursos_pagos = cursos_pagos if cursos_pagos is not None else []
        self.notas_quizzes = notas_quizzes if notas_quizzes is not None else {}
        self.chats: dict[str, 'Chat'] = {}

    @override
    def exibir_menu(self, cursos: list[Course], posts: list['ForumPost']) -> None:
        from aluno.funcoes_aluno import menu_aluno
        menu_aluno(self, cursos, posts)


class Instructor(Usuario):
    def __init__(self, nome, senha):
        super().__init__(nome, senha)  # aqui tbm chama o init da classe usuario
        self.cursos = []

    @override
    def exibir_menu(self, cursos: list[Course], posts: list['ForumPost']) -> None:
        from instrutor.funcoes_instrutor import menu_instrutor, menu_instrutor_strategy
        menu_instrutor_strategy(self, cursos)


class PerguntaQuiz:
    # aqui vai ficas as perguntas do quiz
    def __init__(self, pergunta: str,
                 alternativas: list[str],
                 resposta: str):
        self.pergunta: str = pergunta
        self.alternativas: list[str] = alternativas
        self.resposta: str = resposta

    @override
    def __repr__(self):
        return f"[PerguntaQuiz] {self.pergunta} - {self.alternativas})"

    def acertou(self, alternativaEscolhida: str) -> bool:
        return alternativaEscolhida == self.resposta


class Quiz:
    # quiz completo
    def __init__(self, titulo: str, perguntas: list[PerguntaQuiz]):
        self.titulo: str = titulo
        self.perguntas: list[PerguntaQuiz] = perguntas

    @override
    def __repr__(self):
        return f"[Quiz] {self.titulo} ({len(self.perguntas)} perguntas)"

    @override
    def __str__(self) -> str:
        return self.__repr__()

    def criar_formulario(self) -> list[dict[str, str | list[str]]]:
        formulario: list[dict[str, str | list[str]]] = []
        for pergunta in self.perguntas:
            formulario.append({
                "type": "select",
                "name": pergunta.pergunta,
                "message": pergunta.pergunta,
                "choices": pergunta.alternativas
            })
        return formulario

    def nota(self, respostas: dict[str, str]) -> int:
        acertos: int = 0
        for pergunta in self.perguntas:
            if pergunta.acertou(respostas[pergunta.pergunta]):
                acertos += 1

        return acertos


class Conteudo(ABC):
    # produto abstrato
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
    # produto concreto
    def __init__(self, console: Console,
                 titulo: str, tipo: str, duracao: int, caminho: str) -> None:
        super().__init__(console, titulo, tipo, duracao)
        self.caminho: str = caminho

    @override
    def apresentar(self) -> bool:
        self.abrir_arquivo(self.caminho)
        return True


class Texto(Conteudo):
    # produto concreto
    def __init__(self, console: Console,
                 titulo: str, tipo: str, duracao: int, texto: str) -> None:
        super().__init__(console, titulo, tipo, duracao)
        self.texto: str = texto

    @override
    def apresentar(self) -> bool:
        self.console.print(Panel.fit(Markdown(self.texto)))
        return True


class Questionario(Conteudo):
    # produto concreto
    def __init__(self, console: Console,
                 titulo: str, tipo: str, duracao: int, quiz: Quiz) -> None:
        super().__init__(console, titulo, tipo, duracao)
        self.quiz: Quiz = quiz

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


class Comentario:
    def __init__(self, pai: 'ForumPost', conteudo: str, autor: Usuario):
        self.pai: 'ForumPost' = pai
        self.conteudo: str = conteudo
        self.autor: Usuario = autor

    @override
    def __str__(self) -> str:
        return f"{self.autor.nome}\n > {self.conteudo}"


class ForumPost:
    def __init__(self, titulo: str, conteudo: str, aluno: Student):
        self.titulo: str = titulo
        self.conteudo: str = conteudo
        self.aluno: Student = aluno
        self.comentarios: list[Comentario] = []

    def header(self) -> str:
        return f"> {self.titulo.upper()} por {self.aluno.nome}"


class Mensagem:
    def __init__(self, autor: Usuario, conteudo: str):
        self.autor: Usuario = autor
        self.conteudo: str = conteudo

    @override
    def __str__(self) -> str:
        return f"[bold][{self.autor.nome}][/] {self.conteudo}"


class Chat:
    def __init__(self, user1: Usuario, user2: Student | Instructor):
        self.user1: Usuario = user1
        self.user2: Usuario = user2
        self.mensagens: list[Mensagem] = []

    @override
    def __str__(self) -> str:
        return f"Chat entre {self.user1.nome} e {self.user2.nome}"
