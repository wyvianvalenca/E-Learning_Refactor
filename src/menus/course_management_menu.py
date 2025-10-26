import questionary
from rich.console import Console

from src.models.models import Usuario, Course
from src.menus.menu_manager import MenuManager
from src.menus.course_management_strategies import (
    AddPostCourseStrategy,
    CoursePlatformStrategy,
    PerformanceStrategy,
    UpdateInfoStrategy,
    ViewContentStrategy,
    AddContentStrategy,
    RemoveContentStrategy,
    ReportStrategy,
    # CourseForumStrategy
)
from src.menus.exit_strategy import ExitStrategy


def escolher_curso(cursos_instrutor: list[Course]) -> None | Course:
    """ Função para escolher um curso """

    nomes_cursos: list[str] = [c.titulo for c in cursos_instrutor]
    nomes_cursos.append("Sair")
    escolhido: str = questionary.select("Selecione o curso que deseja gerenciar:",
                                        choices=nomes_cursos).ask()

    if escolhido == "Sair":
        return None

    for curso in cursos_instrutor:
        if curso.titulo == escolhido:
            return curso


def course_management_menu(console: Console, cursos: list[Course], usuario: Usuario) -> None:
    """ STRATEGY PATTERN - Menu para acessar e interagir com um curso """

    # Prepara o contexto
    curso: Course | None = escolher_curso(cursos)

    if curso is None:
        return None

    context = {
        'course': curso,
        'console': console,
        'user': usuario
    }

    # Cria o gerenciador de menu
    menu = MenuManager(
        console,
        f":books: Acessando Curso [bold]{curso.titulo}[/] :books:"
    )

    # Adiciona as estratégias na ordem desejada e roda o menu
    menu.add_strategy(UpdateInfoStrategy()) \
        .add_strategy(ViewContentStrategy()) \
        .add_strategy(CoursePlatformStrategy()) \
        .add_strategy(AddContentStrategy()) \
        .add_strategy(RemoveContentStrategy()) \
        .add_strategy(ReportStrategy()) \
        .add_strategy(PerformanceStrategy()) \
        .add_strategy(AddPostCourseStrategy()) \
        .add_strategy(ExitStrategy()) \
        .run(context)

    None
