from typing import Any
from typing_extensions import override

import questionary
from rich.console import Console

from src.models import (
    Course,
    Conteudo,
    ForumPost,
    Instructor,
    Student
)
from src.menus.strategy_interface import MenuActionStrategy
from src.functions.instructor_functions import gerenciador_conteudo
from src.functions.student_functions import (
    adicionar_post,
    plataforma_do_curso
)
from src.functions import forum
from src.analytics import AnalyticsFacade
from src.validations import text_geq_50characters, text_has_2words


class UpdateInfoStrategy(MenuActionStrategy):
    """ STRATEGY PATTERN - Estratégia para atualizar informações de um curso """

    @override
    def get_label(self) -> str:
        return "Atualizar Informações"

    @override
    def can_execute(self, context) -> bool:
        return isinstance(context['user'], Instructor)

    @override
    def execute(self, context: dict[str, Any]) -> None:
        curso: Course = context['course']

        self.cabecalho(f"Atualizar informações do Curso [bold]{
                       curso.titulo}[/]")
        novo_nome: str = questionary.text(
            "Digite o novo nome (ou <Ctrl+C> para manter):",
            validate=text_has_2words
        ).ask()

        if novo_nome:
            curso.titulo = novo_nome

        nova_desc: str = questionary.text(
            "Digite a nova descrição (ou <Ctrl+C> para manter):",
            validate=text_geq_50characters
        ).ask()

        if nova_desc:
            curso.descricao = nova_desc

        return self.retornar()


class ViewContentStrategy(MenuActionStrategy):
    """ STRATEGY PATTERN - Estratégia para ver os conteúdos de um curso """

    @override
    def get_label(self) -> str:
        return "Ver Conteúdos"

    @override
    def can_execute(self, context: Any) -> bool:
        return len(context['course'].conteudos) > 0

    @override
    def execute(self, context: Any) -> None:
        curso: Course = context['course']

        self.cabecalho(f"Ver Conteúdos do Curso [bold]{curso.titulo}[/]")

        conteudos = curso.conteudos
        exibir: str = ""
        for cont in conteudos:
            exibir += f"  > {cont}\n"
        context['console'].print(exibir)

        return self.retornar()


class CoursePlatformStrategy(MenuActionStrategy):
    """ STRATEGY PATTERN - Estratégia para acessar a plataforma de um curso """

    @override
    def get_label(self) -> str:
        return "Plataforma do Curso"

    @override
    def can_execute(self, context: Any) -> bool:
        return (isinstance(context['user'], Student) and
                (len(context['course'].conteudos) > 0))

    @override
    def execute(self, context: dict[str, Any]) -> None:
        student: Student = context['user']
        course: Course = context['course']

        self.cabecalho(f"Plataforma do Curso [bold]{course.titulo}[/]")

        plataforma_do_curso.executar(student, course)

        return None


class AddContentStrategy(MenuActionStrategy):
    """ STRATEGY PATTERN - Estratégia para adicionar conteúdo a um curso """

    @override
    def get_label(self) -> str:
        return "Adicionar Conteudo"

    @override
    def can_execute(self, context: Any) -> bool:
        return isinstance(context['user'], Instructor)

    @override
    def execute(self, context: dict[str, Any]) -> None:
        curso: Course = context['course']
        console: Console = context['console']

        self.cabecalho(f"Adicionar Conteúdo ao Curso [bold]{curso.titulo}[/]")
        tipo: str = questionary.select(
            "Selecione o tipo do conteudo que deseja adicionar:",
            choices=['Vídeo', 'PDF', 'PowerPoint', 'Texto', 'Quiz']).ask()
        console.print()

        if tipo in ['Vídeo', 'PDF', 'PowerPoint']:
            gerenciador_conteudo.GerenciadorExterno(
                console, tipo).adicionar(curso)

        elif tipo == 'Texto':
            gerenciador_conteudo.GerenciadorTexto(
                console, tipo).adicionar(curso)

        elif tipo == 'Quiz':
            gerenciador_conteudo.GerenciadorQuestionario(
                console, tipo).adicionar(curso)

        else:
            console.print("\nTipo inválido.\n")
            return None

        return self.retornar()


