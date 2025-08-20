# instrutor/listar_cursos.py


"""
    lista todos os cursos criados pelo instrutor logado,
    juntamente com os alunos inscritos em cada um.
"""
def executar(instrutor, cursos):
    print("\n--- Meus Cursos Criados ---")

    #filtra da lista geral de cursos apenas os que pertencem a este instrutor.
    cursos_do_instrutor = [curso for curso in cursos if curso.instrutor == instrutor]

    if not cursos_do_instrutor:
        print("Você ainda não criou nenhum curso.")
        return

    for curso in cursos_do_instrutor:
        print(f"\n- Título: {curso.titulo}")
        print(f"  Descrição: {curso.descricao}")
        
        if curso.students:
            nomes_alunos = [aluno.nome for aluno in curso.students]
            print(f"  Alunos Inscritos: {nomes_alunos}")
        else:
            print("  Nenhum aluno inscrito.")