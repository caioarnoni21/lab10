from collections import deque

PREFIXOS = {"normal": "N", "prioritaria": "P"}


class Fila:
    def __init__(self):
        self._emitidas = {tipo: 0 for tipo in PREFIXOS}
        self._filas = {tipo: deque() for tipo in PREFIXOS}

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
        if self._filas["prioritaria"]:
            return self._filas["prioritaria"].popleft()
        if self._filas["normal"]:
            return self._filas["normal"].popleft()
        raise IndexError("fila vazia")
