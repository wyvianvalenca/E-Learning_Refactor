import questionary

from src.inicial import console
from src.models.models import ForumPost, Student, Draft, PostState, Published


def adicionar_post(aluno_logado: Student, posts: list[ForumPost]) -> None:
    titulo: str = questionary.text("Digite o titulo do post:").ask()
    conteudo: str = questionary.text(
        "Digite o conteudo:", multiline=True).ask()
    state: str = questionary.select(
        "Deseja publicar ou salvar como rascunho?",
        choices=["Salvar como rascunho", "Publicar"]
    ).ask()

    initial_state: PostState = Published() if state == "Publicar" else Draft()
    new_post: ForumPost = ForumPost(
        titulo=titulo,
        conteudo=conteudo,
        aluno=aluno_logado,
        state=initial_state
    )

    posts.append(new_post)
    aluno_logado.posts.append(new_post)
    console.print("\n[bold green][OK][/] Post criado.\n")
    return None
