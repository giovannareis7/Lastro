import html
import datetime
import uuid

import streamlit as st

import banco
import calculo
from ia import interpretar

st.set_page_config(page_title="Lastro", page_icon="✦", layout="wide")
banco.iniciar()

# cada visitante recebe a própria cópia da demonstração
if "sid" not in st.session_state:
    st.session_state["sid"] = uuid.uuid4().hex
    banco.popular_demo(st.session_state["sid"])
SID = st.session_state["sid"]
if "saldo_inicial" not in st.session_state:
    st.session_state["saldo_inicial"] = 1000.0

CSS = (
    "<style>"
    "@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,700;9..144,800&family=Inter+Tight:wght@400;500;600;700;800&display=swap');"
    ":root { --bg: #1F1611; --espresso: #523828; --bronze: #946E4B; --ouro: #D4A569; --ouro-claro: #DCC89A; "
    "--champagne: #F9F0D6; --muda: #B69A67; --alerta: #E0674A; --ambar: #E8A33D; "
    "--vidro: rgba(249,240,214,.05); --borda: rgba(212,165,105,.22); }"
    ".stApp { font-family: 'Inter Tight', sans-serif; color: var(--champagne); "
    "background: radial-gradient(900px 560px at 100% 0%, rgba(212,165,105,.22), transparent 62%), "
    "radial-gradient(700px 520px at 0% 100%, rgba(148,110,75,.20), transparent 60%), var(--bg); }"
    ".block-container { padding-top: 1.4rem; max-width: 1200px; }"
    ".stDeployButton, footer { display: none !important; }"
    "header[data-testid='stHeader'] { background: transparent; } div[data-testid='stToolbar'] { visibility: hidden; }"
    ".nav { display: flex; justify-content: space-between; align-items: center; padding: 8px 8px 8px 26px; "
    "border: 1px solid var(--borda); border-radius: 999px; margin-bottom: 22px; "
    "background: linear-gradient(90deg, rgba(212,165,105,.12), rgba(249,240,214,.02)); }"
    ".nav .logo { font-family: 'Fraunces', Georgia, serif; font-size: 1.7rem; font-weight: 700; "
    "font-style: italic; letter-spacing: -.02em; color: var(--champagne); }"
    ".nav .tag { background: var(--ouro); color: #1F1611; font-weight: 700; border-radius: 999px; "
    "padding: 10px 20px; font-size: .9rem; }"
    ".marca-sub { color: var(--muda); font-size: 1.05rem; margin: 0 0 20px; }"
    ".marca-sub b { color: var(--champagne); }"
    ".hero { position: relative; overflow: hidden; border: 1px solid var(--borda); border-radius: 28px; "
    "padding: 30px 32px; background: linear-gradient(135deg, rgba(212,165,105,.22), rgba(82,56,40,.40) 70%); }"
    ".hero::before { content: ''; position: absolute; inset: 0; "
    "background: repeating-linear-gradient(115deg, rgba(220,200,154,.10) 0 2px, transparent 2px 26px); "
    "-webkit-mask-image: linear-gradient(90deg, transparent 35%, #000 100%); "
    "mask-image: linear-gradient(90deg, transparent 35%, #000 100%); }"
    ".hero.alerta { background: linear-gradient(135deg, rgba(224,103,74,.24), rgba(82,56,40,.40) 70%); }"
    ".hero.alerta::before { background: repeating-linear-gradient(115deg, rgba(224,103,74,.14) 0 2px, transparent 2px 26px); }"
    ".rotulo { font-size: .72rem; font-weight: 600; letter-spacing: .14em; text-transform: uppercase; "
    "color: var(--muda); position: relative; z-index: 1; }"
    ".pulso { display: inline-block; width: 8px; height: 8px; border-radius: 50%; background: var(--ouro); "
    "margin-right: 8px; box-shadow: 0 0 10px var(--ouro); animation: pulso 1.8s ease-in-out infinite; }"
    "@keyframes pulso { 0%, 100% { opacity: 1; } 50% { opacity: .3; } }"
    ".hero-titulo { font-family: 'Fraunces', Georgia, serif; font-size: 2.5rem; line-height: 1.06; font-weight: 800; "
    "letter-spacing: -.02em; margin: 12px 0 14px; color: var(--champagne); position: relative; z-index: 1; }"
    ".neon { background: linear-gradient(90deg, #F9F0D6, #D4A569); -webkit-background-clip: text; "
    "background-clip: text; color: transparent; }"
    ".hero.alerta .neon { background: linear-gradient(90deg, #FFD2B8, #E0674A); -webkit-background-clip: text; "
    "background-clip: text; color: transparent; }"
    ".hero p { margin: 0; color: #E6D9B8; font-size: 1.05rem; position: relative; z-index: 1; }"
    ".hero p b { color: var(--champagne); }"
    ".stats { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin: 14px 0; }"
    ".stat { background: var(--vidro); border: 1px solid var(--borda); border-radius: 18px; padding: 14px 16px; }"
    ".stat .num { font-size: 1.3rem; font-weight: 800; letter-spacing: -.02em; color: var(--champagne); "
    "margin-top: 6px; font-variant-numeric: tabular-nums; }"
    ".stat.livre .num { color: var(--ouro); }"
    ".titulo-reg { font-family: 'Fraunces', Georgia, serif; font-size: 1.9rem; font-weight: 700; line-height: 1.1; "
    "margin: 10px 0 6px; color: var(--champagne); }"
    ".sub-reg { color: var(--muda); margin-bottom: 12px; }"
    ".exemplos { color: var(--muda); font-size: .85rem; margin-top: 10px; line-height: 1.6; }"
    ".barra { display: flex; height: 32px; border-radius: 999px; overflow: hidden; padding: 3px; gap: 3px; "
    "background: rgba(249,240,214,.07); border: 1px solid var(--borda); margin-top: 6px; }"
    ".seg { height: 100%; border-radius: 999px; }"
    ".seg.livre { background: linear-gradient(90deg, #D4A569, #DCC89A); box-shadow: 0 0 18px rgba(212,165,105,.55); }"
    ".legenda { display: flex; flex-wrap: wrap; gap: 6px 18px; font-size: .85rem; color: var(--muda); margin-top: 10px; }"
    ".dot { display: inline-block; width: 10px; height: 10px; border-radius: 50%; margin-right: 6px; }"
    ".nota { color: var(--muda); font-size: .9rem; margin: 12px 0 0; }"
    ".secao { font-family: 'Fraunces', Georgia, serif; font-size: 1.5rem; font-weight: 700; margin: 34px 0 12px; "
    "color: var(--champagne); }"
    ".veredito { border-radius: 16px; padding: 14px 18px; margin-top: 10px; background: var(--vidro); "
    "border: 1px solid var(--borda); color: var(--champagne); }"
    ".veredito.ok { border-color: rgba(212,165,105,.65); box-shadow: 0 0 22px rgba(212,165,105,.15); }"
    ".veredito.no { border-color: rgba(224,103,74,.65); box-shadow: 0 0 22px rgba(224,103,74,.16); }"
    ".veredito.aviso { border-color: rgba(232,163,61,.65); }"
    ".card { display: flex; justify-content: space-between; align-items: center; gap: 12px; "
    "background: var(--vidro); border: 1px solid var(--borda); border-left: 4px solid var(--ouro); "
    "border-radius: 16px; padding: 12px 16px; margin-bottom: 8px; }"
    ".card.urgente { border-left-color: var(--alerta); }"
    ".card.atencao { border-left-color: var(--ambar); }"
    ".card.neutro { border-left-color: var(--muda); }"
    ".card .titulo { font-weight: 700; color: var(--champagne); }"
    ".card .valor { font-weight: 800; white-space: nowrap; color: var(--champagne); font-variant-numeric: tabular-nums; }"
    ".sub { color: var(--muda); font-size: .85rem; margin-top: 4px; }"
    ".chip { font-size: .66rem; font-weight: 700; letter-spacing: .1em; padding: 2px 8px; "
    "border-radius: 999px; border: 1px solid currentColor; margin-right: 8px; }"
    ".chip.urgente { color: var(--alerta); } .chip.atencao { color: var(--ambar); }"
    ".chip.ok { color: var(--ouro); } .chip.neutro { color: var(--muda); }"
    ".linha { display: flex; justify-content: space-between; gap: 12px; padding: 10px 0; "
    "border-bottom: 1px solid var(--borda); color: var(--champagne); }"
    ".pos { color: var(--ouro); font-weight: 700; white-space: nowrap; font-variant-numeric: tabular-nums; }"
    ".neg { color: var(--alerta); font-weight: 700; white-space: nowrap; font-variant-numeric: tabular-nums; }"
    ".neutro { color: var(--muda); white-space: nowrap; font-variant-numeric: tabular-nums; }"
    "div[data-testid='stForm'] { border: 1px solid rgba(212,165,105,.45); border-radius: 22px; "
    "background: var(--vidro); box-shadow: 0 0 32px rgba(212,165,105,.10); padding: 18px; }"
    ".stTextArea textarea, .stTextInput input, .stNumberInput input { border-radius: 14px !important; }"
    "button[data-testid^='stBaseButton-primary'] { background: var(--ouro); border: none; border-radius: 999px; "
    "font-weight: 700; padding: .55rem 1.8rem; }"
    "button[data-testid^='stBaseButton-primary'] * { color: #1F1611 !important; }"
    "button[data-testid^='stBaseButton-primary']:hover { filter: brightness(1.08); }"
    "button[data-testid^='stBaseButton-secondary'] { background: transparent; border: 1px solid var(--ouro); "
    "border-radius: 999px; color: var(--ouro); font-weight: 700; padding: .45rem 1.3rem; }"
    "button[data-testid^='stBaseButton-secondary'] * { color: inherit !important; }"
    "button[data-testid^='stBaseButton-secondary']:hover { background: var(--ouro); color: #1F1611; }"
    "@media (max-width: 640px) { .stats { grid-template-columns: 1fr; } .hero-titulo { font-size: 2rem; } }"
    "</style>"
)
st.markdown(CSS, unsafe_allow_html=True)

