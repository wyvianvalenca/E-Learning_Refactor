from __future__ import annotations

from typing_extensions import override
from abc import ABC, abstractmethod

from src.models import (
    Course,
    ForumPost,
    Chat
)


class Usuario(ABC):  # abstract base class
    """Classe base abstrata para usuários do sistema"""

    def __init__(self, nome: str, senha: str):
        self.nome: str = nome
        self.__senha: str = senha  # senha está encapsulada
        self.chats: dict[str, 'Chat'] = {}

    @abstractmethod  # método que deve ser implementado por subclasses
    def exibir_menu(self, cursos: list['Course'], posts: list['ForumPost']) -> None:
        pass


class Student(Usuario):
    """Classe que representa um estudante"""

    def __init__(self, nome: str, senha: str):
        super().__init__(nome, senha)  # chama o init da classe usuario
        self.cursos_inscritos: list['Course'] = []
        self.progresso: dict[str, list[str]] = {}
        self.cursos_pagos: list['Course'] = []
        self.posts: list['ForumPost'] = []

    @override
    def exibir_menu(self, cursos: list['Course'], posts: list['ForumPost']) -> None:
        from src.menus.student_menu import student_menu
        student_menu(self, cursos, posts)


class Instructor(Usuario):
    """Classe que representa um instrutor"""

    def __init__(self, nome: str, senha: str):
        super().__init__(nome, senha)  # aqui tbm chama o init da classe usuario
        self.cursos: list['Course'] = []

    @override
    def exibir_menu(self, cursos: list['Course'], posts: list['ForumPost']) -> None:
        from src.menus.instructor_menu import instructor_menu
        instructor_menu(self, cursos)
