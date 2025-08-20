from models import Student, Course, Instructor
from data_base import alunos, cursos, instrutores
from aluno.funcoes_aluno import menu_aluno
from instrutor.funcoes_instrutor import menu_instrutor


def inicial():

    print("\n\nBem-vindo a plataforma E-learning!\n\n")
    # Menu principal
    print("--- Menu Principal ---")
    print("1 - Entrar como Aluno")
    print("2 - Entrar como Instrutor")
    print("3 - Sair")
    choose = int(input("Escolha uma opção: "))

    while choose not in [1, 2, 3]:
        print("Opção inválida. Tente novamente.")
        choose = int(input())

    # condições para ir para o menu do aluno ou do instrutor
    if (choose == 1):
        # logica para o aluno
        print("\nAlunos disponíveis:", [aluno.nome for aluno in alunos])
        nome_aluno = input("Digite o nome do aluno para 'logar': ")

        aluno_logado = None
        for aluno in alunos:
            if aluno.nome == nome_aluno or aluno.nome.lower() == nome_aluno.lower():
                aluno_logado = aluno
                break

        if aluno_logado:
            print(f"\nBem-vindo, {aluno_logado.nome}!")
            menu_aluno(aluno_logado, cursos)
            inicial()
        else:
            print("Aluno não encontrado.")
            inicial()

    elif (choose == 2):
        # logica para o instrutor
        print("\nInstrutores disponíveis:", [
              instrutor.nome for instrutor in instrutores])
        nome_instrutor = input("Digite o nome do instrutor para 'logar': ")

        instrutor_logado = None
        for instrutor in instrutores:
            if instrutor.nome == nome_instrutor or instrutor.nome.lower() == nome_instrutor.lower():
                instrutor_logado = instrutor
                break

        if instrutor_logado:
            print(f"\nBem-vindo, {instrutor_logado.nome}!")
            menu_instrutor(instrutor_logado, cursos)
            inicial()
        else:
            print("Instrutor não encontrado.")
            inicial()

    # SAIR DO SISTEMA
    elif (choose == 3):
        print("Saindo do sistema. Até logo!")
        exit()

    # COMANDO NÃO ENCONTRADO
    else:
        print("Opção inválida. Tente novamente.")

        