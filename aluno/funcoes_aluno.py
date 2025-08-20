from models import Student, Course, Instructor, Conteudo
from data_base import alunos, cursos, instrutores
from aluno import inscrever_curso, ver_cursos, plataformas_cursos, desempenho_aluno


def menu_aluno(aluno_logado, cursos):
    while True:
        print("\n--- Menu do Aluno ---")
        print("1 - Ver Cursos Inscritos")
        print("2 - Inscrever em Curso")
        print("3 - Plataforma Cursos")
        print("4 - Desempenho do Aluno")
        print("0 - Sair")

        choose = int(input("Escolha uma opção: "))

        while choose not in [0, 1, 2, 3, 4]:
            print("Opção inválida. Tente novamente.")
            choose = int(input())

        # VER CURSOS INSCRITOS
        if choose == 1:
            ver_cursos.ver_cursos(aluno_logado)
        # MATRICULAR EM CURSO
        elif choose == 2:
            inscrever_curso.executar(aluno_logado, cursos)
        elif choose == 3:
            plataformas_cursos.executar(aluno_logado, cursos)
        elif choose == 4:
            desempenho_aluno.executar(aluno_logado)
        elif choose == 0:
            print("Saindo do menu do aluno. Até logo!")
            break

        else:
            print("Opção inválida. Tente novamente.")
