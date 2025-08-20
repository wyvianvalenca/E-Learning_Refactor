
import os
from aluno import certificado, responder_quiz


'''
    mostra o conteúdo do curso escolhido pelo aluno
'''

def executar(aluno_logado, curso_escolhido):
   
    if curso_escolhido.titulo not in aluno_logado.progresso:
        aluno_logado.progresso[curso_escolhido.titulo] = []

    while True:
        titulos_vistos_pelo_aluno = aluno_logado.progresso[curso_escolhido.titulo]
        titulos_obrigatorios_do_curso = {conteudo.titulo for conteudo in curso_escolhido.conteudos}
        curso_completo = titulos_obrigatorios_do_curso.issubset(set(titulos_vistos_pelo_aluno))
        
        total_conteudos = len(curso_escolhido.conteudos)

        print(f"\n--- Conteúdos do Curso: {curso_escolhido.titulo} ---")
        for i, conteudo in enumerate(curso_escolhido.conteudos):
            status = "✅ Visto" if conteudo.titulo in titulos_vistos_pelo_aluno else ""
            print(f"  {i + 1} - {conteudo} {status}")

        print("-" * 30)
        if curso_completo:
            print(f"{total_conteudos + 1} - Emitir Certificado")
        print("0 - Voltar")

        try:
            escolha = int(input("\nEscolha uma opção: "))
        except:
            print("Opção inválida.")
            continue

        if 1 <= escolha <= total_conteudos:
            conteudo_selecionado = curso_escolhido.conteudos[escolha - 1]
            if conteudo_selecionado.tipo == "video":
                os.startfile("video.mp4")
                if conteudo_selecionado.titulo not in titulos_vistos_pelo_aluno:
                    aluno_logado.progresso[curso_escolhido.titulo].append(conteudo_selecionado.titulo)

            elif conteudo_selecionado.tipo == "PDF":
                os.startfile("pdf.pdf")
                if conteudo_selecionado.titulo not in titulos_vistos_pelo_aluno:
                    aluno_logado.progresso[curso_escolhido.titulo].append(conteudo_selecionado.titulo)
                
            
            
            elif conteudo_selecionado.tipo.lower() == "quiz":
             
                quiz_passou = responder_quiz.executar(conteudo_selecionado)

                if quiz_passou and conteudo_selecionado.titulo not in titulos_vistos_pelo_aluno:
                    aluno_logado.progresso[curso_escolhido.titulo].append(conteudo_selecionado.titulo)
                else:
                    print("Progresso não salvo. Tente o quiz novamente para gabaritá-lo.")


        elif curso_completo and escolha == total_conteudos + 1:
            certificado.executar(curso_escolhido, aluno_logado)
            input("\nPressione Enter para continuar...")
        elif escolha == 0:
            break
        else:
            print("Opção inválida.")