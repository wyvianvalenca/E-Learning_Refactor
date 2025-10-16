import questionary

from src.inicial import console
from src.models.models import ForumPost, Student


def adicionar_post(aluno_logado: Student, posts: list[ForumPost]) -> None:
    titulo: str = questionary.text("Digite o titulo do post:").ask()
    conteudo: str = questionary.text(
        "Digite o conteudo:", multiline=True).ask()

    posts.append(ForumPost(titulo, conteudo, aluno_logado))
    console.print("\n[bold green][OK][/] Post criado.\n")
    return None
