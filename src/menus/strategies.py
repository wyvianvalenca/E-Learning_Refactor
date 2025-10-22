from typing import Any
from typing_extensions import override

from src.inicial import console
from src.models.models import Instructor, Course, ForumPost, Student, Usuario
from src.menus.strategy_interface import MenuActionStrategy
from src.menus.course_management_menu import course_management_menu
from src.functions import forum


def get_users_courses(user: Instructor | Student) -> list[Course]:
    if isinstance(user, Instructor):
        return user.cursos
    else:
        return user.cursos_inscritos


class ManageCourseStrategy(MenuActionStrategy):
    @override
    def get_label(self) -> str:
        return "Acessar Curso"

    @override
    def execute(self, context: dict[str, Any]) -> None:
        user: Student | Instructor = context['user']
        users_courses: list[Course] = get_users_courses(user)

        self.cabecalho("Acessar um Curso")

        course_management_menu(console, users_courses, user)


class AccessForumStrategy(MenuActionStrategy):
    @override
    def get_label(self) -> str:
        return "Acessar Forum"

    @override
    def execute(self, context: dict[str, Any]) -> None:
        user: Usuario = context['user']
        posts: list[ForumPost] = context['posts']

        self.cabecalho("Acessar Forum")

        forum.mostrar_feed(posts, user)

        return None
