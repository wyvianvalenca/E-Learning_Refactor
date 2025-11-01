from typing_extensions import override
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

import questionary

from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from src.inicial import console
from src.validations import is_non_empty

if TYPE_CHECKING:
    from src.models.user import Usuario, Student


class Comentario:
    """Classe que representa um comentário em um post do fórum"""
    
    def __init__(self, pai: 'ForumPost', conteudo: str, autor: 'Usuario'):
        self.pai: 'ForumPost' = pai
        self.conteudo: str = conteudo
        self.autor: 'Usuario' = autor

    @override
    def __str__(self) -> str:
        return f"{self.autor.nome}\n > {self.conteudo}"


class PostState(ABC):
    """ STATE PATTERN - Interface abstrata para estados do ForumPost """

    def __init__(self):
        self.__post: 'ForumPost' = None

    @property
    def post(self) -> 'ForumPost':
        return self.__post

    @post.setter
    def post(self, post: 'ForumPost') -> None:
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
    def comment(self, author: 'Usuario') -> None:
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
            f"\nVocê não pode {action} um post com estado = {type(self).__name__.upper()}"
        )

        return None


class Draft(PostState):
    """STATE PATTERN - Estado concreto Draft (rascunho)"""

    @override
    def publish(self) -> None:
        # Importação local para evitar dependência circular
        from src.models.forum import Published
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
    def comment(self, author: 'Usuario') -> None:
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
        # Importação local para evitar dependência circular
        from src.models.forum import Closed
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
    def comment(self, author: 'Usuario') -> None:
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
    def comment(self, author: 'Usuario') -> None:
        """Can't comment on a closed post"""

        self.log_blocked_action("comentar em")

        return None


class ForumPost:
    """STATE PATTERN - Context que delega comportamento para estados"""

    def __init__(self, titulo: str, conteudo: str, aluno: 'Student',
                 state: PostState):
        self.titulo: str = titulo
        self.conteudo: str = conteudo
        self.edited: str = ""
        self.aluno: 'Student' = aluno
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

    def comment(self, author: 'Usuario') -> None:
        self.__state.comment(author)
        return None

    def render_comments(self) -> None:
        self.__state.render_comments()
        return None
