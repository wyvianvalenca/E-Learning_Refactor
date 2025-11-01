from typing import Any
from typing_extensions import override

from src.models import (
    ForumPost,
    Usuario
)
from src.menus.strategy_interface import MenuActionStrategy
from src.functions import forum


class AccessForumStrategy(MenuActionStrategy):
    """ STRATEGY PATTERN - Estratégia para acessar o forum """

    @override
    def get_label(self) -> str:
        return "Forum Geral"

    @override
    def execute(self, context: dict[str, Any]) -> None:
        user: Usuario = context['user']
        posts: list[ForumPost] = context['posts']

        self.cabecalho("Acessar Forum Geral")

        forum.mostrar_feed(posts, user, "published")

        return None
