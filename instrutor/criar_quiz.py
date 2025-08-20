from models import PerguntaQuiz, Conteudo, Quiz
from instrutor.dry import selecionar_curso_do_instrutor


"""
    permite que um instrutor crie quiz
"""
def executar(instrutor, cursos):
    print("\n------ CRIAR NOVO QUIZ ------")

    curso_selecionado = selecionar_curso_do_instrutor(instrutor, cursos)

    if not curso_selecionado:
        return

    print(f"\nCriando quiz para o curso: '{curso_selecionado.titulo}'")
    
    perguntas_do_quiz = []
    while True:
        enunciado = input("\nDigite o enunciado da pergunta: ")
        alternativas = input("Digite as opções separadas por vírgula: ").split(',')
        opcoes = [opt.strip() for opt in alternativas]
        
        try:
            resposta_idx = int(input(f"Digite o número da resposta correta (1 a {len(opcoes)}): ")) - 1
            if not (0 <= resposta_idx < len(opcoes)):
                print("Índice de resposta inválido. Tente novamente.")
                continue
        except:
            print("Entrada inválida. Digite um número.")
            continue
            
        nova_pergunta = PerguntaQuiz(enunciado, opcoes, resposta_idx)
        perguntas_do_quiz.append(nova_pergunta)

        continuar = input("Deseja adicionar mais perguntas? (s/n): ").lower()
        if continuar != 's':
            break


    if not perguntas_do_quiz:
        print("Nenhuma pergunta foi criada. Quiz cancelado.")
        return

    titulo_quiz = "Quiz sobre " + curso_selecionado.titulo
    novo_quiz_obj = Quiz(titulo_quiz, perguntas_do_quiz)

    conteudo_quiz = Conteudo(titulo_quiz, "Quiz", duracao_minutos=5, quiz_obj=novo_quiz_obj)
    curso_selecionado.conteudos.append(conteudo_quiz)

    print(f"\nQuiz '{novo_quiz_obj.titulo}' adicionado com sucesso ao curso '{curso_selecionado.titulo}'!")