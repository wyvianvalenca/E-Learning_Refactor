# main.py
from src.inicial import inicial
from src.data_base import alunos, instrutores, cursos
from src.dados_iniciais import dados_iniciais


def main():
    dados_iniciais(alunos, instrutores, cursos)
    inicial()


if __name__ == "__main__":
    main()
