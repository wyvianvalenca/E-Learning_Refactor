# instrutor/add_remove_conteudo.py

from models import Conteudo
from instrutor.dry import selecionar_curso_do_instrutor

"""
    permite que um instrutor adicione ou remova objetos Conteudo
    de um de seus cursos
"""
def executar(instrutor, cursos):
    print("\n--- Gerenciar Conteúdos de um Curso ---")

    curso_selecionado = selecionar_curso_do_instrutor(instrutor, cursos)

    if not curso_selecionado:
        return


    print(f"\nGerenciando o curso: '{curso_selecionado.titulo}'")
    if not curso_selecionado.conteudos:
        print("Este curso ainda não possui conteúdos.")
    else:
        print("Conteúdos atuais:")
        for conteudo_obj in curso_selecionado.conteudos:
            print(f"  - {conteudo_obj}")


    acao = input("\nVocê deseja 'adicionar' ou 'remover' um conteúdo? ").lower()


    if acao == 'adicionar':
        print("\n--- Adicionando Novo Conteúdo ---")
        novo_titulo = input("Digite o título do conteúdo: ")
        novo_tipo = input("Digite o tipo (ex: Video, PDF): ")
        try:
            nova_duracao = int(input("Digite a duração em minutos: "))
            novo_conteudo = Conteudo(novo_titulo, novo_tipo, nova_duracao)
            curso_selecionado.conteudos.append(novo_conteudo)
            print(f"\nConteúdo '{novo_conteudo.titulo}' adicionado com sucesso!")
        except:
            print("Erro: A duração deve ser um número inteiro.")

    elif acao == 'remover':
        if not curso_selecionado.conteudos:
            return 

        print("\nQual conteúdo você deseja remover?")
        for i, conteudo_obj in enumerate(curso_selecionado.conteudos):
            print(f"  {i+1} - {conteudo_obj.titulo}")

        try:
            escolha_remover_num = int(input("Digite o número do conteúdo a ser removido: "))
            conteudo_removido = curso_selecionado.conteudos.pop(escolha_remover_num - 1)
            print(f"\nConteúdo '{conteudo_removido.titulo}' removido com sucesso!")
        except:
            print("Opção de conteúdo inválida.")

    else:
        print("Ação inválida. Tente novamente.")