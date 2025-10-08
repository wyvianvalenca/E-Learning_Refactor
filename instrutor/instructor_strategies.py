from typing import Any
from typing_extensions import override

from instrutor import listar_cursos, criar_curso, excluir_curso
from instrutor.gerenciador_cursos import GerenciadorCurso
from menu_strategies import MenuActionStrategy
from models import Instructor, Course, ForumPost
from inicial import console
from aluno import forum

def cursos_instrutor(cursos: list[Course], instrutor: Instructor) -> list[Course]:
    instructor_courses_list: list[Course] = [
        curso for curso in cursos if curso.instrutor == instrutor
    ]
    return instructor_courses_list

class ListCoursesStrategy(MenuActionStrategy):
    @override
    def get_label(self) -> str:
        return "Listar Meus Cursos"

    def execute(self, context: dict[str, Any]) -> None:
        instrutor: Instructor = context['instructor']
        cursos: list[Course] = context['courses']
        listar_cursos.executar(instrutor, cursos)
        return None

class AddCourseStrategy(MenuActionStrategy):
    @override
    def get_label(self) -> str:
        return "Criar Curso"

    def execute(self, context: dict[str, Any]) -> None:
        instrutor: Instructor = context['instructor']
        cursos: list[Course] = context['courses']
        criar_curso.executar(instrutor, cursos)
        return None

class ManageCourseStrategy(MenuActionStrategy):
    @override
    def get_label(self) -> str:
        return "Gerenciar Curso"

    def execute(self, context: dict[str, Any]) -> None:
        instrutor: Instructor = context['instructor']
        cursos: list[Course] = context['courses']

        GerenciadorCurso(console).menu(cursos_instrutor(cursos, instrutor))
        return None

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

        excluir_curso.executar(instrutor, cursos)
        return None

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
        forum.mostrar_feed(posts, instructor)

class ExitStrategy(MenuActionStrategy):
    def get_label(self) -> str:
        return "Sair"

    def execute(self, context: dict[str, Any]) -> None:
        console.print("\nSaindo do menu do instrutor. Até logo!")
        context['continue'] = False  # Sinaliza para parar o loop
        return None