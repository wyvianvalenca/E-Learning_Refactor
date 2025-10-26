import questionary

from src.inicial import console
from src.models.models import ForumPost, Instructor, Usuario


def nada(post: ForumPost, user: Usuario) -> None:
    return None


def comentar(post: ForumPost, user: Usuario) -> None:
    post.comment(user)

    return None


def mostrar_comentarios(post: ForumPost, user: Usuario) -> None:
    post.render_comments()

    return None


def editar_post(post: ForumPost, user: Usuario) -> None:
    if user != post.aluno:
        console.print("\nNão é possível editar um post de outro usuário.")
        return None

    post.edit()

    return None


def publicar_post(post: ForumPost, user: Usuario) -> None:
    post.publish()

    return None


def fechar_post(post: ForumPost, user: Usuario) -> None:
    if not isinstance(user, Instructor):
        console.print("\nApenas instrutores podem fechar posts.")
        return None

    post.close()

    return None


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

    if actions[option] != nada:
        console.print()
        questionary.press_any_key_to_continue(
            "Pressione qualquer tecla para voltar ao feed."
        ).ask()
        console.print()

    if option == "Proximo":
        return index + 1
    elif option == "Anterior":
        return index - 1 if index > 0 else 0
    else:
        return index


def mostrar_post(index: int, post: ForumPost, user: Usuario) -> int:
    # Nao exibe rascunhos, pula para o proximo post
    if post.state == "draft":
        return index + 1

    post.render()

    return acoes_post(index, post, user)


def draft_actions(index: int, post: ForumPost, user: Usuario) -> int:
    actions = {
        "Proximo": nada,
        "Anterior": nada,
        "Editar Post": editar_post,
        "Publicar Post": publicar_post
    }

    console.print()
    option: str = questionary.select("Choose an option:",
                                     choices=list(actions.keys())).ask()

    actions[option](post, user)

    if actions[option] != nada:
        console.print()
        questionary.press_any_key_to_continue(
            "Pressione qualquer tecla para voltar ao feed."
        ).ask()
        console.print()

    if option == "Proximo":
        return index + 1
    elif option == "Anterior":
        return index - 1 if index > 0 else 0
    else:
        return index


def render_drafts(index: int, post: ForumPost, user: Usuario) -> int:
    post.render_draft()

    return draft_actions(index, post, user)


def mostrar_feed(posts: list[ForumPost], user: Usuario, type: str) -> None:
    index: int = 0
    while index < len(posts):
        post: ForumPost = posts[index]

        if type == "forum":
            index = mostrar_post(index, post, user)

        elif type == "drafts":
            index = render_drafts(index, post, user)

    questionary.press_any_key_to_continue(
        "Pressione qualquer tecla para voltar ao menu.").ask()
    return None