ICONES = {
    "entrada": "💰",
    "saida": "🧾",
    "compra_mercadoria": "🛒",
    "perda": "🗑️",
    "compromisso": "📌",
    "retirada_pessoal": "👤",
}
CORES_DIVIDA = ["#946E4B", "#7A6640", "#B69A67"]


def brl(v):
    # &#36; é o símbolo $ (evita que o Streamlit trate dois $ como fórmula)
    s = f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return "R&#36; " + s


def data_br(iso):
    try:
        return datetime.date.fromisoformat(iso).strftime("%d/%m")
    except (TypeError, ValueError):
        return "sem data"


def dias_para(iso):
    try:
        return (datetime.date.fromisoformat(iso) - datetime.date.today()).days
    except (TypeError, ValueError):
        return None


def texto_prazo(iso):
    d = dias_para(iso)
    if d is None:
        return "sem data"
    if d < 0:
        return f"venceu há {-d} dia(s)"
    if d == 0:
        return "vence hoje"
    if d == 1:
        return "vence amanhã"
    return f"vence em {d} dias · {data_br(iso)}"


def chip_prazo(iso):
    d = dias_para(iso)
    if d is None:
        return "neutro", "SEM DATA"
    if d <= 2:
        return "urgente", "URGENTE"
    if d <= 5:
        return "atencao", "ATENÇÃO"
    return "ok", "NO PRAZO"


