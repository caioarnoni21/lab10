def contar_palavras(texto):
    contagem = {}
    for palavra in texto.lower().split():
        palavra = palavra.strip(".,;:!?")
        contagem[palavra] = contagem.get(palavra, 0) + 1
    return contagem
