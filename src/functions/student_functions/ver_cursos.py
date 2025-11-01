
'''
    função que permite a um aluno ver os cursos nos quais está inscrito
'''

from src.models import Student
from src.print_courses import print_courses


def ver_cursos(aluno_logado: Student) -> None:
    if aluno_logado.cursos_inscritos:
        print("\nCursos Inscritos:")
        print_courses(aluno_logado.cursos_inscritos, show_students=False)
    else:
        print("Você não está inscrito em nenhum curso.")
