# TO-DO

## Funcionalidades
- [x] inserir novas informações do curso (nível e categorias) na visualização dos cursos
- [x] permitir edição e publicação de posts em rascunho (alunos)
- [x] implementar forum do curso para os alunos (visualizar e adicionar post)
- [x] implementar limpeza de tela ao voltar para o menu
- [ ] implementar chat
- [x] agrupar logica de calculo de progresso individual e de turma
- [x] implementar opções para a dificuldade de um curso (ao criar)
- [x] implementar opções para as categorias de um curso (ao criar)

## Padrões de Projeto
- [x] refatorar criacao de curso com builder
- [x] implementar strategy no menu dos alunos
- [x] implementar state no forum (open, closed, deleted)
- [x] implementar chain of responsability para criação de conteudos
- [x] implementar adapter
- [x] implementar decorator
- [x] implementar facade

## Tratamento de Excessões / Entradas do Usuário
- [x] ajustar comportamento no Ctrl+C (questionary retorna None, o que pode gerar erro na lógica do código)
- [x] validar tamanho do título dos cursos
- [x] validar tamanho da descrição dos cursos
- [x] validar tamanho do título dos posts
- [x] validar tamanho do conteúdo dos posts
- [x] validar tamanho dos comentários
