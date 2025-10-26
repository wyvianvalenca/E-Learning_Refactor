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
from src.functions.forum import mostrar_feed


class StudentsCoursesStrategy(MenuActionStrategy):
    """ STRATEGY PATTERN - Estratégia para ver os cursos inscritos do aluno """

    @override
    def get_label(self) -> str:
        return "Ver Meus Cursos"

    @override
    def can_execute(self, context: dict[str, Any]) -> bool:
        student: Student = context['user']
        return len(get_users_courses(student)) > 0

    @override
    def execute(self, context: dict[str, Any]) -> None:
        student: Student = context['user']

        self.cabecalho(f"Cursos de {student.nome}")

        ver_cursos.ver_cursos(student)

        return self.retornar()


class SubscribeStrategy(MenuActionStrategy):
    """ STRATEGY PATTERN - Estratégia para inscrever um aluno em um curso """

    @override
    def get_label(self) -> str:
        return "Inscrever-se em Novo Curso"

    @override
    def can_execute(self, context: dict[str, Any]) -> bool:
        return isinstance(context['user'], Student)

    @override
    def execute(self, context: dict[str, Any]) -> None:
        student: Student = context['user']
        courses: list[Course] = context['courses']

        self.cabecalho(self.get_label())

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

        return None


class AccessDraftPostsStrategy(MenuActionStrategy):
    """ STRATEGY PATTERN - Estratégia para ver e editar os rascunhos de posts do aluno """

    @override
    def get_label(self) -> str:
        return "Ver Rascunhos de Posts"

    @override
    def can_execute(self, context: dict[str, Any]) -> bool:
        return isinstance(context['user'], Student)

    @override
    def execute(self, context: dict[str, Any]) -> None:
        student: Student = context['user']

        # Captura somente os rascunhos do aluno
        drafts: list[ForumPost] = [
            p for p in student.posts if p.state == "draft"]

        mostrar_feed(drafts, student, "drafts")
