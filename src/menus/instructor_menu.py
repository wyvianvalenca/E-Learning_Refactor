from src.data_base import posts
from src.inicial import console
from src.models.models import Course, Instructor
from src.menus.menu_manager import MenuManager
from src.menus.instructor_strategies import (
    ListCoursesStrategy,
    AddCourseStrategy,
    DeleteCourseStrategy,
)
from src.menus.strategies import (
    ManageCourseStrategy,
    AccessForumStrategy
)
from src.menus.exit_strategy import ExitStrategy


# STRATEGY MENU
def instructor_menu(instrutor: Instructor, cursos: list[Course]) -> None:
    """Função para criar o menu do instrutor"""

    # Cria o gerenciador de menu
    menu = MenuManager(
        console,
        f":man_teacher: Menu do Instrutor: {instrutor.nome} :man_teacher:"
    )

    # Prepara o contexto
    context = {
        'instructor': instrutor,
        'user': instrutor,
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
