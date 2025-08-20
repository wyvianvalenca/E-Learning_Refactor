
class Course:
    def __init__(self, titulo, descricao, instrutor, conteudos=None, students=None, preco=0.0):
        self.titulo = titulo
        self.descricao = descricao
        self.instrutor = instrutor
        self.conteudos = conteudos if conteudos is not None else []
        self.students = students if students is not None else []
        self.preco = preco  



class Student:
    def __init__(self, nome, senha, cursos_inscritos=None, cursos_pagos=None, progresso=None, notas_quizzes=None):
        self.nome = nome
        self.senha = senha
        self.cursos_inscritos = cursos_inscritos if cursos_inscritos is not None else []
        self.progresso = progresso if progresso is not None else {}
        self.cursos_pagos = cursos_pagos if cursos_pagos is not None else []
        self.notas_quizzes = notas_quizzes if notas_quizzes is not None else {}


class Instructor:
    def __init__(self, nome, senha):
        self.nome = nome
        self.senha = senha
        self.cursos = []

class Conteudo:
    def __init__(self, titulo, tipo, duracao_minutos, quiz_obj=None):
        self.titulo = titulo
        self.tipo = tipo  # 'video' ou 'PDF'
        self.duracao_minutos = duracao_minutos
        self.quiz_obj = quiz_obj


    #representação:
    def __repr__(self):
        return f"[{self.tipo}] {self.titulo} ({self.duracao_minutos} min)"



#aqui é o quiz completo
class Quiz:
    
    def __init__(self, titulo, perguntas):
        self.titulo = titulo
        self.perguntas = perguntas 

    def __repr__(self):
        return f"[Quiz] {self.titulo} ({len(self.perguntas)} perguntas)"



#aqui vai ficas as perguntas do quiz
class PerguntaQuiz:
    def __init__(self, pergunta, alternativas, indiceResposta):
        self.pergunta = pergunta
        self.alternativas = alternativas
        self.indiceResposta = indiceResposta
    
    def __repr__(self):
        return f"[PerguntaQuiz] {self.pergunta} - {self.alternativas})"



