def calcular(lancamentos, saldo_inicial=0.0, reserva_reposicao=0.0):
    caixa = saldo_inicial
    comprometido = 0.0
    perdas = 0.0

    for l in lancamentos:
        tipo, valor = l["tipo"], l["valor"]
        if tipo == "entrada":
            caixa += valor
        elif tipo in ("saida", "compra_mercadoria", "retirada_pessoal"):
            caixa -= valor
        elif tipo == "perda":
            perdas += valor  # a perda não mexe no caixa, só mede o desperdício
        elif tipo == "compromisso":
            if l["pago"]:
                caixa -= valor
            else:
                comprometido += valor

    livre = caixa - comprometido - reserva_reposicao
    return {
        "caixa": caixa,
        "comprometido": comprometido,
        "reserva": reserva_reposicao,
        "livre": livre,
        "pode_retirar": max(0.0, livre),
        "perdas": perdas,
    }