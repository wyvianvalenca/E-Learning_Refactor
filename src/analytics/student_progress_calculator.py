from typing import NamedTuple

from src.models import Student, Course
from src.singleton_metaclass import SingletonMeta


class ProgressMetrics(NamedTuple):
    """ Metricas de progresso de um aluno em determinado cursoo """

    contents: int
    consumed_contents: int
    consumed_contents_set: set[str]
    is_completed: bool
    completion_percent: float


class StudentProgressCalculator(metaclass=SingletonMeta):
    """ SUBSSISTEMA INTERNO - Calcula as metricas de progresso de um aluno em um curso """

    @staticmethod
    def compute(student: Student, course: Course) -> ProgressMetrics:

        current_titles_set: set[str] = {
            content.titulo for content in course.conteudos}
        current_titles: int = len(current_titles_set)

        consumed_titles_set: set[str]
        if course.titulo in student.progresso:
            consumed_titles_set = set(student.progresso[course.titulo])
        else:
            consumed_titles_set = set()

        # intersection: encontra os conteúdos que o aluno já viu e que ainda existem no curso
        current_consumed: int = len(
            current_titles_set.intersection(consumed_titles_set))

        # issubset verifica se todos os conteúdos atuais estao no conjunto de conteudos vistos pelo aluno
        is_completed: bool = current_titles_set.issubset(consumed_titles_set)

        # calcula o progresso do aluno (conteudos atuais consumidos / conteudos atuais)
        progress_percent = (current_consumed / current_titles) * \
            100 if current_titles > 0 else 0

        return ProgressMetrics(
            contents=current_titles,
            consumed_contents=current_consumed,
            consumed_contents_set=consumed_titles_set,
            is_completed=is_completed,
            completion_percent=progress_percent
        )
