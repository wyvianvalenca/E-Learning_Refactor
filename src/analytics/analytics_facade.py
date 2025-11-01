from rich.console import Console

from src.models import Course, Student
from src.singleton_metaclass import SingletonMeta

from src.analytics.course_analytics_calculator import (
    CourseAnalytics,
    CourseAnalyticsCalculator
)
from src.analytics.student_progress_calculator import (
    ProgressMetrics,
    StudentProgressCalculator
)
from src.analytics.report_generator import ReportGenerator


class AnalyticsFacade(metaclass=SingletonMeta):
    """ FACADE PATTERN - Fornce interface simples e unificada para calculo e apresentacao de metricas """

    def __init__(self, console: Console):
        self.console: Console = console
        self._student_calculator: StudentProgressCalculator = StudentProgressCalculator()
        self._course_calculator: CourseAnalyticsCalculator = CourseAnalyticsCalculator(
            self._student_calculator
        )
        self._report_generator: ReportGenerator = ReportGenerator(console)

    def student_performance(self, student: Student, course: Course) -> None:
        metrics: ProgressMetrics = self._student_calculator.compute(
            student, course)
        self._report_generator.student_report(course, metrics)

        return None

    def course_report(self, course: Course) -> None:
        metrics: CourseAnalytics = self._course_calculator.compute(course)
        self._report_generator.course_report(course, metrics)

        return None
