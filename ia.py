import os
import json
import time
import datetime
from typing import Literal, Optional

from dotenv import load_dotenv
from google import genai
from google.genai import types, errors
from pydantic import BaseModel

load_dotenv()
client = genai.Client(
    api_key=os.environ["GEMINI_API_KEY"],
    http_options=types.HttpOptions(timeout=90000),  # desiste após 90s
)
MODELO = "gemini-3.5-flash-lite"

class Lancamento(BaseModel):
    tipo: Literal[
        "entrada", "saida", "compra_mercadoria",
        "perda", "compromisso", "retirada_pessoal",
    ]
    valor: float
    descricao: str
    vencimento: Optional[str] = None  # formato AAAA-MM-DD


INSTRUCOES = (
    "Você ajuda o dono de um hortifruti a registrar o dinheiro do negócio.\n"
    "Leia a mensagem e extraia TODOS os lançamentos citados.\n\n"
    "Tipos:\n"
    "- entrada: dinheiro que entrou (vendas do dia, recebimento de cliente)\n"
    "- saida: despesa do negócio paga na hora (gelo, luz, sacolas, gasolina)\n"
    "- compra_mercadoria: compra de frutas, verduras ou legumes para revender, paga na hora\n"
    "- perda: mercadoria estragada ou jogada fora (valor estimado; use 0 se não for informado)\n"
    "- compromisso: algo a pagar no futuro (fornecedor, boleto). Inclua o vencimento "
    "em AAAA-MM-DD. Compra feita para pagar depois é só um compromisso.\n"
    "- retirada_pessoal: dinheiro tirado do negócio para uso pessoal ou da casa\n\n"
    "Não invente valores nem datas que não foram ditos.\n"
)


def interpretar(texto: str) -> list[Lancamento]:
    hoje = datetime.date.today().isoformat()
    prompt = INSTRUCOES + f"\nHoje é {hoje}.\n\nMensagem: {texto}"

    ultimo_erro = None
    for tentativa in range(5):
        try:
            resposta = client.models.generate_content(
                model=MODELO,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=list[Lancamento],
                ),
            )
            return [Lancamento(**item) for item in json.loads(resposta.text)]
        except errors.ServerError as e:
            ultimo_erro = e
            espera = 2 ** tentativa
            print(f"   (Google ocupado, tentativa {tentativa + 1}/5, aguardando {espera}s...)")
            time.sleep(espera)
    raise ultimo_erro