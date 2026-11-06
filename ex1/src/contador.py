from collections import Counter


def _palavras(texto):
    for bruta in texto.lower().split():
        yield bruta.strip(".,;:!?")


def contar_palavras(texto):
    return dict(Counter(_palavras(texto)))
