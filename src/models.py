from __future__ import annotations

import os
import sys
import subprocess

from typing_extensions import override
from abc import ABC, abstractmethod

import questionary

from rich.panel import Panel
from rich.text import Text
from rich.console import Console
from rich.markdown import Markdown

from src.inicial import console
from src.validations import is_non_empty


# CLASSES DO FORUM


class PostState(ABC):
    """ STATE PATTERN - Interface abstrata para estados do ForumPost """

    def __init__(self):
        self.__post: ForumPost = None

    @property
    def post(self) -> ForumPost:
        return self.__post

    @post.setter
    def post(self, post: ForumPost) -> None:
        self.__post = post
        return None

    @abstractmethod
    def publish(self) -> None:
        pass

    @abstractmethod
    def close(self) -> None:
        pass

    @abstractmethod
    def edit(self) -> bool:
        """Default editing behavior (allowed), return boolean indicating if post was edited"""

        edited: bool = False

        new_name: str = questionary.text(
            "Digite o novo nome (ou deixe vazio para manter):"
        ).ask()

        if new_name:
            self.post.titulo = new_name
            edited = True

        new_content: str = questionary.text(
            "Digite o novo nome (ou deixe vazio para manter):",
            multiline=True
        ).ask()

        if new_content:
            self.post.conteudo = new_content
            edited = True

        return edited

    @abstractmethod
    def render(self) -> None:
        self.render_draft()

        return None

    def render_draft(self) -> None:
        text: str = self.post.header() + " " + self.post.edited + "\n" \
            + self.post.conteudo
        panel: Panel = Panel.fit(Text(text=text).wrap(console, width=100))
        console.print(panel)
        console.print()

        return None

    @abstractmethod
    def comment(self, author: Usuario) -> None:
        conteudo: str = questionary.text(
            "Digite seu comentario:",
            validate=is_non_empty
        ).ask()

        self.post.comentarios.append(Comentario(self.post, conteudo, author))

        console.print("[bold green][OK][/] Comentario adicionado!")

        return None

    def render_comments(self) -> None:
        comments: str = ""

        for comment in self.post.comentarios:
            comments = comments + f"{comment}\n\n"

        console.print(Panel(comments, border_style="gray30"))

        return None

    def log_change(self, new: str) -> None:
        console.print(
            f"\nAlternado \"{self.post.titulo}\" de [bold]{type(self).__name__.upper()}[/] para [bold]{new.upper()}[/]")

        return None

    def log_blocked_action(self, action: str) -> None:
        console.print(
            f"\nVocê não pode {action} um post com estado = {
                type(self).__name__.upper()}"
        )

        return None


class Draft(PostState):
    """STATE PATTERN - Estado concreto Draft (rascunho)"""

    @override
    def publish(self) -> None:
        self.log_change("published")
        self.post.transition_to(Published())

        return None

    @override
    def close(self) -> None:
        """Can't close a draft"""

        self.log_blocked_action("fechar")

        return None

    @override
    def edit(self) -> bool:
        return super().edit()

    @override
    def render(self) -> None:
        """Can't render a draft"""

        self.log_blocked_action("apresentar")

        return None

    @override
    def comment(self, author: Usuario) -> None:
        """Can't comment on a draft"""

        self.log_blocked_action("comentar em")

        return None


class Published(PostState):
    """STATE PATTERN - Estado concreto Published (publicado)"""

    @override
    def publish(self) -> None:
        """Can't publish what's already published"""

        self.log_blocked_action("publicar")

        return None

    @override
    def close(self) -> None:
        self.log_change("closed")
        self.post.transition_to(Closed())

        return None

    @override
    def edit(self) -> bool:
        edited: bool = super().edit()
        if edited:
            self.post.edited = "(editado)"

        return edited

    @override
    def render(self) -> None:
        return super().render()

    @override
    def comment(self, author: Usuario) -> None:
        return super().comment(author)


class Closed(PostState):
    """STATE PATTERN - Estado concreto Closed (fechado)"""

    @override
    def publish(self) -> None:
        """Can't publish a closed post"""

        self.log_blocked_action("publicar")

        return None

    @override
    def close(self) -> None:
        """Can't close a closed post"""

        self.log_blocked_action("fechar")

        return None

    @override
    def edit(self) -> bool:
        """Can't edit a closed post"""

        self.log_blocked_action("editar")

        return False

    @override
    def render(self) -> None:
        return super().render()

    @override
    def comment(self, author: Usuario) -> None:
        """Can't comment on a closed post"""

        self.log_blocked_action("comentar em")

        return None


