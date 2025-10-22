import os
import sys
import subprocess

from typing_extensions import override
from abc import ABC, abstractmethod

import questionary

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.text import Text

from src.inicial import console
from src.validations import is_non_empty


class Course:
    def __init__(self, titulo: str, descricao: str,
                 instrutor: 'Instructor',
                 conteudos: list['Conteudo'],
                 students: list['Student'],
                 preco: float,
                 forum: list['ForumPost'],
                 nivel: str,
                 categorias: list[str]):

        self.titulo: str = titulo
        self.descricao: str = descricao
        self.instrutor: Instructor = instrutor
        self.conteudos: list[Conteudo] = conteudos
        self.students: list[Student] = students
        self.forum: list['ForumPost'] = forum
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


# classe usuario criada para implementar herança
# assim, Student e Instructor herdam de Usuario
class Usuario(ABC):  # abstract base class
    def __init__(self, nome: str, senha: str):
        self.nome: str = nome
        self.__senha: str = senha  # senha está encapsulada

    @abstractmethod  # método que deve ser implementado por subclasses
    def exibir_menu(self, cursos: list[Course], posts: list['ForumPost']) -> None:
        pass


class Student(Usuario):
    def __init__(self, nome: str, senha: str):
        super().__init__(nome, senha)  # chama o init da classe usuario
        self.cursos_inscritos: list[Course] = []
        self.progresso: dict[str, list[str]] = {}
        self.cursos_pagos: list[Course] = []
        self.notas_quizzes = {}
        self.chats: dict[str, 'Chat'] = {}
        self.posts: list['ForumPost'] = []

    @override
    def exibir_menu(self, cursos: list[Course], posts: list['ForumPost']) -> None:
        from src.menus.student_menu import student_menu
        student_menu(self, cursos, posts)


class Instructor(Usuario):
    def __init__(self, nome: str, senha: str):
        super().__init__(nome, senha)  # aqui tbm chama o init da classe usuario
        self.cursos: list[Course] = []

    @override
    def exibir_menu(self, cursos: list[Course], posts: list['ForumPost']) -> None:
        from src.menus.instructor_menu import instructor_menu
        instructor_menu(self, cursos)


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


class ForumPost:
    def __init__(self, titulo: str, conteudo: str, aluno: Student,
                 state: 'PostState'):
        self.titulo: str = titulo
        self.conteudo: str = conteudo
        self.edited: str = ""
        self.aluno: Student = aluno
        self.comentarios: list[Comentario] = []
        self.__state: 'PostState' = state
        self.__state.post = self

    def header(self) -> str:
        return f"> [{type(self.__state).__name__.upper()}] {self.titulo.upper()} por {self.aluno.nome}"

    def transition_to(self, new_state: 'PostState') -> None:
        self.__state = new_state
        self.__state.post = self

    def publish(self) -> None:
        self.__state.publish()
        return None

    def close(self) -> None:
        self.__state.close()
        return None

    def edit(self) -> None:
        self.__state.edit()
        return None

    def render(self) -> None:
        self.__state.render()
        return None

    def comment(self, author: Usuario) -> None:
        self.__state.comment(author)
        return None

    def render_comments(self) -> None:
        self.__state.show_comments()
        return None


"""
FORUM POST STATES
1. Draft
    > can publish
    > can't close
    > can edit
    > can't render
    > can't comment

2. Published
    > can't publish
    > can close
    > can edit (adds edited flag)
    > can render
    > can comment

3. Closed
    > can't publish
    > can't close
    > can't edit
    > can render
    > can't comment
"""


class PostState(ABC):
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
    def edit(self) -> None:
        new_name: str = questionary.text(
            "Digite o novo nome (ou <Enter> para manter):"
        ).ask()

        if new_name:
            self.post.titulo = new_name

        new_content: str = questionary.text(
            "Digite o novo nome (ou <Enter> para manter):",
            multiline=True
        ).ask()

        if new_content:
            self.post.conteudo = new_content

        return None

    @abstractmethod
    def render(self) -> None:
        text: str = self.post.header() + "\n" \
            + self.post.edited + "\n" \
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

    def show_comments(self) -> None:
        comments: str = ""

        for comment in self.post.comentarios:
            comments = comments + f"{comment}\n\n"

        console.print(Panel(comments, border_style="gray30"))

        questionary.press_any_key_to_continue(
            "Pressione qualquer tecla para voltar ao feed").ask()

        return None

    def log_change(self, new: str) -> None:
        console.print(
            f"Changing {self.post.titulo} from [bold]{type(self).__name__}[/] to [bold]{new}[/]")

        return None

    def log_blocked_action(self, action: str) -> None:
        console.print(
            f"You can't {action} a post that is {type(self).__name__.upper()}"
        )

        return None


class Draft(PostState):
    @override
    def publish(self) -> None:
        self.log_change("published")
        self.post.transition_to(Published())

        return None

    @override
    def close(self) -> None:
        """Can't close a draft"""

        self.log_blocked_action("close")

        return None

    @override
    def edit(self) -> None:
        super().edit()

        return None

    @override
    def render(self) -> None:
        """Can't render a draft"""

        self.log_blocked_action("render")

        return None

    @override
    def comment(self, author: Usuario) -> None:
        """Can't comment on a draft"""

        self.log_blocked_action("comment on")

        return None


class Published(PostState):
    @override
    def publish(self) -> None:
        """Can't publish what's already published"""

        self.log_blocked_action("publish")

        return None

    @override
    def close(self) -> None:
        self.log_change("closed")
        self.post.transition_to(Closed())

        return None

    @override
    def edit(self) -> None:
        super().edit()
        self.post.edited = "[EDITADO]"

        return None

    @override
    def render(self) -> None:
        return super().render()

    @override
    def comment(self, author: Usuario) -> None:
        return super().comment(author)


class Closed(PostState):
    @override
    def publish(self) -> None:
        """Can't publish a closed post"""

        self.log_blocked_action("publish")

        return None

    @override
    def close(self) -> None:
        """Can't close a closed post"""

        self.log_blocked_action("close")

        return None

    @override
    def edit(self) -> None:
        """Can't edit a closed post"""

        self.log_blocked_action("edit")

        return None

    @override
    def render(self) -> None:
        return super().render()

    @override
    def comment(self, author: Usuario) -> None:
        """Can't comment on a closed post"""

        self.log_blocked_action("comment on")

        return None


class Comentario:
    def __init__(self, pai: ForumPost, conteudo: str, autor: Usuario):
        self.pai: ForumPost = pai
        self.conteudo: str = conteudo
        self.autor: Usuario = autor

    @override
    def __str__(self) -> str:
        return f"{self.autor.nome}\n > {self.conteudo}"


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
