# Importações das classes de usuário
from .user import Usuario, Student, Instructor

# Importações das classes de curso
from .course import Course

# Importações das classes de quiz
from .quiz import PerguntaQuiz, Quiz

# Importações das classes de conteúdo
from .content import Conteudo, Externo, Texto, Questionario

# Importações das classes de fórum
from .forum import (
    ForumPost,
    PostState,
    Draft,
    Published,
    Closed,
    Comentario
)

# Importações das classes de chat
from .chat import Mensagem, Chat

__all__ = [
    # User classes
    'Usuario',
    'Student',
    'Instructor',
    # Course classes
    'Course',
    # Quiz classes
    'PerguntaQuiz',
    'Quiz',
    # Content classes
    'Conteudo',
    'Externo',
    'Texto',
    'Questionario',
    # Forum classes
    'ForumPost',
    'PostState',
    'Draft',
    'Published',
    'Closed',
    'Comentario',
    # Chat classes
    'Mensagem',
    'Chat',
]