class Comentario:
    """Classe que representa um comentário em um post do fórum"""

    def __init__(self, pai: ForumPost, conteudo: str, autor: Usuario):
        self.pai: ForumPost = pai
        self.conteudo: str = conteudo
        self.autor: Usuario = autor

    @override
    def __str__(self) -> str:
        return f"{self.autor.nome}\n > {self.conteudo}"


class ForumPost:
    """STATE PATTERN - Context que delega comportamento para estados"""

    def __init__(self, titulo: str, conteudo: str, aluno: Student,
                 state: PostState):
        self.titulo: str = titulo
        self.conteudo: str = conteudo
        self.edited: str = ""
        self.aluno: Student = aluno
        self.comentarios: list[Comentario] = []
        self.__state: PostState = state
        self.__state.post = self

    @property
    def state(self) -> str:
        return type(self.__state).__name__.lower()

    def header(self) -> str:
        return f"> [{type(self.__state).__name__.upper()}] {self.titulo.upper()} por {self.aluno.nome}"

    def transition_to(self, new_state: PostState) -> None:
        self.__state = new_state
        self.__state.post = self

    def publish(self) -> None:
        self.__state.publish()
        return None

    def close(self) -> None:
        self.__state.close()
        return None

    def edit(self) -> None:
        _ = self.__state.edit()
        return None

    def render(self) -> None:
        self.__state.render()
        return None

    def render_draft(self) -> None:
        self.__state.render_draft()
        return None

    def comment(self, author: Usuario) -> None:
        self.__state.comment(author)
        return None

    def render_comments(self) -> None:
        self.__state.render_comments()
        return None


# CLASSES DE CONTEUDO


class PerguntaQuiz:
    """Classe que representa uma pergunta de quiz"""

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
    """Classe que representa um quiz completo"""

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
        """ Apresenta o conteudo e retorna se ele foi consumido ou nao """

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


# CLASSE DE CURSO


class Course:
    """Classe que representa um curso"""

    def __init__(self, titulo: str, descricao: str,
                 instrutor: Instructor,
                 conteudos: list[Conteudo],
                 students: list[Student],
                 preco: float,
                 forum: list[ForumPost],
                 nivel: str,
                 categorias: list[str]):

        self.titulo: str = titulo
        self.descricao: str = descricao
        self.instrutor: Instructor = instrutor
        self.conteudos: list[Conteudo] = conteudos
        self.students: list[Student] = students
        self.forum: list[ForumPost] = forum
        self.nivel: str = nivel
        self.categorias: list[str] = categorias

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


# CLASSES DE CHAT


class mensagem:
    """classe que representa uma mensagem em um chat"""

    def __init__(self, autor: Usuario, conteudo: str):
        self.autor: Usuario = autor
        self.conteudo: str = conteudo

    @override
    def __str__(self) -> str:
        return f"[bold][{self.autor.nome}][/] {self.conteudo}"


class chat:
    """classe que representa um chat entre dois usuários"""

    def __init__(self, user1: Usuario, user2: Usuario):
        self.user1: Usuario = user1
        self.user2: Usuario = user2
        self.mensagens: list[mensagem] = []

    @override
    def __str__(self) -> str:
        return f"chat entre {self.user1.nome} e {self.user2.nome}"


# CLASSES DE USUARIO


class Usuario(ABC):  # abstract base class
    """Classe base abstrata para usuários do sistema"""

    def __init__(self, nome: str, senha: str):
        self.nome: str = nome
        self.__senha: str = senha  # senha está encapsulada
        self.chats: dict[str, Chat] = {}

    @abstractmethod  # método que deve ser implementado por subclasses
    def exibir_menu(self, cursos: list[Course], posts: list[ForumPost]) -> None:
        pass


class Student(Usuario):
    """Classe que representa um estudante"""

    def __init__(self, nome: str, senha: str):
        super().__init__(nome, senha)  # chama o init da classe usuario
        self.cursos_inscritos: list[Course] = []
        self.progresso: dict[str, list[str]] = {}
        self.cursos_pagos: list[Course] = []
        self.posts: list[ForumPost] = []

    @override
    def exibir_menu(self, cursos: list[Course], posts: list[ForumPost]) -> None:
        from src.menus.student_menu import student_menu
        student_menu(self, cursos, posts)


class Instructor(Usuario):
    """Classe que representa um instrutor"""

    def __init__(self, nome: str, senha: str):
        super().__init__(nome, senha)  # aqui tbm chama o init da classe usuario
        self.cursos: list[Course] = []

    @override
    def exibir_menu(self, cursos: list[Course], posts: list[ForumPost]) -> None:
        from src.menus.instructor_menu import instructor_menu
        instructor_menu(self, cursos)
