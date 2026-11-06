from collections import deque

PREFIXOS = {"normal": "N", "prioritaria": "P"}


class Fila:
    def __init__(self):
        self._emitidas = {tipo: 0 for tipo in PREFIXOS}
        self._filas = {tipo: deque() for tipo in PREFIXOS}
        self._prioritarias_seguidas = 0

    @property
    def aguardando(self):
        return sum(len(fila) for fila in self._filas.values())

    def emitir(self, tipo):
        if tipo not in PREFIXOS:
            raise ValueError(f"tipo desconhecido: {tipo}")
        self._emitidas[tipo] += 1
        senha = f"{PREFIXOS[tipo]}{self._emitidas[tipo]}"
        self._filas[tipo].append(senha)
        return senha

    def chamar(self):
        normais = self._filas["normal"]
        prioritarias = self._filas["prioritaria"]
        if prioritarias and not (self._prioritarias_seguidas >= 2 and normais):
            self._prioritarias_seguidas += 1
            return prioritarias.popleft()
        if normais:
            return normais.popleft()
        raise IndexError("fila vazia")
