from rich.panel import Panel

from models import Student, Course, Instructor
from data_base import alunos, cursos, instrutores, posts


def inicial():

    print(Panel("\n\nBem-vindo a plataforma E-learning!\n\n"))
    # menu principal
    print("--- Menu Principal ---")
    print("1 - Entrar como Aluno")
    print("2 - Entrar como Instrutor")
    print("3 - Sair")
    choose = int(input("Escolha uma opção: "))

    while choose not in [1, 2, 3]:
        print("Opção inválida. Tente novamente.")
        choose = int(input())

    usuario_logado = None
    tipo_usuario = ""

    # condições para ir para o menu do aluno ou do instrutor
    if (choose == 1):
        # logica para o aluno
        print("\nAlunos disponíveis:", [aluno.nome for aluno in alunos])
        nome_usuario = input("Digite o nome do aluno para 'logar': ")
        lista_usuarios = alunos
        tipo_usuario = "Aluno"

    elif (choose == 2):
        # logica para o instrutor
        print("\nInstrutores disponíveis:", [
              instrutor.nome for instrutor in instrutores])
        nome_usuario = input("Digite o nome do instrutor para 'logar': ")
        lista_usuarios = instrutores
        tipo_usuario = "Instrutor"

    elif (choose == 3):
        print("Saindo do sistema. Até logo!")
        exit()

    for usuario in lista_usuarios:
        if usuario.nome.lower() == nome_usuario.lower():
            usuario_logado = usuario
            break

    if usuario_logado:
        print(f"\nBem-vindo, {usuario_logado.nome}!")
        # aqui chamamos o polimorfismo
        usuario_logado.exibir_menu(cursos, posts)
        inicial()
    else:
        print(f"{tipo_usuario} não encontrado.")
        inicial()
