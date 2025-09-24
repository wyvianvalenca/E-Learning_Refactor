import questionary
from aluno import forum
from data_base import alunos, cursos, instrutores, posts
from models import Course, Student, Instructor, Conteudo, Usuario
from instrutor import listar_cursos, criar_curso, atualizar_curso, excluir_curso, add_remove_conteudo, ver_conteudo, criar_quiz, relatorios_turma


def menu_instrutor(instrutor: Instructor, cursos: list[Course]) -> None:

    while True:
        # Menu do instrutor
        print(f"\n--- Menu do Instrutor: {instrutor.nome} ---")

        opcoes: list[str] = [
            "1 - Listar Meus Cursos",
            "2 - Criar Curso",
            "3 - Atualizar informações Curso",
            "4 - Excluir Curso",
            "5 - Ver conteúdos do curso",
            "6 - Adicionar/Remover conteúdos do curso",
            "7 - Chat e Fórum",
            "8 - Criar Quiz/Tarefa",
            "9 - Relatórios da Turma",
            "10 - Ver Forum",
            "0 - Sair"]

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

        elif choose == 5:
            ver_conteudo.executar(instrutor, cursos)

        elif choose == 6:
            add_remove_conteudo.executar(instrutor, cursos)

        elif choose == 7:
            print("Chat e Fórum")

        elif choose == 8:
            criar_quiz.executar(instrutor, cursos)

        elif choose == 9:
            relatorios_turma.executar(instrutor, cursos)

        elif choose == 10:
            forum.mostrar_feed(posts, instrutor)

        # SAIR
        elif choose == 0:
            print("Saindo do menu do instrutor. Até logo!")
            break
