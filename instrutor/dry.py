
'''
    dry - don't repeat yourself
    aqui retornamos o obj do curso selecionado
'''

def selecionar_curso_do_instrutor(instrutor, cursos):
    cursos_do_instrutor = [curso for curso in cursos if curso.instrutor == instrutor]

    if not cursos_do_instrutor:
        print("\nVocê ainda não criou nenhum curso.")
        return None

    print("\nDisponível nos seus cursos:")
    for i, curso in enumerate(cursos_do_instrutor):
        print(f"{i + 1} - {curso.titulo}")
    
    try:
        escolha_num = int(input("Digite o número do curso: "))
        if 1 <= escolha_num <= len(cursos_do_instrutor):
            return cursos_do_instrutor[escolha_num - 1]
        else:
            print("Número fora do intervalo.")
            return None
    except:
        print("Entrada inválida. Digite um número.")
        return None