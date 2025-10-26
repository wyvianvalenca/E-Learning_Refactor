from typing import Any
from typing_extensions import override

import questionary
from rich.console import Console

from src.models.models import Course, Conteudo, ForumPost, Instructor, Student
from src.menus.strategy_interface import MenuActionStrategy
from src.functions.instructor_functions import (
    gerenciador_conteudo
)
from src.functions.student_functions import (
    # adicionar_post,
    desempenho_aluno,
    plataforma_do_curso
)
# from src.functions import forum


# CONCRETE COURSE MANAGEMENT STRATEGIES


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
            "Digite o novo nome (ou <Enter> para manter):").ask()

        if novo_nome:
            curso.titulo = novo_nome

        nova_desc: str = questionary.text(
            "Digite a nova descrição (ou <Enter> para manter):").ask()

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

        self.cabecalho(f"Desempenho de {student.nome} no Curso [bold]{
                       course.titulo}[/]")

        desempenho_aluno.executar(student, course)

        return None


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
        curso: Course = context['course']
        alunos_curso: list[Student] = curso.students
        total_alunos: int = len(alunos_curso)

        self.cabecalho(f"Relatórios da Turma [bold]{curso.titulo}[/]")

        total_concluintes = 0
        soma_percentuais_progresso = 0

        titulos_obrigatorios_do_curso = {c.titulo for c in curso.conteudos}
        total_conteudos_curso = len(titulos_obrigatorios_do_curso)

        for aluno in alunos_curso:
            if curso.titulo in aluno.progresso:
                titulos_vistos_pelo_aluno = set(aluno.progresso[curso.titulo])
            else:
                titulos_vistos_pelo_aluno = set()

            # issubset verifica se todos os conteúdos foram vistos pelo aluno
            # ele verifica da seguinte forma: todos os itens do primeiro conjunto (conteúdos do curso)
            # estão presentes no segundo conjunto (conteúdos vistos pelo aluno)
            aluno_concluiu = titulos_obrigatorios_do_curso.issubset(
                titulos_vistos_pelo_aluno)

            if aluno_concluiu:
                total_concluintes += 1
                percentual_aluno = 100.0
            else:
                vistos_que_ainda_existem = len(
                    titulos_obrigatorios_do_curso.intersection(titulos_vistos_pelo_aluno))
                percentual_aluno = (vistos_que_ainda_existem / total_conteudos_curso) * \
                    100 if total_conteudos_curso > 0 else 0

            soma_percentuais_progresso += percentual_aluno

        progresso_medio_turma = soma_percentuais_progresso / total_alunos

        print("\n" + "=" * 45)
        print(f"  RELATÓRIO DO CURSO: {curso.titulo.upper()}")
        print("=" * 45)
        print(f"Total de Alunos Inscritos: {total_alunos}")
        print(f"Progresso Médio da Turma: {progresso_medio_turma:.1f}%")
        print(f"Alunos que Concluíram o Curso: {total_concluintes} ({
              (total_concluintes / total_alunos) * 100:.1f}%)")
        print("=" * 45)

        self.retornar()


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


"""
class CourseForumStrategy(MenuActionStrategy):
     STRATEGY PATTERN - Estratégia para ver o forum de um curso 

    @override
    def get_label(self) -> str:
        return "Ver Forum do Curso"

    @override
    def can_execute(self, context: Any) -> bool:
        return context['course'].forum is not None and len(context['course'].forum) > 0

    @override
    def execute(self, context: Any) -> None:
        curso: Course = context['course']
        curso_forum: list[ForumPost] = context['course'].forum

        self.cabecalho(f"Forum do Curso [bold]{curso.titulo}[/]")

        forum.mostrar_feed(curso_forum, context['user'])

        return None
"""
