import questionary
from rich.panel import Panel

from models import Student, Course, Instructor
from data_base import alunos, cursos, instrutores, posts

from rich.console import Console

console = Console()


def inicial():

    console.print(
        Panel.fit(":laptop_computer: Bem-vind@ à plataforma E-learning! :book:", style="cyan"))

    # menu principal
    opcoes: list[str] = [
        "Entrar como Aluno",
        "Entrar como Instrutor",
        "Sair"]
    choose: str = questionary.select("Escolha uma opcao:",
                                     choices=opcoes).ask()

    usuario_logado = None
    tipo_usuario = ""

    # condições para ir para o menu do aluno ou do instrutor
    if (choose == opcoes[0]):
        # logica para o aluno
        print("\nAlunos disponíveis:", [aluno.nome for aluno in alunos])
        nome_usuario = input("Digite o nome do aluno para 'logar': ")
        lista_usuarios = alunos
        tipo_usuario = "Aluno"

    elif (choose == opcoes[1]):
        # logica para o instrutor
        print("\nInstrutores disponíveis:", [
              instrutor.nome for instrutor in instrutores])
        nome_usuario: str = questionary.text(
            "Digite o nome do instrutor para 'logar':").ask()
        lista_usuarios = instrutores
        tipo_usuario = "Instrutor"

    elif (choose == opcoes[2]):
        print("Saindo do sistema. Até logo!")
        exit()

    # encontrar usuario
    for usuario in lista_usuarios:
        if usuario.nome.lower() == nome_usuario.lower():
            usuario_logado = usuario
            break

    if usuario_logado:
        console.print(
            f"\n\nBem-vindo, {usuario_logado.nome}!\n", style="gray100 on light_sea_green")
        # aqui chamamos o polimorfismo
        usuario_logado.exibir_menu(cursos, posts)
        inicial()
    else:
        print(f"{tipo_usuario} não encontrado.")
        inicial()
