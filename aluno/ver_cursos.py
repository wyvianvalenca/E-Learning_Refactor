
'''
    função que permite a um aluno ver os cursos nos quais está inscrito
'''

def ver_cursos(aluno_logado):
    if aluno_logado.cursos_inscritos:
        print("\nCursos Inscritos:")
        for i,curso in enumerate(aluno_logado.cursos_inscritos):
            print(f"{i+1}- {curso.titulo}")
    else:
        print("Você não está inscrito em nenhum curso.")