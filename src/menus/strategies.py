from typing import Any
from typing_extensions import override

from src.inicial import console
from src.models.models import Instructor, Course, ForumPost, Student, Usuario
from src.menus.menu_strategies import MenuActionStrategy
from src.menus.course_management_menu import course_management_menu
from src.functions import forum


# def cursos_instrutor(all_courses: list[Course], instructor: Instructor) -> list[Course]:
#     instructor_courses_list: list[Course] = [
#         curso for curso in all_courses if curso.instrutor == instructor
#     ]
#     return instructor_courses_list


def get_users_courses(user: Instructor | Student) -> list[Course]:
    if isinstance(user, Instructor):
        return user.cursos
    else:
        return user.cursos_inscritos


class ManageCourseStrategy(MenuActionStrategy):
    @override
    def get_label(self) -> str:
        return "Gerenciar Curso"

    @override
    def execute(self, context: dict[str, Any]) -> None:
        user: Student | Instructor = context['user']
        users_courses: list[Course] = get_users_courses(user)
        # cursos: list[Course] = context['courses']

        # course_management_menu(console, cursos_instrutor(cursos, user), user)
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
