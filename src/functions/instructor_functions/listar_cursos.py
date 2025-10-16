# instrutor/listar_cursos.py


"""
    lista todos os cursos criados pelo instrutor logado,
    juntamente com os alunos inscritos em cada um.
"""
from src.print_courses import print_courses


def executar(instrutor, cursos):

    #filtra da lista geral de cursos apenas os que pertencem a este instrutor.
    cursos_do_instrutor = [curso for curso in cursos if curso.instrutor == instrutor]

    if not cursos_do_instrutor:
        print("Você ainda não criou nenhum curso.")
        return

    print_courses(cursos_do_instrutor, show_students=True)