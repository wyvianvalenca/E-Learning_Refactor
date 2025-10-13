from rich.panel import Panel
from rich.text import Text

import questionary

from models import ForumPost, Comentario, Usuario

from inicial import console


def nada(post: ForumPost, autor: Usuario) -> None:
    return None


def wip(post: ForumPost, autor: Usuario) -> None:
    console.print("Estamos trabalhando nisso...")
    return None


def comentar(pai: ForumPost, autor: Usuario) -> None:
    conteudo: str = questionary.text("Digite seu comentario:").ask()
    pai.comentarios.append(Comentario(pai, conteudo, autor))
    console.print("[bold green][OK][/] Comentario adicionado!")
    return None


def mostrar_comentarios(post: ForumPost, usuario_logado: Usuario) -> None:
    comentarios: str = ""

    for comentario in post.comentarios:
        comentarios = comentarios + f"{comentario}\n\n"

    console.print(Panel(comentarios, border_style="gray30"))

    questionary.press_any_key_to_continue(
        "Pressione qualquer tecla para voltar ao feed").ask()


def acoes_post(index: int, post: ForumPost, autor: Usuario) -> int:
    actions = {
        "Proximo": nada,
        "Comentar": comentar,
        "Ver Comentarios": mostrar_comentarios,
        "Anterior": nada
    }

    console.print()
    option: str = questionary.select("Choose an option:",
                                     choices=list(actions.keys())).ask()

    actions[option](post, autor)

    if option == "Proximo":
        return index + 1
    elif option == "Anterior":
        return index - 1 if index > 0 else 0
    else:
        return index


def mostrar_post(index: int, post: ForumPost, usuario_logado: Usuario) -> int:
    texto: str = post.header() + "\n" + post.conteudo
    painel: Panel = Panel.fit(Text(text=texto).wrap(console, width=100))
    console.print(painel)
    console.print()

    return acoes_post(index, post, usuario_logado)


def mostrar_feed(posts: list[ForumPost], usuario_logado: Usuario) -> None:
    index: int = 0
    while index < len(posts):
        post: ForumPost = posts[index]

        index = mostrar_post(index, post, usuario_logado)

    questionary.press_any_key_to_continue(
        "Pressione qualquer tecla para voltar ao menu.").ask()
    return None
