from aluno import plataforma_do_curso




"""
    função para exibir o menu da plataforma de cursos para o aluno.
"""
def executar(aluno_logado, cursos):
    
    print("\n--- Plataforma de Cursos ---")
    print("1 - Visualizar Conteúdo dos Cursos Inscritos")
    print("2 - Sair")

    escolha = int(input("Escolha uma opção: "))
    while True:
        if escolha == 1:
            print("Você quer entrar na plataforma de qual curso?")
            for i, curso in enumerate(aluno_logado.cursos_inscritos):
                print(f"{i + 1} - {curso.titulo}")
                total_cursos = i
            print(f"{total_cursos + 2} - Voltar ao menu principal")

            choose = int(input("Digite o número: "))
            if choose == total_cursos + 2:
                print("Voltando ao menu principal...")
                return

            if(0 < choose ) and (choose <= total_cursos + 1):
                curso_escolhido = aluno_logado.cursos_inscritos[int(choose) - 1]
                print(f"Você escolheu o curso: {curso_escolhido.titulo}")
                plataforma_do_curso.executar(aluno_logado, curso_escolhido)

            else:
                print("Opção inválida. Por favor, digite um número válido.")
                executar(aluno_logado, cursos)
            
            
        elif escolha == 2:
            print("Saindo da plataforma de cursos. Até logo!")
            break
        else:
            print("Opção inválida. Tente novamente.")