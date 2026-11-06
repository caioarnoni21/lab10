CUPONS = {"DEZ": 10, "VINTE": 20}  # codigo -> porcentagem de desconto
MINIMOS = {"DEZ": 10000, "VINTE": 30000}  # codigo -> subtotal minimo


class Carrinho:
    def __init__(self):
        self._subtotal = 0
        self._cupom = None

    def adicionar(self, preco, quantidade=1):
        if preco <= 0:
            raise ValueError("preco deve ser positivo")
        if quantidade < 1:
            raise ValueError("quantidade deve ser ao menos 1")
        self._subtotal += preco * quantidade

    def aplicar_cupom(self, codigo):
        if codigo not in CUPONS:
            raise ValueError("cupom desconhecido")
        self._cupom = codigo

    @property
    def total(self):
        if self._cupom is None or self._subtotal < MINIMOS[self._cupom]:
            return self._subtotal
        return self._subtotal * (100 - CUPONS[self._cupom]) // 100
