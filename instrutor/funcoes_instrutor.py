import questionary
from rich.panel import Panel

from inicial import console
from data_base import posts
from models import Course, Instructor

from instrutor.menu_manager import MenuManager
from instrutor import listar_cursos, criar_curso, excluir_curso
from instrutor.gerenciador_cursos import GerenciadorCurso
from instrutor.instructor_strategies import (
    ListCoursesStrategy,
    AddCourseStrategy,
    ManageCourseStrategy,
    DeleteCourseStrategy,
    AccessForumStrategy,
    ExitStrategy,
    cursos_instrutor
)
from aluno import forum

def menu_instrutor_strategy(instrutor: Instructor, cursos: list[Course]) -> None:
    # Cria o gerenciador de menu
    menu = MenuManager(
        console,
        f":man_teacher: Menu do Instrutor: {instrutor.nome} :man_teacher:"
    )

    # Adiciona as estratégias na ordem desejada
    menu.add_strategy(ListCoursesStrategy()) \
        .add_strategy(AddCourseStrategy()) \
        .add_strategy(ManageCourseStrategy()) \
        .add_strategy(DeleteCourseStrategy()) \
        .add_strategy(AccessForumStrategy()) \
        .add_strategy(ExitStrategy())

    # Prepara o contexto
    context = {
        'instructor': instrutor,
        'courses': cursos,
        'posts': posts
    }

    # Executa o menu
    menu.run(context)

def menu_instrutor(instrutor: Instructor, cursos: list[Course]) -> None:
    while True:
        # Menu do instrutor
        console.print(Panel.fit(
            f":man_teacher: Menu do Instrutor: {instrutor.nome} :man_teacher:", style="dark_cyan"))

        opcoes: list[str] = [
            "Listar Meus Cursos",
            "Criar Curso",
            "Gerenciar Curso",
            "Excluir Curso",
            "Ver Forum",
            "Sair"
        ]

        console.print()
        choose: str = questionary.select("Escolha uma opcao:",
                                         choices=opcoes).ask()
        console.print()

        if choose == opcoes[0]:
            listar_cursos.executar(instrutor, cursos)

        elif choose == opcoes[1]:
            criar_curso.executar(instrutor, cursos)

        elif choose == opcoes[2]:
            GerenciadorCurso(console).menu(cursos_instrutor(cursos, instrutor))

        elif choose == opcoes[3]:
            excluir_curso.executar(instrutor, cursos)

        elif choose == opcoes[4]:
            forum.mostrar_feed(posts, instrutor)

        # SAIR
        elif choose == opcoes[5]:
            print("Saindo do menu do instrutor. Até logo!")
            break
