from rich.console import Console

from src.analytics.course_analytics_calculator import CourseAnalytics
from src.models.course import Course
from src.singleton_metaclass import SingletonMeta

from src.analytics.student_progress_calculator import ProgressMetrics


class ReportGenerator(metaclass=SingletonMeta):
    """ SUBSSISTEMA INTERNO - Gera os relatorios de aluno e de turma """

    def __init__(self, console: Console):
        self.console: Console = console

    def student_report(self, course: Course, metrics: ProgressMetrics) -> None:

        self.console.print("\n" + "="*45)
        self.console.print(f">  RELATÓRIO DE DESEMPENHO: {
                           course.titulo.upper()}")
        self.console.print("="*45)
        self.console.print(f"Progresso Geral: {metrics.consumed_contents} de {
                           metrics.contents} conteúdos concluídos.")
        self.console.print(
            f"Porcentagem: {metrics.completion_percent:.1f}%")

        if metrics.is_completed:
            self.console.print("Status: [bold green]Concluído![/]")
        else:
            self.console.print("Status: [yellow]Em andamento[/]")

        print("="*45)

        return None

    def course_report(self, course: Course, metrics: CourseAnalytics) -> None:

        self.console.print("\n" + "=" * 45)
        self.console.print(f"  RELATÓRIO DO CURSO: {course.titulo.upper()}")
        self.console.print("=" * 45)

        self.console.print("Total de Alunos Inscritos: " +
                           f"{metrics.total_students}")

        self.console.print("Progresso Médio da Turma: " +
                           f"{metrics.average_progress:.1f}%")

        self.console.print("Alunos que Concluíram o Curso:" +
                           f"{metrics.completers} ({metrics.completion_rate:.1f}%)")

        self.console.print("=" * 45)

        return None
