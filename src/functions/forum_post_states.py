from abc import ABC, abstractmethod
from typing_extensions import override

import questionary
from rich.panel import Panel
from rich.text import Text

from src.inicial import console
from src.models.models import ForumPost, Usuario, Comentario
from src.validations import is_non_empty


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
