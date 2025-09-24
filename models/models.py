from abc import ABC, abstractmethod


from typing_extensions import override


class Course:
    def __init__(self, titulo, descricao, instrutor, conteudos=None, students=None, preco=0.0):
        self.titulo: str = titulo
        self.descricao: str = descricao
        self.instrutor = instrutor
        self.conteudos = conteudos if conteudos is not None else []
        self.students = students if students is not None else []
        # underline (convenção), indicando que é "privado"
        self._preco = preco  # preco esta encapsulado

    @property  # getter só retorna o valor
    def preco(self):
        return self._preco

    @preco.setter  # setter controla o valor definto
    def preco(self, novo_preco):

        if novo_preco >= 0:
            self._preco = novo_preco
        else:
            print("Erro: O preço de um curso não pode ser negativo.")


# classe usuario criada para implementar herança
# assim, Student e Instructor herdam de Usuario
class Usuario(ABC):  # abstract base class
    def __init__(self, nome, senha):
        self.nome = nome
        self.__senha = senha  # senha está encapsulada

    @abstractmethod  # método que deve ser implementado por subclasses
    def exibir_menu(self, cursos: list[Course], posts: list['ForumPost']) -> None:
        pass


class Student(Usuario):
    def __init__(self, nome, senha, cursos_inscritos=None, cursos_pagos=None, progresso=None, notas_quizzes=None):
        super().__init__(nome, senha)  # chama o init da classe usuario
        self.cursos_inscritos: list[Course] = cursos_inscritos if cursos_inscritos is not None else [
        ]
        self.progresso = progresso if progresso is not None else {}
        self.cursos_pagos = cursos_pagos if cursos_pagos is not None else []
        self.notas_quizzes = notas_quizzes if notas_quizzes is not None else {}
        self.chats: dict[str, 'Chat'] = {}

    @override
    def exibir_menu(self, cursos: list[Course], posts: list['ForumPost']) -> None:
        # tive q usar assim pq tava dando erro circular :(
        from aluno.funcoes_aluno import menu_aluno
        menu_aluno(self, cursos, posts)


class Instructor(Usuario):
    def __init__(self, nome, senha):
        super().__init__(nome, senha)  # aqui tbm chama o init da classe usuario
        self.cursos = []

    @override
    def exibir_menu(self, cursos: list[Course], posts: list['ForumPost']) -> None:
        from instrutor.funcoes_instrutor import menu_instrutor
        menu_instrutor(self, cursos)


class Conteudo:
    def __init__(self, titulo, tipo, duracao_minutos, quiz_obj=None):
        self.titulo = titulo
        self.tipo = tipo  # 'video' ou 'PDF'
        self.duracao_minutos = duracao_minutos
        self.quiz_obj = quiz_obj

    # representação:

    def __repr__(self):
        return f"[{self.tipo}] {self.titulo} ({self.duracao_minutos} min)"


# aqui é o quiz completo
class Quiz:

    def __init__(self, titulo, perguntas):
        self.titulo = titulo
        self.perguntas = perguntas

    def __repr__(self):
        return f"[Quiz] {self.titulo} ({len(self.perguntas)} perguntas)"


# aqui vai ficas as perguntas do quiz
class PerguntaQuiz:
    def __init__(self, pergunta, alternativas, indiceResposta):
        self.pergunta = pergunta
        self.alternativas = alternativas
        self.indiceResposta = indiceResposta

    @override
    def __repr__(self):
        return f"[PerguntaQuiz] {self.pergunta} - {self.alternativas})"


class Comentario:
    def __init__(self, pai: 'ForumPost', conteudo: str, autor: Usuario):
        self.pai: 'ForumPost' = pai
        self.conteudo: str = conteudo
        self.autor: Usuario = autor

    @override
    def __str__(self) -> str:
        return f"{self.autor.nome}\n > {self.conteudo}"


class ForumPost:
    def __init__(self, titulo: str, conteudo: str, aluno: Student):
        self.titulo: str = titulo
        self.conteudo: str = conteudo
        self.aluno: Student = aluno
        self.comentarios: list[Comentario] = []

    def header(self) -> str:
        return f"> {self.titulo.upper()} por {self.aluno.nome}"


class Mensagem:
    def __init__(self, autor: Usuario, conteudo: str):
        self.autor: Usuario = autor
        self.conteudo: str = conteudo

    @override
    def __str__(self) -> str:
        return f"[bold][{self.autor.nome}][/] {self.conteudo}"


class Chat:
    def __init__(self, user1: Usuario, user2: Student | Instructor):
        self.user1: Usuario = user1
        self.user2: Usuario = user2
        self.mensagens: list[Mensagem] = []

    @override
    def __str__(self) -> str:
        return f"Chat entre {self.user1.nome} e {self.user2.nome}"
