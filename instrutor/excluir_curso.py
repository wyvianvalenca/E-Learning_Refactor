
from instrutor.dry import selecionar_curso_do_instrutor
"""
    permite que o instrutor exclua um de seus cursos da plataforma.
"""

def executar(instrutor, cursos):

    print("\n--- Excluir Curso ---")
    curso_para_excluir = selecionar_curso_do_instrutor(instrutor, cursos)

    if not curso_para_excluir:
        return

    try:
        confirmacao = input(f"Tem certeza que deseja excluir o curso '{curso_para_excluir.titulo}'? (s/n): ").lower()

        if confirmacao == 's':
            # Remove o curso da lista geral e da lista pessoal do instrutor
            cursos.remove(curso_para_excluir)
            instrutor.cursos.remove(curso_para_excluir)
            print("\nCurso excluído com sucesso!")
        else:
            print("\nExclusão cancelada.")

    except:
        print("Ocorreu um erro inesperado durante a exclusão")