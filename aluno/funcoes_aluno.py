from models import Student, Course, Instructor, Conteudo, Usuario, ForumPost
from aluno import adicionar_post, inscrever_curso, ver_cursos, plataformas_cursos, desempenho_aluno, forum


def menu_aluno(aluno_logado: Student, cursos: Course, posts: list[ForumPost]):
    while True:
        print("\n--- Menu do Aluno ---")
        print("1 - Ver Cursos Inscritos")
        print("2 - Inscrever em Curso")
        print("3 - Plataforma Cursos")
        print("4 - Desempenho do Aluno")
        print("5 - Ver Forum")
        print("6 - Adicionar Post")
        print("0 - Sair")

        choose = int(input("Escolha uma opção: "))

        while choose not in [0, 1, 2, 3, 4, 5, 6]:
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

        elif choose == 5:
            forum.mostrar_feed(posts, aluno_logado)

        elif choose == 6:
            adicionar_post.adicionar_post(aluno_logado, posts)

        elif choose == 0:
            print("Saindo do menu do aluno. Até logo!")
            break

        else:
            print("Opção inválida. Tente novamente.")
