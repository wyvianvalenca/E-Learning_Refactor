from models import Course, Student, Instructor, Conteudo, PerguntaQuiz, Quiz
from data_base import alunos, cursos, instrutores


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
        PerguntaQuiz("O que é Python?", ["Linguagem de programação", "Fruta", "Animal"], 0),
        PerguntaQuiz("Qual a extensão de arquivos Python?", [".py", ".txt", ".docx"], 0)
    ]
    perguntas_ds = [
        PerguntaQuiz("O que é Data Science?", ["Análise de dados", "Programação", "Design"], 0),
        PerguntaQuiz("Qual biblioteca é usada para análise de dados em Python?", ["Pandas", "NumPy", "Matplotlib"], 0)
    ]
    perguntas_ml = [
        PerguntaQuiz("O que é Machine Learning?", ["Aprendizado de máquina", "Programação", "Banco de dados"], 0),
        PerguntaQuiz("Qual algoritmo é usado em Machine Learning?", ["Regressão Linear", "HTML", "CSS"], 0)
    ]
    perguntas_django = [
        PerguntaQuiz("O que é Django?", ["Framework web", "Banco de dados", "Sistema operacional"], 0),
        PerguntaQuiz("Qual linguagem é usada no Django?", ["Python", "JavaScript", "Java"], 0)
    ]

    # Criando objetos Quiz
    quiz1 = Quiz("Quiz Python", perguntas_py)
    quiz2 = Quiz("Quiz Data Science", perguntas_ds)
    quiz3 = Quiz("Quiz Machine Learning", perguntas_ml)
    quiz4 = Quiz("Quiz Django", perguntas_django)

    quiz_py = Conteudo("Quiz Python", "Quiz", 5, quiz_obj=quiz1)
    quiz_ds = Conteudo("Quiz Data Science", "Quiz", 5, quiz_obj=quiz2)
    quiz_ml = Conteudo("Quiz Machine Learning", "Quiz", 5, quiz_obj=quiz3)
    quiz_django = Conteudo("Quiz Django", "Quiz", 5, quiz_obj=quiz4)


    #CONTÉUDOS
    conteudos_py = [
        Conteudo("PDF - Sobre Python", "PDF", 10),
        Conteudo("video - Introdução ao Python", "video", 30),
        quiz_py
    ]
    conteudos_ds = [
        Conteudo("PDF - Introdução ao Data Science", "PDF", 15),
        Conteudo("video - Análise de Dados", "video", 45),
        quiz_ds
    ]
    conteudos_ml = [
        Conteudo("PDF - Fundamentos de Machine Learning", "PDF", 20),
        Conteudo("video - Algoritmos de Machine Learning", "video", 50),
        quiz_ml
    ]
    conteudos_web = [
        Conteudo("PDF - Introdução ao Django", "PDF", 25),
        Conteudo("video - Criando APIs com Django", "video", 60),
        quiz_django
    ]




    #CURSOS
    curso1 = Course("Python Basico", "Curso introdutório de Python", carlos, conteudos_py, [lucas, larissa], preco=100.0)
    curso2 = Course("Data Science", "Curso de Data Science com Python", laura, conteudos_ds, [larissa, maria], preco=150.0)
    curso3 = Course("Machine Learning", "Curso de Machine Learning com Python", carlos, conteudos_ml, [lucas, maria], preco=200.0)
    curso4 = Course("Desenvolvimento Web", "Curso de desenvolvimento web com Django", laura, conteudos_web, [larissa], preco=250.0)
    listaCursos.extend([curso1, curso2, curso3, curso4])

    for curso in listaCursos:
        for aluno in curso.students:
            if curso not in aluno.cursos_inscritos:
                aluno.cursos_inscritos.append(curso)


   