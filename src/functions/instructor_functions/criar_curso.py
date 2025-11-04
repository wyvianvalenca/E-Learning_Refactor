# instrutor/criar_curso.py
import questionary

from src.validations import (
    is_positive_number,
    text_geq_50characters,
    text_has_2words
)
from src.models import Course, Instructor
from src.functions.instructor_functions.course_builder import CourseBuilder

"""
    cria um novo objeto curso, associando ao instrutor.
"""


def executar(instructor: Instructor, all_courses_list: list[Course]) -> None:

    name: str = questionary.text(
        "Digite o nome do novo curso:", qmark="->",
        validate=text_has_2words
    ).ask()

    desc: str = questionary.text(
        "Digite a descrição do curso:", qmark="->",
        validate=text_geq_50characters
    ).ask()

    price: str = questionary.text(
        "Digite o preço do curso (R$):", qmark="->",
        validate=is_positive_number
    ).ask()

    difficulty: str = questionary.select(
        "Selecione o nível de dificuldade do curso:", qmark="->",
        choices=["Iniciante", "Intermediário", "Avançado"]
    ).ask()

    categories_list: list[str] = questionary.checkbox(
        "Escolha as categorias do curso (separadas por vírgula):", qmark="->",
        choices=["Web", "Segurança", "IA",
                 "Desenvolvimento", "Software", "Qualidade"]
    ).ask()

    if (name is None or
            desc is None or
            price is None or
            difficulty is None or
            categories_list is None):
        print("Operação cancelada pelo usuário")
        return None

    new_course: Course = CourseBuilder() \
        .with_name(name) \
        .with_descricao(desc) \
        .with_instrutor(instructor) \
        .with_preco(float(price)) \
        .with_nivel(difficulty) \
        .with_categorias(categories_list) \
        .build()
    all_courses_list.append(new_course)
    instructor.cursos.append(new_course)

    print(f"\nCurso '{name}' criado com sucesso!")
