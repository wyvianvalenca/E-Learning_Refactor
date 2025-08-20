
"""
    executa um quiz para o alun
"""

def executar(conteudo_quiz):
    
    quiz_obj = conteudo_quiz.quiz_obj
    total_de_perguntas = len(quiz_obj.perguntas)
    corretas = 0

    print(f"\n--- Iniciando Quiz: {quiz_obj.titulo} ---")
    

    for i, pergunta_atual in enumerate(quiz_obj.perguntas):
        print(f"\nPergunta {i + 1}: {pergunta_atual.pergunta}")
        for j, alternativa_texto in enumerate(pergunta_atual.alternativas):
            print(f"  {j + 1} - {alternativa_texto}")
        
        try:
            resposta_usuario = int(input("Qual a sua resposta? "))
            if (resposta_usuario - 1) == pergunta_atual.indiceResposta:
                print("Resposta Correta!")
                corretas += 1
            else:
                resposta_certa_texto = pergunta_atual.alternativas[pergunta_atual.indiceResposta]
                print(f"Resposta Incorreta. A resposta certa era: '{resposta_certa_texto}'")
        except (ValueError, IndexError):
            print("Resposta inválida.")
    
    print("\n--- Resultado do Quiz ---")
    print(f"Você acertou {corretas} de {total_de_perguntas} perguntas.")


    return corretas == total_de_perguntas