import questionary

from src.inicial import console
from src.menus.strategy_interface import MenuActionStrategy
from src.models import ForumPost, Student, Draft, PostState, Published
from src.validations import text_geq_100characters, text_has_2words


def adicionar_post(aluno_logado: Student, posts: list[ForumPost]) -> None:
    titulo: str = questionary.text(
        "Digite o titulo do post:",
        validate=text_has_2words
    ).ask()

    conteudo: str = questionary.text(
        "Digite o conteudo:",
        multiline=True,
        validate=text_geq_100characters
    ).ask()

    state: str = questionary.select(
        "Deseja publicar ou salvar como rascunho?",
        choices=["Salvar como rascunho", "Publicar"]
    ).ask()

    if titulo is None or conteudo is None or state is None:
        console.print("\n Operação cancelada pelo usuário.")
        MenuActionStrategy.retornar()
        return None

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
