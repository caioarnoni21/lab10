class Fila:
    def __init__(self):
        self._emitidas = {"normal": 0, "prioritaria": 0}
        self._esperando = []

    @property
    def aguardando(self):
        return len(self._esperando)

    def emitir(self, tipo):
        if tipo not in self._emitidas:
            raise ValueError(f"tipo desconhecido: {tipo}")
        self._emitidas[tipo] += 1
        prefixo = "P" if tipo == "prioritaria" else "N"
        senha = f"{prefixo}{self._emitidas[tipo]}"
        self._esperando.append(senha)
        return senha
