from __future__ import annotations

from src.models import (
    Instructor,
    Student,
    Conteudo,
    ForumPost
)


class Course:
    """Classe que representa um curso"""

    def __init__(self, titulo: str, descricao: str,
                 instrutor: 'Instructor',
                 conteudos: list['Conteudo'],
                 students: list['Student'],
                 preco: float,
                 forum: list['ForumPost'],
                 nivel: str,
                 categorias: list[str]):

        self.titulo: str = titulo
        self.descricao: str = descricao
        self.instrutor: 'Instructor' = instrutor
        self.conteudos: list['Conteudo'] = conteudos
        self.students: list['Student'] = students
        self.forum: list['ForumPost'] = forum
        self.nivel: str = nivel
        self.categorias: list[str] = categorias

        # underline (convenção), indicando que é "privado"
        self.__preco: float = preco  # preco esta encapsulado

    @property  # getter só retorna o valor
    def preco(self) -> float:
        return self.__preco

    @preco.setter  # setter controla o valor definto
    def preco(self, novo_preco: float):

        if novo_preco >= 0:
            self.__preco = novo_preco
        else:
            print("Erro: O preço de um curso não pode ser negativo.")
