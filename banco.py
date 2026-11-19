import sqlite3
import datetime

ARQUIVO = "dados.db"


def conectar():
    con = sqlite3.connect(ARQUIVO, timeout=10)
    con.row_factory = sqlite3.Row
    return con


def iniciar():
    con = conectar()
    # se existir uma versão antiga da tabela (sem a coluna "sessao"), recria
    colunas = [c["name"] for c in con.execute("PRAGMA table_info(lancamentos)").fetchall()]
    if colunas and "sessao" not in colunas:
        con.execute("DROP TABLE lancamentos")
    con.execute(
        "CREATE TABLE IF NOT EXISTS lancamentos ("
        "id INTEGER PRIMARY KEY AUTOINCREMENT, sessao TEXT, "
        "data TEXT, tipo TEXT, valor REAL, descricao TEXT, "
        "vencimento TEXT, pago INTEGER DEFAULT 0)"
    )
    con.commit()
    con.close()


def salvar(sessao, tipo, valor, descricao, vencimento=None, data=None, pago=None):
    # compromisso nasce como "não pago"; os outros tipos já aconteceram
    if pago is None:
        pago = 0 if tipo == "compromisso" else 1
    data = data or datetime.date.today().isoformat()
    con = conectar()
    con.execute(
        "INSERT INTO lancamentos (sessao, data, tipo, valor, descricao, vencimento, pago) "
        "VALUES (?, ?, ?, ?, ?, ?, ?)",
        (sessao, data, tipo, valor, descricao, vencimento, pago),
    )
    con.commit()
    con.close()


def listar(sessao):
    con = conectar()
    linhas = con.execute(
        "SELECT * FROM lancamentos WHERE sessao = ? ORDER BY id", (sessao,)
    ).fetchall()
    con.close()
    return [dict(l) for l in linhas]


def marcar_pago(id_lancamento):
    con = conectar()
    con.execute("UPDATE lancamentos SET pago = 1 WHERE id = ?", (id_lancamento,))
    con.commit()
    con.close()


def limpar(sessao):
    con = conectar()
    con.execute("DELETE FROM lancamentos WHERE sessao = ?", (sessao,))
    con.commit()
    con.close()


def popular_demo(sessao):
    # carrega duas semanas da Ana Beatriz (apaga o que essa sessão tinha antes)
    limpar(sessao)
    hoje = datetime.date.today()

    def dia(n):
        return (hoje + datetime.timedelta(days=n)).isoformat()

    v = "Vendas do dia"
    # (dia, tipo, valor, descrição, vencimento, pago)
    demo = [
        (-13, "entrada", 385, v, None, None),
        (-13, "compra_mercadoria", 520, "Ceasa: tomate, cebola e batata", None, None),
        (-12, "entrada", 420, v, None, None),
        (-12, "saida", 38, "Gelo", None, None),
        (-12, "retirada_pessoal", 150, "Retirada para a casa", None, None),
        (-11, "entrada", 395, v, None, None),
        (-11, "perda", 28, "Banana madura demais", None, None),
        (-10, "entrada", 460, v, None, None),
        (-10, "compra_mercadoria", 480, "Ceasa: frutas da semana", None, None),
        (-10, "saida", 90, "Gasolina da Kombi", None, None),
        (-9, "entrada", 610, v, None, None),
        (-9, "saida", 55, "Sacolas e embalagens", None, None),
        (-9, "compromisso", 700, "Fornecedor de legumes (boleto)", dia(-9), 1),
        (-8, "entrada", 540, v, None, None),
        (-8, "perda", 45, "Mamão e alface murchos", None, None),
        (-8, "retirada_pessoal", 200, "Mercado e contas de casa", None, None),
        (-7, "entrada", 370, v, None, None),
        (-7, "saida", 40, "Gelo", None, None),
        (-6, "entrada", 405, v, None, None),
        (-6, "entrada", 150, "Recebimento de cliente (fiado)", None, None),
        (-6, "compra_mercadoria", 450, "Ceasa: legumes e verduras", None, None),
        (-5, "entrada", 430, v, None, None),
        (-5, "saida", 120, "Diária do ajudante", None, None),
        (-5, "perda", 32, "Tomate machucado", None, None),
        (-5, "compromisso", 95, "Conta de água", dia(-5), 1),
        (-4, "entrada", 455, v, None, None),
        (-4, "saida", 35, "Gelo", None, None),
        (-4, "retirada_pessoal", 120, "Retirada pessoal", None, None),
        (-3, "entrada", 590, v, None, None),
        (-3, "compra_mercadoria", 500, "Ceasa: frutas e hortaliças", None, None),
        (-3, "compromisso", 380, "Conta de luz", dia(4), 0),
        (-2, "entrada", 520, v, None, None),
        (-2, "entrada", 90, "Recebimento de cliente (fiado)", None, None),
        (-2, "saida", 62, "Sacolas e embalagens", None, None),
        (-2, "perda", 38, "Folhas amarelando", None, None),
        (-2, "compromisso", 110, "Internet e maquininha", dia(-2), 1),
        (-2, "compromisso", 850, "Aluguel do ponto", dia(5), 0),
        (-1, "entrada", 410, v, None, None),
        (-1, "compra_mercadoria", 380, "Ceasa: reposição de frutas", None, None),
        (-1, "saida", 85, "Gasolina da Kombi", None, None),
        (-1, "perda", 22, "Morango estragado", None, None),
        (-1, "retirada_pessoal", 100, "Retirada para a casa", None, None),
        (-1, "compromisso", 900, "Fornecedor de legumes (boleto)", dia(2), 0),
        (0, "entrada", 365, v, None, None),
        (0, "compromisso", 520, "Fornecedor de frutas", dia(7), 0),
    ]
    demo.sort(key=lambda x: x[0])
    for d, tipo, valor, desc, venc, pago in demo:
        salvar(sessao, tipo, valor, desc, venc, dia(d), pago)
