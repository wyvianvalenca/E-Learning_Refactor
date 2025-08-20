import time

'''
 pagamento de curso 
'''

def pagamento(aluno, curso):
    
    print("\n" + "="*20)
    print("        INSCRIÇÃO E PAGAMENTO")
    print("="*20)
    print(f"Curso: {curso.titulo}")
    print(f"Valor: R$ {curso.preco:.2f}")
    
    confirmacao = input("Deseja prosseguir para o pagamento? (s/n): ").lower()

    if confirmacao != 's':
        print("Inscrição cancelada.")
        return False

    print("\nPara pagar, acesse o link abaixo:")

    print("\nLink para pagamento: https://pagamento.exemplo/pix/A1B2C3D4\n")

    input("Pressione Enter após ter realizado o pagamento para confirmar...")

    print("\nProcessando pagamento...")
    time.sleep(3)
    
    print("Pagamento confirmado com sucesso!")
    aluno.cursos_pagos.append(curso)
    return True