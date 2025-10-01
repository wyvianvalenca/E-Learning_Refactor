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
            "Relatório da Turma": self.wip,
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