def primeiro_furo(pendentes, caixa_apos):
    # anda pelos boletos na ordem de vencimento e acha o primeiro que não fecha
    acumulado = 0.0
    for p in pendentes:
        acumulado += p["valor"]
        if acumulado > caixa_apos:
            return p, acumulado - caixa_apos
    return None


def veredito(classe, texto):
    st.markdown(f"<div class='veredito {classe}'>{texto}</div>", unsafe_allow_html=True)


def recarregar_demo():
    banco.popular_demo(SID)
    st.session_state["saldo_inicial"] = 1000.0


def comecar_do_zero():
    banco.limpar(SID)
    st.session_state["saldo_inicial"] = 0.0


# ---------- barra lateral ----------
saldo_inicial = st.sidebar.number_input("Saldo inicial do caixa", step=50.0, key="saldo_inicial")
reserva = st.sidebar.number_input("Reserva para repor mercadoria", value=0.0, step=50.0)

# ---------- cálculos ----------
lancamentos = banco.listar(SID)
r = calculo.calcular(lancamentos, saldo_inicial, reserva)
pendentes = [l for l in lancamentos if l["tipo"] == "compromisso" and not l["pago"]]
pendentes = sorted(pendentes, key=lambda l: l["vencimento"] or "9999-12-31")
dividas = r["comprometido"] + r["reserva"]

# ---------- topo ----------
st.markdown(
    "<div class='nav'><span class='logo'>Lastro.</span>"
    "<span class='tag'>Demonstração · Ana Beatriz · Hortifruti</span></div>",
    unsafe_allow_html=True,
)
st.markdown(
    "<div class='marca-sub'>O banco mostra quanto você tem. A Lastro mostra o que você pode usar para ficar tranquilo(a).</div>",
    unsafe_allow_html=True,
)

