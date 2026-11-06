CUPONS = {  # codigo -> (porcentagem de desconto, subtotal minimo)
    "DEZ": (10, 10000),
    "VINTE": (20, 30000),
}


class Carrinho:
    def __init__(self):
        self._subtotal = 0
        self._cupom = None

    def adicionar(self, preco, quantidade=1):
        if preco <= 0:
            raise ValueError("preco deve ser positivo")
        if not isinstance(quantidade, int):
            raise ValueError("quantidade deve ser inteira")
        if quantidade < 1:
            raise ValueError("quantidade deve ser ao menos 1")
        self._subtotal += preco * quantidade

    def aplicar_cupom(self, codigo):
        if codigo not in CUPONS:
            raise ValueError("cupom desconhecido")
        self._cupom = codigo

    def _porcentagem(self):
        if self._cupom is None:
            return 0
        porcentagem, minimo = CUPONS[self._cupom]
        if self._subtotal < minimo:
            return 0
        return porcentagem

    @property
    def total(self):
        return self._subtotal * (100 - self._porcentagem()) // 100
