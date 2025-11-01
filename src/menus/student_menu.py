from typing import Any

from src.inicial import console
from src.logging.strategy_logging_decorator import LoggingDecoratorStrategy
from src.models import Student, Course, ForumPost
from src.menus.menu_manager import MenuManager
from src.menus.student_strategies import (
    AccessDraftPostsStrategy,
    AddPostStrategy,
    StudentsCoursesStrategy,
    SubscribeStrategy
)
from src.functions.access_forum import AccessForumStrategy
from src.functions.manage_course import ManageCourseStrategy
from src.functions.exit_strategy import ExitStrategy


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
        .add_strategy(LoggingDecoratorStrategy(SubscribeStrategy())) \
        .add_strategy(ManageCourseStrategy()) \
        .add_strategy(LoggingDecoratorStrategy(AddPostStrategy())) \
        .add_strategy(AccessForumStrategy()) \
        .add_strategy(AccessDraftPostsStrategy()) \
        .add_strategy(ExitStrategy()) \
        .run(context)
