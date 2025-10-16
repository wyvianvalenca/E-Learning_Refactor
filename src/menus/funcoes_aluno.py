import questionary
from rich.panel import Panel

from src.inicial import console
from src.models.models import Student, Course, ForumPost
from src.functions.student_functions import (
    adicionar_post,
    inscrever_curso,
    ver_cursos,
    plataformas_cursos,
    desempenho_aluno
)
from src.menus import forum


def menu_aluno(aluno_logado: Student, cursos: list[Course], posts: list[ForumPost]):
    while True:

        console.print(Panel.fit(
            f":pencil: Menu do Aluno: {aluno_logado.nome} :pencil:", style="light_sea_green"))

        opcoes: list[str] = [
            "Ver Cursos Inscritos",
            "Inscrever em Curso",
            "Plataforma Cursos",
            "Desempenho do Aluno",
            "Ver Forum",
            "Adicionar Post",
            "Sair"
        ]

        choose: str = questionary.select("Escolha uma opcao:",
                                         choices=opcoes).ask()

        # VER CURSOS INSCRITOS
        if choose == opcoes[0]:
            ver_cursos.ver_cursos(aluno_logado)

        # MATRICULAR EM CURSO
        elif choose == opcoes[1]:
            inscrever_curso.executar(aluno_logado, cursos)

        elif choose == opcoes[2]:
            plataformas_cursos.executar(aluno_logado, cursos)

        elif choose == opcoes[3]:
            desempenho_aluno.executar(aluno_logado)

        elif choose == opcoes[4]:
            forum.mostrar_feed(posts, aluno_logado)

        elif choose == opcoes[5]:
            adicionar_post.adicionar_post(aluno_logado, posts)

        elif choose == opcoes[6]:
            print("Saindo do menu do aluno. Até logo!")
            break

        else:
            print("Opção inválida. Tente novamente.")
