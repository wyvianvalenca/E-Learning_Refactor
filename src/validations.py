def is_non_empty(text: str) -> bool | str:
    if len(text.strip()) > 0:
        return True
    else:
        return "O texto não pode ser vazio."


def text_geq_100characters(text: str) -> bool | str:
    if len(text.strip()) >= 100:
        return True
    else:
        return "O texto precisa ter no mínimo 100 caracteres"


def text_geq_50characters(text: str) -> bool | str:
    if len(text.strip()) >= 50:
        return True
    else:
        return "O texto precisa ter no mínimo 50 caracteres"


def text_has_2words(text: str) -> bool | str:
    if len(text.split(" ")) >= 2:
        return True
    else:
        return "O texto precisa ter pelo menos 2 palavras"


def is_positive_number(text: str) -> bool | str:
    try:
        f: float = float(text)
        if f >= 0:
            return True
        else:
            return "O número deve ser positivo."
    except ValueError:
        return "Por favor insira um número."
