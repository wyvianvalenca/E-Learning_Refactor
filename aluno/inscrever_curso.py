from aluno.pagamento import pagamento
'''
    função para inscrever um aluno em um curso
'''

def executar(aluno_logado, cursos):

    print("\nCursos Disponíveis:")
    for curso in cursos:
        print(f"- {curso.titulo} (Instrutor: {curso.instrutor.nome})")

    titulo_curso = input("\nDigite o título do curso para se matricular: ")
    curso_encontrado = None

    for curso in cursos:
        if curso.titulo.lower() == titulo_curso.lower():
            curso_encontrado = curso
            break

    if curso_encontrado:

        if curso_encontrado in aluno_logado.cursos_inscritos:
            print("Você já está inscrito neste curso.")
        else:
            if pagamento(aluno_logado, curso_encontrado):
                print(f"Inscrevendo-se no curso '{curso_encontrado.titulo}'...")
                aluno_logado.cursos_inscritos.append(curso_encontrado)
                curso_encontrado.students.append(aluno_logado)
                print(f"Você se inscreveu no curso '{curso_encontrado.titulo}' com sucesso!")
    else: 
        print("Curso não encontrado.")