if not lancamentos and saldo_inicial == 0:
    classe = "hero"
    titulo = "Vamos começar <span class='neon'>do zero</span>"
    sub = "Registre ao lado o que entrou e o que saiu. Se já tem dinheiro no caixa, informe o saldo inicial no menu lateral."
elif r["livre"] > 0:
    classe = "hero"
    titulo = f"Hoje você pode retirar até <span class='neon'>{brl(r['pode_retirar'])}</span>"
    sub = f"Seu caixa tem {brl(r['caixa'])}, mas <b>{brl(dividas)} já têm dono.</b>"
else:
    classe = "hero alerta"
    titulo = "Segura a retirada <span class='neon'>por enquanto</span>"
    falta = -r["livre"]
    if falta > 0:
        sub = f"O caixa tem {brl(r['caixa'])} e você deve <b>{brl(dividas)}</b>. Faltam <b>{brl(falta)}</b>."
    else:
        sub = "Todo o dinheiro do caixa já está <b>destinado</b>."

# ---------- situação (esquerda) + registrar (direita) ----------
col_sit, col_reg = st.columns([1.25, 1], gap="large")

with col_sit:
    st.markdown(
        f"<div class='{classe}'><div class='rotulo'><span class='pulso'></span>Dinheiro com dono</div>"
        f"<div class='hero-titulo'>{titulo}</div><p>{sub}</p></div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<div class='stats'>"
        f"<div class='stat'><div class='rotulo'>Caixa</div><div class='num'>{brl(r['caixa'])}</div></div>"
        f"<div class='stat'><div class='rotulo'>Já tem dono</div><div class='num'>{brl(dividas)}</div></div>"
        f"<div class='stat livre'><div class='rotulo'>Livre</div><div class='num'>{brl(r['livre'])}</div></div>"
        "</div>",
        unsafe_allow_html=True,
    )

with col_reg:
    st.markdown(
        "<div class='rotulo'><span class='pulso'></span>Registrar agora</div>"
        "<div class='titulo-reg'>Conte o que aconteceu de novidade</div>"
        "<div class='sub-reg'>Vendas, compras, perdas, contas a pagar. Escreva do seu jeito e nós organizamos.</div>",
        unsafe_allow_html=True,
    )
    with st.form("registro", clear_on_submit=True):
        texto = st.text_area(
            "Conte do seu jeito",
            placeholder="Ex: vendi 320 hoje, paguei 40 de gelo e tirei 100 pra mim",
            height=110,
            label_visibility="collapsed",
        )
        enviar = st.form_submit_button("Registrar", type="primary")
    st.markdown(
        "<div class='exemplos'>Exemplos: <i>“comprei 3 caixas de tomate por 180”</i> · "
        "<i>“perdi 2 quilos de banana”</i> · <i>“devo 600 pro fornecedor, pago na sexta”</i></div>",
        unsafe_allow_html=True,
    )

    if enviar and texto.strip():
        try:
            with st.spinner("Entendendo..."):
                itens = interpretar(texto)
            for i in itens:
                banco.salvar(SID, i.tipo, i.valor, i.descricao, i.vencimento)
            resumo = ", ".join(f"{i.tipo}: {brl(i.valor)}" for i in itens)
            st.session_state["aviso"] = f"Registrei: {resumo}"
            st.rerun()
        except Exception as e:
            st.error(f"Não consegui registrar agora. Tente de novo em instantes. ({e})")

    if "aviso" in st.session_state:
        st.success(st.session_state.pop("aviso"))

# ---------- barra do dinheiro ----------
st.markdown("<div class='secao'>Para onde vai o dinheiro</div>", unsafe_allow_html=True)
base = max(r["caixa"], dividas, 1)
segs = []
legenda = []
for i, p in enumerate(pendentes):
    cor = CORES_DIVIDA[i % len(CORES_DIVIDA)]
    pct = p["valor"] / base * 100
    segs.append(f"<div class='seg' style='width:{pct:.2f}%;background:{cor}'></div>")
    legenda.append(
        f"<span><span class='dot' style='background:{cor}'></span>"
        f"{html.escape(p['descricao'])} {brl(p['valor'])}</span>"
    )
