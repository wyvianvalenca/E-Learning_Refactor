"""
    mostra um relatório de desempenho do aluno.
"""
def executar(aluno_logado):
    
    print("\n--- Meu Desempenho ---")
    
    if not aluno_logado.cursos_inscritos:
        print("Você não está inscrito em nenhum curso.")
        return

    print("Deseja ver o relatório de qual curso?")
    for i, curso in enumerate(aluno_logado.cursos_inscritos):
        print(f"{i + 1} - {curso.titulo}")
    
    try:
        escolha = int(input("\nDigite o número do curso: "))
        curso = aluno_logado.cursos_inscritos[escolha - 1]
    except (ValueError, IndexError):
        print("Opção inválida.")
        return


    titulos_obrigatorios_do_curso = {c.titulo for c in curso.conteudos}
    total_conteudos_atuais = len(titulos_obrigatorios_do_curso)

    if curso.titulo in aluno_logado.progresso:
        titulos_vistos_pelo_aluno = set(aluno_logado.progresso[curso.titulo])
    else:
        titulos_vistos_pelo_aluno = set()
        
    # intersection: encontra os conteúdos que o aluno já viu e que ainda existem no curso
    # vistos_que_ainda_existem: conta quantos conteúdos o aluno já viu que ainda existem no curso
    vistos_que_ainda_existem = len(titulos_obrigatorios_do_curso.intersection(titulos_vistos_pelo_aluno))
    
    # verifica com issubset dnv
    # issubset verifica se todos os conteúdos obrigatórios foram vistos pelo aluno
    # ele verifica da seguinte forma: todos os itens do primeiro conjunto (conteúdos do curso)
    # estão presentes no segundo conjunto (conteúdos vistos pelo aluno)
    curso_completo = titulos_obrigatorios_do_curso.issubset(titulos_vistos_pelo_aluno)
    progresso_percent = (vistos_que_ainda_existem / total_conteudos_atuais) * 100 if total_conteudos_atuais > 0 else 0

    
    print("\n" + "="*45)
    print(f"  RELATÓRIO DE DESEMPENHO: {curso.titulo.upper()}")
    print("="*45)
    print(f"Progresso Geral: {vistos_que_ainda_existem} de {total_conteudos_atuais} conteúdos concluídos.")
    print(f"Porcentagem: {progresso_percent:.1f}%")

    if curso.titulo in aluno_logado.notas_quizzes:
        nota = aluno_logado.notas_quizzes[curso.titulo]
        print(f"Nota no Quiz: {nota[0]} de {nota[1]} acertos.")
    
    if curso_completo:
        print("Status: Concluído!")
    else:
        print("Status: Em andamento")
    print("="*45)
    input("\nPressione Enter para voltar...")