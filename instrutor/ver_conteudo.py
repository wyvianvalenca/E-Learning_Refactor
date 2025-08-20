from models import Conteudo
from instrutor.dry import selecionar_curso_do_instrutor

'''
    função para ver todos os conteudos do curso
'''

def executar(instrutor, cursos):
    print("\n--- Ver Conteúdos de um Curso ---")

    curso_selecionado = selecionar_curso_do_instrutor(instrutor, cursos)

    # Se a função retornou um curso, mostramos os conteúdos dele
    if curso_selecionado:
        print(f"\nConteúdos do curso: '{curso_selecionado.titulo}'")
        if not curso_selecionado.conteudos:
            print("  - Este curso ainda não possui conteúdos.")
        else:
            for conteudo_obj in curso_selecionado.conteudos:
                print(f"  - {conteudo_obj.titulo} ({conteudo_obj.tipo}, {conteudo_obj.duracao_minutos} min)")