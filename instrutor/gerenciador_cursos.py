from typing import Callable
import questionary

from rich.console import Console
from rich.panel import Panel

from singleton_metaclass import SingletonMeta

from models.models import Course, Conteudo
from instrutor.gerenciador_conteudo import (
    GerenciadorConteudo,
    GerenciadorExterno,
    GerenciadorTexto,
    GerenciadorQuestionario
)


class GerenciadorCurso(metaclass=SingletonMeta):
    @staticmethod
    def escolher_curso(cursos_instrutor: list[Course]) -> None | Course:
        nomes_cursos: list[str] = [c.titulo for c in cursos_instrutor]
        escolhido: str = questionary.select("Selecione o curso que deseja gerenciar:",
                                            choices=nomes_cursos).ask()

        for curso in cursos_instrutor:
            if curso.titulo == escolhido:
                return curso

        return None

    @staticmethod
    def nada() -> None:
        return None

    def retornar(self) -> None:
        self.console.print()
        _ = questionary.press_any_key_to_continue(
            "Pressione qualquer tecla para retornar...").ask()
        return None

    def __init__(self, console: Console):
        self.console: Console = console
        self.trocar_curso: bool = True
        self.__curso: Course
        self.__gerenciador: GerenciadorConteudo

    def cabecalho(self, titulo: str) -> None:
        self.console.print()
        self.console.print(
            Panel.fit(f"--- {titulo} [bold]{self.__curso.titulo}[/] ---",
                      style="gray62"))
        self.console.print()

    def wip(self) -> None:
        self.cabecalho("Work In Progress")
        self.console.print("\nEstamos trabalhando nesse...\n")
        return self.retornar()

    def atualizar_infos(self) -> None:
        self.cabecalho("Atualizar o Curso")

        novo_nome: str = questionary.text(
            "Digite o novo nome (ou <Enter> para manter):").ask()

        if novo_nome:
            self.__curso.titulo = novo_nome

        nova_desc: str = questionary.text(
            "Digite a nova descrição (ou <Enter> para manter):").ask()

        if nova_desc:
            self.__curso.descricao = nova_desc

        return self.retornar()

    def ver_conteudos(self) -> None:
        self.cabecalho("Conteúdos do Curso")

        conteudos = self.__curso.conteudos
        exibir: str = ""
        if conteudos:
            for cont in conteudos:
                exibir += (f"  > {cont}\n")
            self.console.print(exibir)
        else:
            self.console.print("  > Este curso ainda não possui conteúdos.")

        return self.retornar()

    def adicionar_conteudo(self) -> None:
        self.cabecalho("Adicionar Conteúdo ao Curso")

        tipo: str = questionary.select(
            "Selecione o tipo do conteudo que deseja adicionar:",
            choices=['Vídeo', 'PDF', 'PowerPoint', 'Texto', 'Quiz']).ask()
        self.console.print()

        if tipo in ['Vídeo', 'PDF', 'PowerPoint']:
            self.__gerenciador = GerenciadorExterno(self.console, tipo)

        elif tipo == 'Texto':
            self.__gerenciador = GerenciadorTexto(self.console, tipo)

        elif tipo == 'Quiz':
            self.__gerenciador = GerenciadorQuestionario(self.console, tipo)

        else:
            self.console.print("\nTipo inválido.\n")
            return None

        self.__gerenciador.adicionar(self.__curso)

        return self.retornar()

    def remvover_conteudo(self) -> None:
        self.cabecalho("Remover Conteúdo do Curso")

        nomes: list[str] = [f"{id} - {item}" for id,
                            item in enumerate(self.__curso.conteudos)]
        remover: str = questionary.select(
            "Selecione o conteúdo que deseja remover:",
            choices=nomes).ask()
        index_remover: int = int(remover.split('-')[0].strip())

        removido: Conteudo = self.__curso.conteudos.pop(index_remover)

        self.console.print(f"Conteudo {removido.titulo} removido.")

        return self.retornar()

    def relatorios(self) -> None:
        self.cabecalho("Relatórios da Turma")

        total_alunos = len(self.__curso.students)
        if total_alunos == 0:
            print("\nAinda não há alunos inscritos neste curso para gerar um relatório.")
            return

        total_concluintes = 0
        soma_percentuais_progresso = 0

        titulos_obrigatorios_do_curso = {
            c.titulo for c in self.__curso.conteudos}
        total_conteudos_curso = len(titulos_obrigatorios_do_curso)

        for aluno in self.__curso.students:
            if self.__curso.titulo in aluno.progresso:
                titulos_vistos_pelo_aluno = set(
                    aluno.progresso[self.__curso.titulo])
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

        progresso_medio_turma = soma_percentuais_progresso / \
            total_alunos if total_alunos > 0 else 0
        print("\n" + "="*45)
        print(f"  RELATÓRIO DO CURSO: {self.__curso.titulo.upper()}")
        print("="*45)
        print(f"Total de Alunos Inscritos: {total_alunos}")
        print(f"Progresso Médio da Turma: {progresso_medio_turma:.1f}%")
        print(f"Alunos que Concluíram o Curso: {total_concluintes} ({
              (total_concluintes/total_alunos)*100:.1f}%)")
        print("="*45)

        self.retornar()

    def menu(self, cursos_instrutor: list[Course]) -> None:
        if self.trocar_curso:
            curso_escolhido: Course | None = self.escolher_curso(
                cursos_instrutor)
            if curso_escolhido:
                self.__curso = curso_escolhido
                self.trocar_curso = False
            else:
                raise ValueError

        # Tipagem do dicionario de opcoes:
        # Chave: opcao que vai aparecer na tela (tipo str)
        # Valor: funcao correspondente a ser chamada
        #       (tipo Callable com qualquer args e nenhum retorno)
        opcoes: dict[str, Callable[..., None]] = {
            "Atualizar Informações": self.atualizar_infos,
            "Ver Conteúdos": self.ver_conteudos,
            "Adicionar Conteúdo": self.adicionar_conteudo,
            "Remover Conteúdo": self.remvover_conteudo,
            "Relatório da Turma": self.relatorios,
            "Retonar para o menu anterior": self.nada,
        }

        while self.__curso:
            self.console.print()
            self.console.print(
                Panel.fit("===> Gerenciador de Cursos <===", style="light_sea_green"))
            self.console.print()

            self.console.print(
                f"Gerenciando o curso [gray0 on light_sea_green]{self.__curso.titulo}[/]...\n")

            acao: str = questionary.select("O que deseja fazer?",
                                           choices=list(opcoes.keys())).ask()

            if acao == "Retonar para o menu anterior":
                self.trocar_curso = True
                return None

            opcoes[acao]()
