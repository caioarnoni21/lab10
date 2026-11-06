import pytest

from fila import Fila


def chamar_todas(fila, n):
    return [fila.chamar() for _ in range(n)]


def test_fila_nova_nao_tem_ninguem_aguardando():
    assert Fila().aguardando == 0


def test_primeira_senha_normal_e_n1():
    assert Fila().emitir("normal") == "N1"
