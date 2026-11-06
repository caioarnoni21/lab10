from collections import deque


class Fila:
    def __init__(self):
        self._emitidas = {"normal": 0, "prioritaria": 0}
        self._normais = deque()
        self._prioritarias = deque()

    @property
    def aguardando(self):
        return len(self._normais) + len(self._prioritarias)

    def emitir(self, tipo):
        if tipo not in self._emitidas:
            raise ValueError(f"tipo desconhecido: {tipo}")
        self._emitidas[tipo] += 1
        if tipo == "prioritaria":
            senha = f"P{self._emitidas[tipo]}"
            self._prioritarias.append(senha)
        else:
            senha = f"N{self._emitidas[tipo]}"
            self._normais.append(senha)
        return senha

    def chamar(self):
        if self._prioritarias:
            return self._prioritarias.popleft()
        if self._normais:
            return self._normais.popleft()
        raise IndexError("fila vazia")
