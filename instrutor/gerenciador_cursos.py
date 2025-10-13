import questionary
from rich.console import Console

from models.models import Course, Conteudo
from menu_manager import MenuManager
from menu_strategies import ExitStrategy
from instrutor.course_management_strategies import (
    UpdateInfoStrategy,
    ViewContentStrategy,
    AddContentStrategy,
    RemoveContentStrategy,
    ReportStrategy
)


def escolher_curso(cursos_instrutor: list[Course]) -> None | Course:
    nomes_cursos: list[str] = [c.titulo for c in cursos_instrutor]
    escolhido: str = questionary.select("Selecione o curso que deseja gerenciar:",
                                        choices=nomes_cursos).ask()

    for curso in cursos_instrutor:
        if curso.titulo == escolhido:
            return curso

    return None


# STRATEGY MENU
def course_management_menu(console: Console, cursos: list[Course]) -> None:
    """Função para criar o menu do gerenciador de cursos"""

    # Prepara o contexto
    curso: Course = escolher_curso(cursos)
    context = {
        'course': curso,
        'console': console
    }

    # Cria o gerenciador de menu
    menu = MenuManager(
        console,
        f":books: Gerenciar Curso [bold]{curso.titulo}[/] :books:"
    )

    # Adiciona as estratégias na ordem desejada e roda o menu
    menu.add_strategy(UpdateInfoStrategy()) \
        .add_strategy(ViewContentStrategy()) \
        .add_strategy(AddContentStrategy()) \
        .add_strategy(RemoveContentStrategy()) \
        .add_strategy(ReportStrategy()) \
        .add_strategy(ExitStrategy()) \
        .run(context)