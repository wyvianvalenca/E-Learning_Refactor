
from typing_extensions import override


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
        self.chats: dict[str, 'Chat'] = {}


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
    
    @override
    def __repr__(self):
        return f"[PerguntaQuiz] {self.pergunta} - {self.alternativas})"

class Comentario:
    def __init__(self, pai: 'ForumPost', conteudo: str, autor: Student | Instructor):
        self.pai: 'ForumPost' = pai
        self.conteudo: str = conteudo
        self.autor: Student | Instructor = autor

    @override
    def __str__(self) -> str:
        return f"{self.autor.nome}\n > {self.conteudo}"

class ForumPost:
    def __init__(self, titulo: str, conteudo: str, aluno: Student):
        self.titulo: str = titulo
        self.conteudo: str = conteudo
        self.aluno: Student = aluno
        self.comentarios: list['Comentario'] = []

    def header(self) -> str:
        return f"> {self.titulo.upper()} por {self.aluno.nome}"

class Mensagem:
    def __init__(self, autor: Student | Instructor, conteudo: str):
        self.autor: Student | Instructor = autor
        self.conteudo: str = conteudo

    @override
    def __str__(self) -> str:
        return f"[bold][{self.autor.nome}][/] {self.conteudo}"

class Chat:
    def __init__(self, user1: Student | Instructor, user2: Student | Instructor):
        self.user1: Student | Instructor = user1
        self.user2: Student | Instructor = user2
        self.mensagens: list[Mensagem] = []

    def __str__(self) -> str:
        return f"Chat entre {self.user1.nome} e {self.user2.nome}"
