from collections import Counter


def _palavras(texto):
    for bruta in texto.lower().split():
        palavra = bruta.strip(".,;:!?")
        if palavra:
            yield palavra


def contar_palavras(texto):git 
    return dict(Counter(_palavras(texto)))
