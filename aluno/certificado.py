import os
from datetime import datetime

"""
    emite o certificado do aluno
"""

def executar(curso_escolhido, aluno_logado):
    print(f"Emitindo certificado para o aluno {aluno_logado.nome} no curso {curso_escolhido.titulo}...")
    

    diretorio_certificados = "certificados"
    if not os.path.exists(diretorio_certificados):
        os.makedirs(diretorio_certificados)

    data_emissao = datetime.now().strftime("%d/%m/%Y às %H:%M")


    conteudo_certificado = f"""
    +-----------------------------------------------------------------+
    |                                                                 |
    |                         CERTIFICADO DE CONCLUSÃO                |
    |                                                                 |
    +-----------------------------------------------------------------+

    Certificamos que o(a) aluno(a):

        {aluno_logado.nome.upper()}

    concluiu com sucesso o curso:

        "{curso_escolhido.titulo.upper()}"

    ministrado pelo(a) instrutor(a) {curso_escolhido.instrutor.nome}.

    -------------------------------------------------------------------
    Certificado emitido em: {data_emissao}
    Plataforma E-Learning
    """

    nome_arquivo = f"Certificado_{aluno_logado.nome}_{curso_escolhido.titulo}.txt".replace(" ", "_")
    caminho_completo = os.path.join(diretorio_certificados, nome_arquivo)

    if os.access(diretorio_certificados, os.W_OK):
        with open(caminho_completo, 'w', encoding='utf-8') as arquivo:
            arquivo.write(conteudo_certificado)
        
        print("\n+---------------------------------------------------+")
        print(f"| Certificado emitido com sucesso! ✅               |")
        print(f"| Arquivo salvo em: {caminho_completo} |")
        print("+---------------------------------------------------+")

    else:
        # Se a verificação com IF falhou
        print(f"\nOcorreu um erro: Sem permissão para escrever na pasta '{diretorio_certificados}'.")
        print("Verifique as permissões da pasta ou execute o programa como administrador.")