class RemoveContentStrategy(MenuActionStrategy):
    """ STRATEGY PATTERN - Estratégia para remover conteúdo de um curso """

    @override
    def get_label(self) -> str:
        return "Remover Conteúdo"

    @override
    def can_execute(self, context: Any) -> bool:
        return ((isinstance(context['user'], Instructor)) and
                (len(context['course'].conteudos) > 0))

    @override
    def execute(self, context: Any) -> None:
        curso: Course = context['course']

        self.cabecalho(f"Remover Conteúdo do Curso [bold]{curso.titulo}[/]")

        nomes: list[str] = [f"{id} - {item}" for id,
                            item in enumerate(curso.conteudos)]
        remover: str = questionary.select(
            "Selecione o conteúdo que deseja remover:",
            choices=nomes).ask()

        if remover is None:
            context['console'].print("Operação cancelada pelo usuário")
            return MenuActionStrategy.retornar()

        index_remover: int = int(remover.split('-')[0].strip())

        removido: Conteudo = curso.conteudos.pop(index_remover)

        context['console'].print(f"Conteúdo {removido.titulo} removido.")

        return self.retornar()


class PerformanceStrategy(MenuActionStrategy):
    """ STRATEGY PATTERN - Estratégia para ver o desempenho de um aluno em um curso """

    @override
    def get_label(self) -> str:
        return "Desempenho do Aluno"

    @override
    def can_execute(self, context: Any) -> bool:
        return ((isinstance(context['user'], Student)) and
                (len(context['course'].conteudos) > 0))

    @override
    def execute(self, context: Any) -> None:
        student: Student = context['user']
        course: Course = context['course']
        console: Console = context['console']

        self.cabecalho(f"Desempenho de {student.nome} no Curso [bold]{
                       course.titulo}[/]")

        AnalyticsFacade(console).student_performance(student, course)

        return self.retornar()


class ReportStrategy(MenuActionStrategy):
    """ STRATEGY PATTERN - Estratégia para ver os relatórios da turma de um curso """

    @override
    def get_label(self) -> str:
        return "Relatórios da Turma"

    @override
    def can_execute(self, context: Any) -> bool:
        return ((isinstance(context['user'], Instructor)) and
                (len(context['course'].students) > 0))

    @override
    def execute(self, context: Any) -> None:
        course: Course = context['course']
        console: Console = context['console']

        AnalyticsFacade(console).course_report(course)

        return self.retornar()


class AddPostCourseStrategy(MenuActionStrategy):
    """ STRATEGY PATTERN - Estratégia para criar um post no forum do curso """

    @override
    def get_label(self) -> str:
        return "Criar Post no Forum do Curso"

    @override
    def can_execute(self, context) -> bool:
        return (isinstance(context['user'], Student))

    @override
    def execute(self, context: Any) -> None:
        curso: Course = context['course']
        usuario: Student = context['user']
        curso_forum: list[ForumPost] = context['course'].forum

        self.cabecalho(f"Adicionar Post no Forum do Curso [bold]{
                       curso.titulo}[/]")

        adicionar_post.adicionar_post(usuario, curso_forum)

        return None


class CourseForumStrategy(MenuActionStrategy):
    """ STRATEGY PATTERN - Estratégia para ver o forum de um curso """

    @override
    def get_label(self) -> str:
        return "Ver Forum do Curso"

    @override
    def can_execute(self, context: Any) -> bool:
        return context['course'].forum is not None and len(context['course'].forum) > 0

    @override
    def execute(self, context: Any) -> None:
        curso: Course = context['course']
        curso_forum: list[ForumPost] = curso.forum

        self.cabecalho(f"Forum do Curso [bold]{curso.titulo}[/]")

        forum.mostrar_feed(curso_forum, context['user'], "published")

        return None
