from src.models.models import (
    Instructor,
    Conteudo,
    Student,
    Course,
    ForumPost
)


class CourseBuilder:
    """ BUILDER PATTERN - Builder para construção de Course com métodos fluentes """

    def __init__(self):
        self.__nome = None
        self.__descricao = None
        self.__instrutor = None
        self.__conteudos = None
        self.__students = None
        self.__preco = None
        self.__forum = None
        self.__nivel = None
        self.__categorias = None

    def with_name(self, name: str) -> 'CourseBuilder':
        self.__nome = name
        return self

    def with_descricao(self, descricao: str) -> 'CourseBuilder':
        self.__descricao = descricao
        return self

    def with_instrutor(self, instrutor: Instructor) -> 'CourseBuilder':
        self.__instrutor = instrutor
        return self

    def with_conteudos(self, conteudos: list[Conteudo]) -> 'CourseBuilder':
        self.__conteudos = conteudos
        return self

    def with_students(self, students: list[Student]) -> 'CourseBuilder':
        self.__students = students
        return self

    def with_preco(self, preco: float) -> 'CourseBuilder':
        self.__preco = preco
        return self

    def with_forum(self, forum: list[ForumPost]) -> 'CourseBuilder':
        self.__forum = forum
        return self

    def with_nivel(self, nivel: str) -> 'CourseBuilder':
        self.__nivel = nivel
        return self

    def with_categorias(self, categorias: list[str]) -> 'CourseBuilder':
        self.__categorias = categorias
        return self

    def build(self) -> 'Course':
        if self.__nome is None:
            raise Exception('Course must have a name')

        if self.__descricao is None:
            self.__descricao = ''

        if self.__instrutor is None:
            raise Exception('Course must have an instrutor')

        if self.__conteudos is None:
            self.__conteudos = []

        if self.__students is None:
            self.__students = []

        if self.__preco is None:
            raise Exception('Course must have a price')

        if self.__forum is None:
            self.__forum = []

        if self.__nivel is None:
            self.__nivel = ''

        if self.__categorias is None:
            self.__categorias = []

        return Course(
            self.__nome,
            self.__descricao,
            self.__instrutor,
            self.__conteudos,
            self.__students,
            self.__preco,
            self.__forum,
            self.__nivel,
            self.__categorias
        )
