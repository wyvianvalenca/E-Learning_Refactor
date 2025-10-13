from inicial import console
from data_base import posts
from instrutor.course_builder import CourseBuilder
from models.models import (
    Course,
    Student,
    Instructor,
    Comentario,
    ForumPost,
    Externo,
    Questionario,
    Quiz,
    PerguntaQuiz
)


def dados_iniciais(listaAlunos, listaInstrutores, listaCursos):

    # ALUNOS
    lucas = Student("Lucas", "coxinha123")
    larissa = Student("Larissa", "bolacha456")
    maria = Student("Maria", "pudim456")
    listaAlunos.extend([lucas, larissa, maria])

    # INSTRUTORES
    carlos = Instructor("Carlos", "prof123")
    laura = Instructor("Laura", "ensino456")
    listaInstrutores.extend([carlos, laura])

    # Quiz
    perguntas_py = [
        PerguntaQuiz("O que é Python?", [
                     "Linguagem de programação", "Fruta", "Animal"],
                     "Linguagem de programação"),
        PerguntaQuiz("Qual a extensão de arquivos Python?",
                     [".py", ".txt", ".docx"],
                     ".py")
    ]
    perguntas_ds = [
        PerguntaQuiz("O que é Data Science?", [
                     "Análise de dados", "Programação", "Design"],
                     "Análise de dados"),
        PerguntaQuiz("Qual biblioteca é usada para análise de dados em Python?",
                     ["Pandas", "NumPy", "Matplotlib"],
                     "Pandas")
    ]
    perguntas_ml = [
        PerguntaQuiz("O que é Machine Learning?",
                     ["Aprendizado de máquina", "Programação", "Banco de dados"],
                     "Aprendizado de máquina"),
        PerguntaQuiz("Qual algoritmo é usado em Machine Learning?",
                     ["Regressão Linear", "HTML", "CSS"],
                     "Regressão Linear")
    ]
    perguntas_django = [
        PerguntaQuiz("O que é Django?",
                     ["Framework web", "Banco de dados", "Sistema operacional"],
                     "Framework web"),
        PerguntaQuiz("Qual linguagem é usada no Django?",
                     ["Python", "JavaScript", "Java"],
                     "Python")
    ]

    # Criando objetos Quiz
    quiz1 = Quiz("Quiz Python", perguntas_py)
    quiz2 = Quiz("Quiz Data Science", perguntas_ds)
    quiz3 = Quiz("Quiz Machine Learning", perguntas_ml)
    quiz4 = Quiz("Quiz Django", perguntas_django)

    quiz_py = Questionario(
        console, "Quiz Python", "Quiz", 5, quiz=quiz1)
    quiz_ds = Questionario(
        console, "Quiz Data Science", "Quiz", 5, quiz=quiz2)
    quiz_ml = Questionario(
        console, "Quiz Machine Learning", "Quiz", 5, quiz=quiz3)
    quiz_django = Questionario(
        console, "Quiz Django", "Quiz", 5, quiz=quiz4)

    # CONTÉUDOS
    conteudos_py = [
        Externo(console, "Sobre Python", "PDF", 10, "content\\pdf.pdf"),
        Externo(console, "Introdução ao Python",
                "video", 30, "content\\videoo.mp4"),
        quiz_py
    ]
    conteudos_ds = [
        Externo(console, "Introdução ao Data Science",
                "PDF", 15, "content\\pdf.pdf"),
        Externo(console, "Análise de Dados",
                "video", 45, "content\\videoo.mp4"),
        quiz_ds
    ]
    conteudos_ml = [
        Externo(console, "Fundamentos de Machine Learning",
                "PDF", 20, "content\\pdf.pdf"),
        Externo(console, "Algoritmos de Machine Learning",
                "video", 50, "content\\videoo.mp4"),
        quiz_ml
    ]
    conteudos_web = [
        Externo(console, "Introdução ao Django",
                "PDF", 25, "content\\pdf.pdf"),
        Externo(console, "Criando APIs com Django",
                "video", 60, "content\\videoo.mp4"),
        quiz_django
    ]

    # CURSOS
    curso1 = Course("Python Basico", "Curso introdutório de Python",
                    carlos, conteudos_py, [lucas, larissa], 100.0, [], '', [])
    curso2 = Course("Data Science", "Curso de Data Science com Python",
                    laura, conteudos_ds, [larissa, maria], 150.0, [], '', [])
    curso3 = Course("Machine Learning", "Curso de Machine Learning com Python",
                    carlos, conteudos_ml, [lucas, maria], 200.0, [], '', [])
    curso4_com_builder: Course = CourseBuilder() \
        .with_name("Desenvolvimento Web") \
        .with_descricao("Curso de desenvolvimento web com Django") \
        .with_instrutor(laura) \
        .with_conteudos(conteudos_web) \
        .with_students([larissa]) \
        .with_preco(250.0) \
        .with_forum([ForumPost("Preciso de ajuda com o interpretador!", "ajude-me!", larissa)]) \
        .build()

    listaCursos.extend([curso1, curso2, curso3, curso4_com_builder])

    for curso in listaCursos:
        for aluno in curso.students:
            if curso not in aluno.cursos_inscritos:
                aluno.cursos_inscritos.append(curso)

    # FORUMS
    p1 = ForumPost("Codigo Python nao roda!",
                   "Meu programa em python nao esta rodando",
                   lucas)
    p2 = ForumPost("Nao entendi encapsulamento",
                   "Alguem pode me explicar?",
                   larissa)
    posts.extend([p1, p2])

    # COMENTARIOS
    c1 = Comentario(p1, "Posso te ajudar, manda uma msg", carlos)
    p1.comentarios.append(c1)
