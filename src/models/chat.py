from typing_extensions import override
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.models.user import Usuario, Student, Instructor


class Mensagem:
    """Classe que representa uma mensagem em um chat"""
    
    def __init__(self, autor: 'Usuario', conteudo: str):
        self.autor: 'Usuario' = autor
        self.conteudo: str = conteudo

    @override
    def __str__(self) -> str:
        return f"[bold][{self.autor.nome}][/] {self.conteudo}"


class Chat:
    """Classe que representa um chat entre dois usuários"""
    
    def __init__(self, user1: 'Usuario', user2: 'Student' | 'Instructor'):
        self.user1: 'Usuario' = user1
        self.user2: 'Usuario' = user2
        self.mensagens: list[Mensagem] = []

    @override
    def __str__(self) -> str:
        return f"Chat entre {self.user1.nome} e {self.user2.nome}"