if r["reserva"] > 0:
    pct = r["reserva"] / base * 100
    segs.append(f"<div class='seg' style='width:{pct:.2f}%;background:var(--ambar)'></div>")
    legenda.append(
        f"<span><span class='dot' style='background:var(--ambar)'></span>Reserva {brl(r['reserva'])}</span>"
    )
if r["livre"] > 0:
    pct = r["livre"] / base * 100
    segs.append(f"<div class='seg livre' style='width:{pct:.2f}%'></div>")
    legenda.append(
        f"<span><span class='dot' style='background:var(--ouro)'></span><b>Livre {brl(r['livre'])}</b></span>"
    )
st.markdown(
    f"<div class='barra'>{''.join(segs)}</div><div class='legenda'>{''.join(legenda)}</div>"
    f"<p class='nota'>🗑️ Foi para o lixo: <b>{brl(r['perdas'])}</b></p>",
    unsafe_allow_html=True,
)

# ---------- posso retirar? + a pagar ----------
c1, c2 = st.columns(2, gap="large")

with c1:
    st.markdown("<div class='secao'>Posso retirar?</div>", unsafe_allow_html=True)
    valor = st.number_input("Quanto você quer tirar? (em reais)", min_value=0.0, value=0.0, step=50.0)
    if valor > 0:
        if valor <= r["pode_retirar"]:
            sobra = r["pode_retirar"] - valor
            veredito("ok", f"<b>Pode.</b> Depois de tirar {brl(valor)}, ainda sobram {brl(sobra)} livres.")
        else:
            furo = primeiro_furo(pendentes, r["caixa"] - valor)
            if furo:
                p, falta_p = furo
                veredito(
                    "no",
                    f"<b>Melhor não.</b> Se tirar {brl(valor)}, faltam {brl(falta_p)} para pagar "
                    f"“{html.escape(p['descricao'])}” ({texto_prazo(p['vencimento'])}).",
                )
            else:
                veredito("aviso", "<b>Atenção.</b> Isso invadiria a reserva para repor mercadoria.")

with c2:
    st.markdown("<div class='secao'>A pagar</div>", unsafe_allow_html=True)
    if not pendentes:
        st.write("Nenhum compromisso em aberto. 🎉")
    for p in pendentes:
        status, rotulo_chip = chip_prazo(p["vencimento"])
        col1, col2 = st.columns([3, 1])
        col1.markdown(
            f"<div class='card {status}'><div><div class='titulo'>{html.escape(p['descricao'])}</div>"
            f"<div class='sub'><span class='chip {status}'>{rotulo_chip}</span>{texto_prazo(p['vencimento'])}</div></div>"
            f"<div class='valor'>{brl(p['valor'])}</div></div>",
            unsafe_allow_html=True,
        )
        if col2.button("Paguei", key=f"pagar_{p['id']}"):
            banco.marcar_pago(p["id"])
            st.rerun()

# ---------- movimentações ----------
st.markdown("<div class='secao'>Últimas movimentações</div>", unsafe_allow_html=True)
linhas = []
for l in lancamentos[::-1][:12]:
    t = l["tipo"]
    if t == "entrada":
        cls, sinal = "pos", "+"
    elif t in ("saida", "compra_mercadoria", "retirada_pessoal") or (t == "compromisso" and l["pago"]):
        cls, sinal = "neg", "−"
    else:
        cls, sinal = "neutro", ""
    linhas.append(
        f"<div class='linha'><span>{ICONES.get(t, '•')} {html.escape(l['descricao'])} "
        f"<span class='sub'>{data_br(l['data'])}</span></span>"
        f"<span class='{cls}'>{sinal}{brl(l['valor'])}</span></div>"
    )
if linhas:
    st.markdown("".join(linhas), unsafe_allow_html=True)
else:
    st.write("Nenhuma movimentação ainda. Registre a primeira ali em cima.")

# ---------- testar como novo cliente ----------
st.markdown("<div class='secao'>Teste como um novo cliente</div>", unsafe_allow_html=True)
st.markdown(
    "<div class='sub-reg'>Cada visitante tem a própria cópia. Volte à demonstração da Ana Beatriz  "
    "ou comece do zero com os seus números.</div>",
    unsafe_allow_html=True,
)
b1, b2, _ = st.columns([1, 1, 2])
b1.button("🔄 Recarregar demonstração", on_click=recarregar_demo)
b2.button("🆕 Começar do zero", on_click=comecar_do_zero)
