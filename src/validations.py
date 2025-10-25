def is_non_empty(text: str) -> bool | str:
    if len(text.strip()) > 0:
        return True
    else:
        return "O texto não pode ser vazio."


def is_positive_number(text: str) -> bool | str:
    try:
        f: float = float(text)
        if f >= 0:
            return True
        else:
            return "O número deve ser positivo."
    except ValueError:
        return "Por favor insira um número."


"""
VERIFICACAO DE ENTRADAS

eh texto > ta vazio > tem 30+ caracteres

eh numero > eh positivo > eh maior que zero
"""
