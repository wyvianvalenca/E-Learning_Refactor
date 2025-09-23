# main.py
from inicial import inicial
from data_base import alunos, instrutores, cursos
from dados_iniciais import dados_iniciais

from rich.console import Console

console = Console()


def main():
    dados_iniciais(alunos, instrutores, cursos)
    inicial()


if __name__ == "__main__":
    main()
