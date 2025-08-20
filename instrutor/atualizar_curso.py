from instrutor.dry import selecionar_curso_do_instrutor


"""
    permite que o instrutor edite o título e a descrição de um de seus cursos.
"""
def executar(instrutor, cursos):

    print("\n--- Atualizar Curso ---")

    curso_selecionado = selecionar_curso_do_instrutor(instrutor, cursos)

    if curso_selecionado:
        print(f"\nEditando o curso: {curso_selecionado.titulo}")
        novo_nome = input(f"Digite o novo nome (ou enter para manter): ")
        nova_descricao = input(f"Digite a nova descrição (ou enter para manter): ")

        if novo_nome:
            curso_selecionado.titulo = novo_nome
        if nova_descricao:
            curso_selecionado.descricao = nova_descricao
        
        print("\nCurso atualizado com sucesso!")