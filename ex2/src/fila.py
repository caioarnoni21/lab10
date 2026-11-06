from collections import deque

PREFIXOS = {"normal": "N", "prioritaria": "P"}
LIMITE_PRIORITARIAS_SEGUIDAS = 2


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

    def _vez_da_normal(self):
        normais = self._filas["normal"]
        prioritarias = self._filas["prioritaria"]
        if not prioritarias:
            return bool(normais)
        limite_atingido = self._prioritarias_seguidas >= LIMITE_PRIORITARIAS_SEGUIDAS
        return limite_atingido and bool(normais)

    def chamar(self):
        if not self.aguardando:
            raise IndexError("fila vazia")
        if self._vez_da_normal():
            self._prioritarias_seguidas = 0
            return self._filas["normal"].popleft()
        self._prioritarias_seguidas += 1
        return self._filas["prioritaria"].popleft()
