from typing import Any

from src.inicial import console
from src.models.models import Student, Course, ForumPost
from src.menus.menu_manager import MenuManager
from src.menus.student_strategies import (
    AddPostStrategy,
    StudentsCoursesStrategy,
    SubscribeStrategy
)
from src.menus.strategies import (
    AccessForumStrategy,
    ManageCourseStrategy,
)
from src.menus.exit_strategy import ExitStrategy


def student_menu(student: Student,
                 all_courses: list[Course],
                 main_forum: list[ForumPost]) -> None:
    """STRATEGY PATTERN - Menu para o aluno"""

    # Cria o gerenciador de menus
    menu = MenuManager(
        console,
        f":pencil: Menu do Aluno: {student.nome} :pencil:"
    )

    # Prepara o contexto
    context: dict[str, Any] = {
        'console': console,      # tipo Console
        'user': student,         # tipo Student
        'courses': all_courses,  # tipo list[Course]
        'posts': main_forum      # tipo list[ForumPost]
    }

    # Adiciona as estrategias e roda o menu
    menu.add_strategy(StudentsCoursesStrategy()) \
        .add_strategy(SubscribeStrategy()) \
        .add_strategy(ManageCourseStrategy()) \
        .add_strategy(AccessForumStrategy()) \
        .add_strategy(AddPostStrategy()) \
        .add_strategy(ExitStrategy()) \
        .run(context)
