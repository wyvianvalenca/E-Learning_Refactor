import questionary
from rich.panel import Panel

from inicial import console

from data_base import alunos, cursos, instrutores, posts

from models import Course, Student, Instructor, Conteudo, Usuario

from instrutor import listar_cursos, criar_curso, atualizar_curso, excluir_curso, add_remove_conteudo, ver_conteudo, criar_quiz, relatorios_turma
from aluno import forum


def menu_instrutor(instrutor: Instructor, cursos: list[Course]) -> None:

    while True:
        # Menu do instrutor
        console.print(Panel.fit(
            f":man_teacher: Menu do Instrutor: {instrutor.nome} :man_teacher:", style="light_sea_green"))

        opcoes: list[str] = [
            "Listar Meus Cursos",
            "Criar Curso",
            "Atualizar informações Curso",
            "Excluir Curso",
            "Ver conteúdos do curso",
            "Adicionar/Remover conteúdos do curso",
            "Criar Quiz/Tarefa",
            "Relatórios da Turma",
            "Ver Forum",
            "Sair"
        ]

        choose: str = questionary.select("Escolha uma opcao:",
                                         choices=opcoes).ask()

        if choose == opcoes[0]:
            listar_cursos.executar(instrutor, cursos)

        elif choose == opcoes[1]:
            criar_curso.executar(instrutor, cursos)

        elif choose == opcoes[2]:
            atualizar_curso.executar(instrutor, cursos)

        elif choose == opcoes[3]:
            excluir_curso.executar(instrutor, cursos)

        elif choose == opcoes[4]:
            ver_conteudo.executar(instrutor, cursos)

        elif choose == opcoes[5]:
            add_remove_conteudo.executar(instrutor, cursos)

        elif choose == opcoes[6]:
            criar_quiz.executar(instrutor, cursos)

        elif choose == opcoes[7]:
            relatorios_turma.executar(instrutor, cursos)

        elif choose == opcoes[8]:
            forum.mostrar_feed(posts, instrutor)

        # SAIR
        elif choose == opcoes[9]:
            print("Saindo do menu do instrutor. Até logo!")
            break
