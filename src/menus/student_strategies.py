from typing import Any
from typing_extensions import override

from src.models.models import Student, Course, ForumPost
from src.menus.strategy_interface import MenuActionStrategy
from src.functions.student_functions import (
    adicionar_post,
    inscrever_curso,
    ver_cursos
)
from src.menus.strategies import get_users_courses


class StudentsCoursesStrategy(MenuActionStrategy):
    """ STRATEGY PATTERN - Estratégia para ver os cursos inscritos do aluno """

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
    """ STRATEGY PATTERN - Estratégia para inscrever um aluno em um curso """

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


class AddPostStrategy(MenuActionStrategy):
    """ STRATEGY PATTERN - Estratégia para criar um post no forum geral """

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

        adicionar_post.adicionar_post(student, posts)
