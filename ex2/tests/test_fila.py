import pytest

from fila import Fila


def chamar_todas(fila, n):
    return [fila.chamar() for _ in range(n)]


def test_fila_nova_nao_tem_ninguem_aguardando():
    assert Fila().aguardando == 0
