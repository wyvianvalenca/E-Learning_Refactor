from typing import Any
from typing_extensions import override

from rich.console import Console

from src.models.models import Student, Course, ForumPost
from src.menus.menu_strategies import MenuActionStrategy
from src.functions.student_functions import (
    inscrever_curso,
    ver_cursos
)
from src.menus.course_management_menu import course_management_menu
from src.menus.strategies import get_users_courses
from src.functions import forum


class StudentsCoursesStrategy(MenuActionStrategy):
    @override
    def get_label(self) -> str:
        return "Ver Cursos Inscritos"

    @override
    def can_execute(self, context: dict[str, Any]) -> bool:
        student: Student = context['user']
        return len(get_users_courses(student)) > 0

    @override
    def execute(self, context: dict[str, Any]) -> None:
        student: Student = context['user']

        self.cabecalho(f"Cursos Inscritos de {student.nome}")

        ver_cursos.ver_cursos(student)

        return self.retornar()


class SubscribeStrategy(MenuActionStrategy):
    @override
    def get_label(self) -> str:
        return "Inscrever em Curso"

    @override
    def can_execute(self, context: dict[str, Any]) -> bool:
        return isinstance(context['user'], Student)

    @override
    def execute(self, context: dict[str, Any]) -> None:
        student: Student = context['user']
        courses: list[Course] = context['courses']

        self.cabecalho("Inscrever em Curso")

        inscrever_curso.executar(student, courses)

        return self.retornar()


class AccessCourseStrategy(MenuActionStrategy):
    @override
    def get_label(self) -> str:
        return "Acessar Curso"

    @override
    def can_execute(self, context: Any) -> bool:
        student: Student = context['user']
        return len(get_users_courses(student)) > 0

    @override
    def execute(self, context: dict[str, Any]) -> None:
        student: Student = context['user']
        students_courses: list[Course] = get_users_courses(student)
        console: Console = context['console']

        course_management_menu(console, students_courses, student)

        return None


class AddPostStrategy(MenuActionStrategy):
    @override
    def get_label(self) -> str:
        return "Criar Post no Forum Geral"

    @override
    def can_execute(self, context: dict[str, Any]) -> bool:
        return isinstance(context['user'], Student)

    @override
    def execute(self, context: dict[str, Any]) -> None:
        student: Student = context['user']
        posts: list[ForumPost] = context['posts']

        self.cabecalho("Forum Geral")

        forum.mostrar_feed(posts, student)
