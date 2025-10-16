from src.models.models import Course


def print_courses(courses: list[Course], show_students: bool) -> None:
    for c in courses:
        print(f"\n> {c.titulo.upper()}")

        if c.descricao:
            print(f"  Descrição: {c.descricao}")

        if c.nivel:
            print(f"  Nível: {c.nivel}")

        if c.categorias:
            print(f"  Categorias: {', '.join(c.categorias)}")

        if show_students:
            if c.students:
                nomes_alunos = [aluno.nome for aluno in c.students]
                print(f"  Alunos Inscritos: {nomes_alunos}")

            else:
                print("  Nenhum aluno inscrito.")

    return None
