from abc import ABC, abstractmethod


class Course:
    def __init__(self, titulo, descricao, instrutor, conteudos=None, students=None, preco=0.0):
        self.titulo = titulo
        self.descricao = descricao
        self.instrutor = instrutor
        self.conteudos = conteudos if conteudos is not None else []
        self.students = students if students is not None else []
        # underline (convenção), indicando que é "privado"
        self._preco = preco #preco esta encapsulado

    @property #getter só retorna o valor
    def preco(self):
        return self._preco

    @preco.setter #setter controla o valor definto
    def preco(self, novo_preco):
        
        if novo_preco >= 0:
            self._preco = novo_preco
        else:
            print("Erro: O preço de um curso não pode ser negativo.")


# classe usuario criada para implementar herança
# assim, Student e Instructor herdam de Usuario
class Usuario(ABC): #abstract base class
    def __init__(self, nome, senha):
        self.nome = nome
        self.__senha = senha #senha está encapsulada

    @abstractmethod # método que deve ser implementado por subclasses
    def exibir_menu(self, cursos): # metodo abstrato
        pass


class Student(Usuario):
    def __init__(self, nome, senha, cursos_inscritos=None, cursos_pagos=None, progresso=None, notas_quizzes=None):
        super().__init__(nome, senha) #chama o init da classe usuario
        self.cursos_inscritos = cursos_inscritos if cursos_inscritos is not None else []
        self.progresso = progresso if progresso is not None else {}
        self.cursos_pagos = cursos_pagos if cursos_pagos is not None else []
        self.notas_quizzes = notas_quizzes if notas_quizzes is not None else {}

    def exibir_menu(self, cursos):
        from aluno.funcoes_aluno import menu_aluno # tive q usar assim pq tava dando erro circular :(
        menu_aluno(self, cursos)

class Instructor(Usuario):
    def __init__(self, nome, senha):
        super().__init__(nome, senha) #aqui tbm chama o init da classe usuario
        self.cursos = []
    
    def exibir_menu(self, cursos):
        from instrutor.funcoes_instrutor import menu_instrutor
        menu_instrutor(self, cursos)

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



