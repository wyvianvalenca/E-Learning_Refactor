from rich.panel import Panel
from rich.text import Text
from models import ForumPost, Comentario 
from main import console

def mostrar_post(post: ForumPost) -> None:
    texto: str = post.header + "\n" + post.conteudo
    painel: Panel = Panel(Text(text=texto).wrap(console, width=500)).fit()
    console.print(painel)
