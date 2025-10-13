from inicial import console
from data_base import posts
from models import Course, Instructor

from menu_manager import MenuManager
from instrutor.instructor_strategies import (
    ListCoursesStrategy,
    AddCourseStrategy,
    ManageCourseStrategy,
    DeleteCourseStrategy,
    AccessForumStrategy
)
from menu_strategies import ExitStrategy


# STRATEGY MENU
def menu_instrutor_strategy(instrutor: Instructor, cursos: list[Course]) -> None:
    """Função para criar o menu do instrutor"""

    # Cria o gerenciador de menu
    menu = MenuManager(
        console,
        f":man_teacher: Menu do Instrutor: {instrutor.nome} :man_teacher:"
    )

    # Prepara o contexto
    context = {
        'instructor': instrutor,
        'courses': cursos,
        'posts': posts
    }

    # Adiciona as estratégias na ordem desejada e roda o menu
    menu.add_strategy(ListCoursesStrategy()) \
        .add_strategy(AddCourseStrategy()) \
        .add_strategy(ManageCourseStrategy()) \
        .add_strategy(DeleteCourseStrategy()) \
        .add_strategy(AccessForumStrategy()) \
        .add_strategy(ExitStrategy()) \
        .run(context)