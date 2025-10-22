import questionary

from src.inicial import console
from src.models.models import ForumPost, Instructor, Usuario


def nada(post: ForumPost, user: Usuario) -> None:
    return None


def wip(post: ForumPost, user: Usuario) -> None:
    console.print("Estamos trabalhando nisso...")
    return None


def comentar(post: ForumPost, user: Usuario) -> None:
    post.comment(user)

    return None


def mostrar_comentarios(post: ForumPost, user: Usuario) -> None:
    post.render_comments()

    return None


def editar_post(post: ForumPost, user: Usuario) -> None:
    if user != post.aluno:
        console.print("Não é possível editar um post de outro usuário.")
        return None

    post.edit()

    return None


def fechar_post(post: ForumPost, user: Usuario) -> None:
    if not isinstance(user, Instructor):
        console.print("Apenas instrutores podem fechar posts.")
        return None

    post.close()


def acoes_post(index: int, post: ForumPost, user: Usuario) -> int:
    actions = {
        "Proximo": nada,
        "Anterior": nada,
        "Comentar": comentar,
        "Ver Comentarios": mostrar_comentarios,
        "Editar Post": editar_post,
        "Fechar Post": fechar_post
    }

    console.print()
    option: str = questionary.select("Choose an option:",
                                     choices=list(actions.keys())).ask()

    actions[option](post, user)

    if option == "Proximo":
        return index + 1
    elif option == "Anterior":
        return index - 1 if index > 0 else 0
    else:
        return index


def mostrar_post(index: int, post: ForumPost, user: Usuario) -> int:
    post.render()

    return acoes_post(index, post, user)


def mostrar_feed(posts: list[ForumPost], user: Usuario) -> None:
    index: int = 0
    while index < len(posts):
        post: ForumPost = posts[index]

        index = mostrar_post(index, post, user)

    questionary.press_any_key_to_continue(
        "Pressione qualquer tecla para voltar ao menu.").ask()
    return None
