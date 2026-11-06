import pytest

from fila import Fila


def chamar_todas(fila, n):
    return [fila.chamar() for _ in range(n)]


def test_fila_nova_nao_tem_ninguem_aguardando():
    assert Fila().aguardando == 0


def test_primeira_senha_normal_e_n1():
    assert Fila().emitir("normal") == "N1"


def test_senhas_normais_sao_numeradas_em_sequencia():
    fila = Fila()
    fila.emitir("normal")
    assert fila.emitir("normal") == "N2"


def test_prioritaria_tem_numeracao_propria():
    fila = Fila()
    fila.emitir("normal")
    assert fila.emitir("prioritaria") == "P1"
    assert fila.emitir("normal") == "N2"


def test_tipo_desconhecido_lanca_value_error():
    with pytest.raises(ValueError):
        Fila().emitir("vip")


def test_aguardando_conta_as_senhas_emitidas():
    fila = Fila()
    fila.emitir("normal")
    fila.emitir("prioritaria")
    assert fila.aguardando == 2


def test_chamar_fila_vazia_lanca_index_error():
    with pytest.raises(IndexError):
        Fila().chamar()
