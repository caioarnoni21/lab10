from contador import contar_palavras


def test_texto_vazio_devolve_dicionario_vazio():
    assert contar_palavras("") == {}
