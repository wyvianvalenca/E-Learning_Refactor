from typing import Any
from typing_extensions import override

from instrutor import listar_cursos, criar_curso, excluir_curso
from instrutor.gerenciador_cursos import course_management_menu
from menu_strategies import MenuActionStrategy
from models import Instructor, Course, ForumPost
from inicial import console
from aluno import forum


def cursos_instrutor(cursos: list[Course], instrutor: Instructor) -> list[Course]:
    instructor_courses_list: list[Course] = [
        curso for curso in cursos if curso.instrutor == instrutor
    ]
    return instructor_courses_list


# CONCRETE INSTRUCTOR STRATEGIES


class ListCoursesStrategy(MenuActionStrategy):
    @override
    def get_label(self) -> str:
        return "Listar Meus Cursos"

    def execute(self, context: dict[str, Any]) -> None:
        instrutor: Instructor = context['instructor']
        cursos: list[Course] = context['courses']

        self.cabecalho(f"Cursos de [bold]{instrutor.nome}[/]")

        listar_cursos.executar(instrutor, cursos)

        return self.retornar()


class AddCourseStrategy(MenuActionStrategy):
    @override
    def get_label(self) -> str:
        return "Criar Curso"

    def execute(self, context: dict[str, Any]) -> None:
        instrutor: Instructor = context['instructor']
        cursos: list[Course] = context['courses']

        self.cabecalho("Criar Curso")

        criar_curso.executar(instrutor, cursos)

        return self.retornar()


class ManageCourseStrategy(MenuActionStrategy):
    @override
    def get_label(self) -> str:
        return "Gerenciar Curso"

    @override
    def execute(self, context: dict[str, Any]) -> None:
        instrutor: Instructor = context['instructor']
        cursos: list[Course] = context['courses']

        course_management_menu(console, cursos_instrutor(cursos, instrutor), instrutor)

    @override
    def can_execute(self, context: dict[str, Any]) -> bool:
        instrutor: Instructor = context['instructor']
        cursos: list[Course] = context['courses']

        return len(cursos_instrutor(cursos, instrutor)) > 0


class DeleteCourseStrategy(MenuActionStrategy):
    @override
    def get_label(self) -> str:
        return "Excluir Curso"

    @override
    def execute(self, context: dict[str, Any]) -> None:
        instrutor: Instructor = context['instructor']
        cursos: list[Course] = context['courses']

        self.cabecalho("Excluir Curso")

        excluir_curso.executar(instrutor, cursos)

        return self.retornar()

    @override
    def can_execute(self, context: dict[str, Any]) -> bool:
        instrutor: Instructor = context['instructor']
        cursos: list[Course] = context['courses']

        return len(cursos_instrutor(cursos, instrutor)) > 0


class AccessForumStrategy(MenuActionStrategy):
    @override
    def get_label(self) -> str:
        return "Acessar Forum"

    @override
    def execute(self, context: dict[str, Any]) -> None:
        instructor: Instructor = context['instructor']
        posts: list[ForumPost] = context['posts']

        self.cabecalho("Acessar Forum")

        forum.mostrar_feed(posts, instructor)

        return None