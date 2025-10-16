# instrutor/criar_curso.py
import questionary

from src.validations import is_non_empty, is_positive_number
from src.models.models import Course, Instructor
from src.functions.instructor_functions.course_builder import CourseBuilder

"""
    cria um novo objeto curso, associando ao instrutor.
"""


def executar(instructor: Instructor, all_courses_list: list[Course]) -> None:

    name: str = questionary.text("Digite o nome do novo curso:", qmark="->",
                                 validate=is_non_empty).ask()
    desc: str = questionary.text("Digite a descrição do curso:", qmark="->",
                                 validate=is_non_empty).ask()
    price: float = questionary.text("Digite o preço do curso (R$):", qmark="->",
                                    validate=is_positive_number).ask()
    difficulty: str = questionary.text(
        "Digite o nível de dificuldade do curso:", qmark="->").ask()
    categories: str = questionary.text(
        "Digite as categorias do curso (separadas por vírgula):", qmark="->").ask()
    categories_list = categories.split(",")

    new_course: Course = CourseBuilder() \
        .with_name(name) \
        .with_descricao(desc) \
        .with_instrutor(instructor) \
        .with_preco(price) \
        .with_nivel(difficulty) \
        .with_categorias(categories_list) \
        .build()
    all_courses_list.append(new_course)
    instructor.cursos.append(new_course)

    print(f"\nCurso '{name}' criado com sucesso!")
