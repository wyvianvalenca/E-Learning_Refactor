from typing import NamedTuple

from src.models import Course, Student
from src.singleton_metaclass import SingletonMeta

from src.analytics.student_progress_calculator import (
    ProgressMetrics,
    StudentProgressCalculator
)


class CourseAnalytics(NamedTuple):
    """ Metricas do progresso da turma """

    total_students: int
    completers: int
    completion_rate: float
    average_progress: float
    # student, progress percentage, course completion
    students_progress: list[tuple[Student, float, bool]]


class CourseAnalyticsCalculator(metaclass=SingletonMeta):
    """ SUBSSISTEMA INTERNO - Calcula as metricas de progresso da turma inteira """

    def __init__(self, progress_calculator: StudentProgressCalculator):
        self.progress_calculator: StudentProgressCalculator = progress_calculator

    def compute(self, course: Course) -> CourseAnalytics:
        students_list: list[Student] = course.students
        total_students: int = len(students_list)

        if total_students == 0:
            return CourseAnalytics(0, 0, 0.0, 0.0, [])

        completers: int = 0
        students_progress: list[tuple[Student, float, bool]] = []
        progress_sum: float = 0.0

        for student in students_list:
            metrics: ProgressMetrics = self.progress_calculator.compute(
                student, course
            )

            if metrics.is_completed:
                completers += 1

            students_progress.append((
                student,
                metrics.completion_percent,
                metrics.is_completed
            ))

            progress_sum += metrics.completion_percent

        completion_rate: float = (completers / total_students * 100)
        average_progress: float = progress_sum / total_students

        return CourseAnalytics(
            total_students=total_students,
            completers=completers,
            completion_rate=completion_rate,
            average_progress=average_progress,
            students_progress=students_progress
        )
