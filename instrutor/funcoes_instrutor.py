from data_base import alunos, cursos, instrutores
from models import Course, Student, Instructor, Conteudo
from instrutor import listar_cursos, criar_curso, atualizar_curso, excluir_curso, add_remove_conteudo, ver_conteudo, criar_quiz, relatorios_turma




def menu_instrutor(instrutor, cursos):

    while True:
        # Menu do instrutor
        print(f"\n--- Menu do Instrutor: {instrutor.nome} ---")
        print("1 - Listar Meus Cursos")
        print("2 - Criar Curso")
        print("3 - Atualizar informações Curso")
        print("4 - Excluir Curso")
        print("5 - Ver conteúdos do curso")
        print("6 - Adicionar/Remover conteúdos do curso")
        print("7 - Chat e Fórum")
        print("8 - Criar Quiz/Tarefa")
        print("9 - Relatórios da Turma")
        print("0 - Sair")

        choose = int(input("Escolha uma opção: "))

        while choose not in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]:
            print("Opção inválida. Tente novamente.")
            choose = int(input())

        # 
        if choose == 1:
            listar_cursos.executar(instrutor, cursos)
        elif choose == 2:
            criar_curso.executar(instrutor, cursos)
        elif choose == 3:
            atualizar_curso.executar(instrutor, cursos)
        elif choose == 4:
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

        # SAIR
        elif choose == 0:
            print("Saindo do menu do instrutor. Até logo!")
            break
