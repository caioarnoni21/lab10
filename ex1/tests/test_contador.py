from contador import contar_palavras


def test_texto_vazio_devolve_dicionario_vazio():
    assert contar_palavras("") == {}


def test_uma_palavra_conta_uma_vez():
    assert contar_palavras("teste") == {"teste": 1}


def test_espaco_separa_duas_palavras():
    assert contar_palavras("bom dia") == {"bom": 1, "dia": 1}


def test_palavra_repetida_soma_ocorrencias():
    assert contar_palavras("dia a dia") == {"dia": 2, "a": 1}


def test_quebra_de_linha_separa_palavras():
    assert contar_palavras("bom\ndia") == {"bom": 1, "dia": 1}


def test_varios_espacos_nao_criam_palavra_vazia():
    assert contar_palavras("bom   dia") == {"bom": 1, "dia": 1}


def test_hifen_interno_faz_parte_da_palavra():
    assert contar_palavras("guarda-chuva") == {"guarda-chuva": 1}


def test_maiusculas_contam_como_minusculas():
    assert contar_palavras("Dia dia DIA") == {"dia": 3}


def test_pontuacao_no_fim_e_ignorada():
    assert contar_palavras("fim. Fim!") == {"fim": 2}


def test_virgula_e_ponto_e_virgula_nas_bordas():
    assert contar_palavras(",dia, ;dia;") == {"dia": 2}


def test_dois_pontos_e_interrogacao_nas_bordas():
    assert contar_palavras(":dia: ?dia?") == {"dia": 2}


def test_so_pontuacao_devolve_dicionario_vazio():
    assert contar_palavras("... !") == {}
