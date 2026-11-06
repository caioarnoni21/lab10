from contador import contar_palavras


def test_texto_vazio_devolve_dicionario_vazio():
    assert contar_palavras("") == {}


def test_uma_palavra_conta_uma_vez():
    assert contar_palavras("teste") == {"teste": 1}


def test_espaco_separa_duas_palavras():
    assert contar_palavras("bom dia") == {"bom": 1, "dia": 1}
