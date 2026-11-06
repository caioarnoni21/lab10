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


def test_cupom_dez_abaixo_do_minimo_nao_da_desconto(carrinho):
    carrinho.adicionar(5000)
    carrinho.aplicar_cupom("DEZ")
    assert carrinho.total == 5000


def test_cupom_desconhecido_e_rejeitado(carrinho):
    with pytest.raises(ValueError):
        carrinho.aplicar_cupom("XYZ")


def test_cupom_antes_de_itens_abaixo_do_minimo_nao_da_desconto(carrinho):
    carrinho.aplicar_cupom("DEZ")
    carrinho.adicionar(1000)
    assert carrinho.total == 1000


def test_cupom_dez_um_centavo_abaixo_do_minimo(carrinho):
    carrinho.adicionar(9999)
    carrinho.aplicar_cupom("DEZ")
    assert carrinho.total == 9999


def test_cupom_dez_exatamente_no_minimo(carrinho):
    carrinho.adicionar(10000)
    carrinho.aplicar_cupom("DEZ")
    assert carrinho.total == 9000


def test_desconto_vale_quando_subtotal_chega_ao_minimo(carrinho):
    carrinho.aplicar_cupom("DEZ")
    carrinho.adicionar(5000)
    assert carrinho.total == 5000
    carrinho.adicionar(5000)
    assert carrinho.total == 9000


def test_cupom_vinte_no_minimo_da_20_por_cento(carrinho):
    carrinho.adicionar(30000)
    carrinho.aplicar_cupom("VINTE")
    assert carrinho.total == 24000
