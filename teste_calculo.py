from calculo import calcular


def test_saldo_livre_desconta_o_que_ja_tem_dono():
    lancamentos = [
        {"tipo": "entrada", "valor": 320, "pago": 1},
        {"tipo": "saida", "valor": 40, "pago": 1},
        {"tipo": "retirada_pessoal", "valor": 100, "pago": 1},
        {"tipo": "compra_mercadoria", "valor": 180, "pago": 1},
        {"tipo": "perda", "valor": 25, "pago": 1},
        {"tipo": "compromisso", "valor": 600, "pago": 0},
    ]
    r = calcular(lancamentos, saldo_inicial=1000)
    assert r["caixa"] == 1000
    assert r["comprometido"] == 600
    assert r["livre"] == 400
    assert r["perdas"] == 25  # perda não mexe no caixa


def test_compromisso_pago_sai_do_caixa():
    lancamentos = [{"tipo": "compromisso", "valor": 300, "pago": 1}]
    r = calcular(lancamentos, saldo_inicial=1000)
    assert r["caixa"] == 700
    assert r["comprometido"] == 0


def test_nao_pode_retirar_quando_deve_mais_que_tem():
    lancamentos = [{"tipo": "compromisso", "valor": 900, "pago": 0}]
    r = calcular(lancamentos, saldo_inicial=500)
    assert r["livre"] == -400
    assert r["pode_retirar"] == 0


if __name__ == "__main__":
    test_saldo_livre_desconta_o_que_ja_tem_dono()
    test_compromisso_pago_sai_do_caixa()
    test_nao_pode_retirar_quando_deve_mais_que_tem()
    print("Todos os testes passaram.")