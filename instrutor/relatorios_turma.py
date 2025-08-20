from instrutor.dry import selecionar_curso_do_instrutor

"""
    mostra um relatório geral de engajamento da turma em um curso
"""
def executar(instrutor, cursos):
    
    print("\n--- Relatórios da Turma ---")
    curso = selecionar_curso_do_instrutor(instrutor, cursos)

    if not curso:
        return

    total_alunos = len(curso.students)
    if total_alunos == 0:
        print("\nAinda não há alunos inscritos neste curso para gerar um relatório.")
        return

    total_concluintes = 0
    soma_percentuais_progresso = 0

    titulos_obrigatorios_do_curso = {c.titulo for c in curso.conteudos}
    total_conteudos_curso = len(titulos_obrigatorios_do_curso)

    for aluno in curso.students:
        if curso.titulo in aluno.progresso:
            titulos_vistos_pelo_aluno = set(aluno.progresso[curso.titulo])
        else:
            titulos_vistos_pelo_aluno = set()
            
        # issubset verifica se todos os conteúdos foram vistos pelo aluno
        # ele verifica da seguinte forma: todos os itens do primeiro conjunto (conteúdos do curso)
        # estão presentes no segundo conjunto (conteúdos vistos pelo aluno)
        aluno_concluiu = titulos_obrigatorios_do_curso.issubset(titulos_vistos_pelo_aluno)
        
        if aluno_concluiu:
            total_concluintes += 1
            percentual_aluno = 100.0
        else:
            vistos_que_ainda_existem = len(titulos_obrigatorios_do_curso.intersection(titulos_vistos_pelo_aluno))
            percentual_aluno = (vistos_que_ainda_existem / total_conteudos_curso) * 100 if total_conteudos_curso > 0 else 0
        
        soma_percentuais_progresso += percentual_aluno
            
    progresso_medio_turma = soma_percentuais_progresso / total_alunos if total_alunos > 0 else 0
    print("\n" + "="*45)
    print(f"  RELATÓRIO DO CURSO: {curso.titulo.upper()}")
    print("="*45)
    print(f"Total de Alunos Inscritos: {total_alunos}")
    print(f"Progresso Médio da Turma: {progresso_medio_turma:.1f}%")
    print(f"Alunos que Concluíram o Curso: {total_concluintes} ({ (total_concluintes/total_alunos)*100:.1f}%)")
    print("="*45)
    input("\nPressione Enter para voltar...")