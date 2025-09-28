import questionary
from rich.panel import Panel

from inicial import console
from data_base import posts

from models import Course, Instructor

from instrutor import listar_cursos, criar_curso, excluir_curso
from instrutor.gerenciador_cursos import GerenciadorCurso

from aluno import forum


def menu_instrutor(instrutor: Instructor, cursos: list[Course]) -> None:
    cursos_instrutor: list[Course] = [
        curso for curso in cursos if curso.instrutor == instrutor
    ]

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
            GerenciadorCurso(console).menu(cursos_instrutor)

        elif choose == opcoes[3]:
            excluir_curso.executar(instrutor, cursos)

        elif choose == opcoes[4]:
            forum.mostrar_feed(posts, instrutor)

        # SAIR
        elif choose == opcoes[5]:
            print("Saindo do menu do instrutor. Até logo!")
            break
