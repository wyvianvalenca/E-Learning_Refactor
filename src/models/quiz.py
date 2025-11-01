from typing_extensions import override


class PerguntaQuiz:
    """Classe que representa uma pergunta de quiz"""
    
    def __init__(self, pergunta: str,
                 alternativas: list[str],
                 resposta: str):
        self.pergunta: str = pergunta
        self.alternativas: list[str] = alternativas
        self.resposta: str = resposta

    @override
    def __repr__(self):
        return f"[PerguntaQuiz] {self.pergunta} - {self.alternativas})"

    def acertou(self, alternativaEscolhida: str) -> bool:
        return alternativaEscolhida == self.resposta


class Quiz:
    """Classe que representa um quiz completo"""
    
    def __init__(self, titulo: str, perguntas: list[PerguntaQuiz]):
        self.titulo: str = titulo
        self.perguntas: list[PerguntaQuiz] = perguntas

    @override
    def __repr__(self):
        return f"[Quiz] {self.titulo} ({len(self.perguntas)} perguntas)"

    @override
    def __str__(self) -> str:
        return self.__repr__()

    def criar_formulario(self) -> list[dict[str, str | list[str]]]:
        formulario: list[dict[str, str | list[str]]] = []
        for pergunta in self.perguntas:
            formulario.append({
                "type": "select",
                "name": pergunta.pergunta,
                "message": pergunta.pergunta,
                "choices": pergunta.alternativas
            })
        return formulario

    def nota(self, respostas: dict[str, str]) -> int:
        acertos: int = 0
        for pergunta in self.perguntas:
            if pergunta.acertou(respostas[pergunta.pergunta]):
                acertos += 1

        return acertos
