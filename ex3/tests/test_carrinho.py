import pytest

from carrinho import Carrinho


@pytest.fixture
def carrinho():
    return Carrinho()


def test_carrinho_vazio_tem_total_zero(carrinho):
    assert carrinho.total == 0


def test_um_item_soma_o_preco(carrinho):
    carrinho.adicionar(2500)
    assert carrinho.total == 2500


def test_quantidade_multiplica_o_preco(carrinho):
    carrinho.adicionar(2500, quantidade=2)
    assert carrinho.total == 5000


def test_preco_zero_e_rejeitado(carrinho):
    with pytest.raises(ValueError):
        carrinho.adicionar(0)


def test_cupom_dez_em_5000_da_4500(carrinho):
    carrinho.adicionar(5000)
    carrinho.aplicar_cupom("DEZ")
    assert carrinho.total == 4500


def test_cupom_desconhecido_e_rejeitado(carrinho):
    with pytest.raises(ValueError):
        carrinho.aplicar_cupom("XYZ")


def test_item_adicionado_apos_o_cupom_tambem_tem_desconto(carrinho):
    carrinho.aplicar_cupom("DEZ")
    carrinho.adicionar(1000)
    assert carrinho.total == 900
