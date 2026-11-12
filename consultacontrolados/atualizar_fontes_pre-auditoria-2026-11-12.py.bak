# -*- coding: utf-8 -*-
"""
atualizar_fontes.py

Busca as duas fontes oficiais que alimentam o módulo (Portaria SVS/MS 344/98
e a Instrução Normativa vigente sobre antimicrobianos), funde com a
curadoria manual (detalhes_farmacologicos.json e excecoes.json, se
existirem nesta pasta) e grava o controlados.json final -- pronto para o
atualizar_pagina.py.

Substitui os antigos atualiza_controlados.py + atualiza_antimicrobianos.py +
estrutura_controlados.py (3 scripts, 2 arquivos intermediários) por um único
passo. Roda isto no SEU computador, com internet normal -- fora de qualquer
sandbox/bridge, já que os dois sites abaixo não são alcançáveis de dentro de
uma sessão restrita.

Uso:
    python3 atualizar_fontes.py

Gera:
    controlados.json -- dado final, pronto para o atualizar_pagina.py
"""

import requests
import re
import html as html_lib
import json
from datetime import date
from pathlib import Path

# Se a ANVISA revogar a Portaria 344/98 por uma nova norma (improvável, mas
# já aconteceu com os antimicrobianos -- ver abaixo), troque a URL aqui.
URL_PORTARIA_344 = (
    "https://anvisalegis.datalegis.net/action/ActionDatalegis.php"
    "?acao=abrirTextoAto&tipo=POR&numeroAto=00000344&seqAto=000"
    "&valorAno=1998&orgao=SVS%2FMS&codTipo=&desItem=&desItemFim="
    "&cod_menu=1696&cod_modulo=134&pesquisa=true"
)

# Se a IN 360/2025 for substituída por uma IN mais nova, troque numeroAto e
# valorAno aqui (mesmo padrão de parâmetros).
URL_IN_ANTIMICROBIANOS = (
    "https://anvisalegis.datalegis.net/action/ActionDatalegis.php"
    "?acao=abrirTextoAto&link=S&tipo=INM&numeroAto=00000360&seqAto=000"
    "&valorAno=2025&orgao=DC%2FANVISA%2FMS&cod_modulo=310&cod_menu=9431"
)

HEADERS = {"User-Agent": "Mozilla/5.0 (FarmaPratica-bot; contato: betofs1@gmail.com)"}

# Só as listas da Portaria 344/98 que correspondem a medicamento dispensável
# em farmácia com receita. D1, D2, E, F (precursores, insumos, plantas/fungos
# e substâncias proscritas) ficam de fora -- não é algo que se dispensa.
LISTAS_RELEVANTES = ["A1", "A2", "A3", "B1", "B2", "C1", "C2", "C3", "C5"]

REGRAS_POR_LISTA = {
    "A1": {"receita": "Notificação de Receita A (amarela)", "vias": 1, "validade_dias": 30, "retencao": True},
    "A2": {"receita": "Notificação de Receita A (amarela)", "vias": 1, "validade_dias": 30, "retencao": True},
    "A3": {"receita": "Notificação de Receita A (amarela)", "vias": 1, "validade_dias": 30, "retencao": True},
    "B1": {"receita": "Notificação de Receita B (azul)", "vias": 1, "validade_dias": 30, "retencao": True},
    "B2": {"receita": "Notificação de Receita B2 (azul)", "vias": 1, "validade_dias": 30, "retencao": True},
    "C1": {"receita": "Receita de Controle Especial (branca, 2 vias)", "vias": 2, "validade_dias": 30, "retencao": True},
    "C2": {"receita": "Receita de Controle Especial + Termo de Consentimento", "vias": 2, "validade_dias": 30, "retencao": True},
    "C3": {"receita": "Notificação de Receita Especial + Termo de Consentimento", "vias": 2, "validade_dias": 30, "retencao": True},
    "C5": {"receita": "Receita de Controle Especial (branca, 2 vias)", "vias": 2, "validade_dias": 30, "retencao": True},
}

REGRA_ANTIMICROBIANO = {
    "receita": "Receita simples, 2 vias (retenção da 2ª via)",
    "vias": 2,
    "validade_dias": 10,
    "retencao": True,
}

# Cabeçalho real no HTML bruto da Portaria: aparece em negrito, no formato
# "LISTA - A1", "LISTA - B1" etc. Isso distingue o cabeçalho de verdade de
# uma referência cruzada no texto corrido (ex.: "...relacionada na Lista
# A1"), que não tem essa marcação.
PADRAO_LISTA_HTML = re.compile(r'<b>\s*LISTA\s*[-–—"\']?\s*([A-F]\d?)\b', re.IGNORECASE)


def limpar_html(bruto: str) -> str:
    """Remove tags HTML e decodifica entidades (&eacute; -> é, etc.)."""
    sem_tags = re.sub(r'<[^>]+>', ' ', bruto)
    decodificado = html_lib.unescape(sem_tags)
    return re.sub(r'[ \t]+', ' ', decodificado)


def buscar(url: str) -> str:
    resp = requests.get(url, headers=HEADERS, timeout=30)
    resp.raise_for_status()
    return resp.text


# ---------------------------------------------------------------------------
# Parte 1: Portaria 344/98 (substâncias controladas)
# ---------------------------------------------------------------------------

def extrair_blocos_portaria(html_bruto: str) -> dict:
    """
    Localiza os cabeçalhos de lista no HTML BRUTO (antes de limpar), porque
    só ali dá pra distinguir um cabeçalho real (em negrito) de uma
    referência cruzada no texto. O anexo de verdade começa na ÚLTIMA
    ocorrência de "ANEXO I" (a primeira é só uma citação dentro do Art. 2).
    """
    posicoes = [m.start() for m in re.finditer(r'ANEXO I\b', html_bruto, re.IGNORECASE)]
    if not posicoes:
        raise RuntimeError(
            "Não encontrei 'ANEXO I' no texto retornado -- confira se a página "
            "carregou por completo, ou se a URL/formato mudou."
        )
    html_anexo = html_bruto[posicoes[-1]:]

    corte = re.search(r'ANEXO\s+II\b', html_anexo, re.IGNORECASE)
    if corte:
        html_anexo = html_anexo[:corte.start()]

    matches = list(PADRAO_LISTA_HTML.finditer(html_anexo))
    if not matches:
        raise RuntimeError(
            "Não encontrei nenhum cabeçalho de lista em negrito (<b>LISTA - X</b>) "
            "-- o HTML pode ter mudado de formato. Avise antes de prosseguir."
        )

    blocos = {}
    for i, m in enumerate(matches):
        codigo = m.group(1).upper()
        inicio = m.end()
        fim = matches[i + 1].start() if i + 1 < len(matches) else len(html_anexo)
        bloco_limpo = limpar_html(html_anexo[inicio:fim]).strip()
        if bloco_limpo:
            blocos.setdefault(codigo, bloco_limpo)
    return blocos


def parse_bloco(bloco: str):
    """Separa um bloco de texto corrido em (título, lista de substâncias, adendo)."""
    if "ADENDO:" in bloco:
        parte_itens, adendo = bloco.split("ADENDO:", 1)
    else:
        parte_itens, adendo = bloco, ""

    m = re.search(r'(?:^|\s)1\.\s*', parte_itens)
    if not m:
        return None, [], adendo.strip()

    titulo = parte_itens[:m.start()].strip()
    itens_texto = parte_itens[m.end():]
    itens = re.split(r'\s+\d+\.\s*', itens_texto)
    itens = [i.strip() for i in itens if i.strip()]
    return titulo, itens, adendo.strip()


def montar_listas_portaria():
    print("1/4 Buscando texto consolidado da Portaria 344/98...")
    html_bruto = buscar(URL_PORTARIA_344)
    blocos = extrair_blocos_portaria(html_bruto)

    listas = {}
    avisos = []
    for codigo in LISTAS_RELEVANTES:
        bloco = blocos.get(codigo)
        if not bloco:
            avisos.append(f"{codigo}: não encontrada no HTML -- confira manualmente.")
            continue
        titulo, substancias, adendo = parse_bloco(bloco)
        if not substancias:
            avisos.append(f"{codigo}: não consegui separar em itens -- confira manualmente.")
            continue
        listas[codigo] = {
            "titulo": titulo or f"LISTA {codigo}",
            "regra": REGRAS_POR_LISTA[codigo],
            "substancias": substancias,
            "adendo": adendo,
        }
        print(f"   {codigo}: {len(substancias)} substância(s)")

    if avisos:
        print("   Avisos:")
        for a in avisos:
            print(f"     - {a}")

    return listas


# ---------------------------------------------------------------------------
# Parte 2: IN vigente sobre antimicrobianos
# ---------------------------------------------------------------------------

def montar_lista_antimicrobianos():
    print("2/4 Buscando texto da IN vigente sobre antimicrobianos...")
    html_bruto = buscar(URL_IN_ANTIMICROBIANOS)
    texto = limpar_html(html_bruto)

    m = re.search(r'p[aá]g\.\s*\d+[,:]?(.*?)§\s*1º\s*Esta lista', texto, re.DOTALL | re.IGNORECASE)
    if not m:
        raise RuntimeError(
            "Não encontrei o bloco esperado (entre 'pág. XX:' e '§ 1º Esta lista') "
            "-- confira se o formato da norma mudou."
        )

    bloco = m.group(1).strip()
    itens = re.split(r'\d+\s*[-.]\s*', bloco)
    itens = [i.strip().rstrip(';,.').strip() for i in itens if i.strip()]
    itens = [re.sub(r',\s*e$', '', i, flags=re.IGNORECASE).strip() for i in itens]
    itens = [i for i in itens if i]

    print(f"   ANTIMICROBIANO: {len(itens)} substância(s)")

    return {
        "titulo": "Antimicrobianos de uso sob prescrição (IN 360/2025)",
        "regra": REGRA_ANTIMICROBIANO,
        "substancias": itens,
        "adendo": (
            "Lista não se aplica a antimicrobianos de uso exclusivo hospitalar. "
            "Receita válida por 10 dias a contar da emissão; dispensação mediante "
            "retenção da 2ª via, devolvendo a 1ª via ao paciente."
        ),
    }


# ---------------------------------------------------------------------------
# Parte 3: fusão com curadoria manual + diff contra o estado anterior
# ---------------------------------------------------------------------------

def carregar_json_opcional(caminho: Path, rotulo: str, vazio):
    if caminho.exists():
        dados = json.loads(caminho.read_text(encoding="utf-8"))
        print(f"3/4 {rotulo}: {len(dados)} entrada(s) encontrada(s) em {caminho.name}")
        return dados
    print(f"3/4 Aviso: {caminho.name} não encontrado -- seguindo sem {rotulo.lower()}.")
    return vazio


def mostrar_diff(anterior: dict, novo: dict):
    if not anterior:
        print("4/4 Não havia controlados.json anterior para comparar -- primeira captura.")
        return

    listas_antes = anterior.get("listas", {})
    listas_depois = novo.get("listas", {})
    mudou_algo = False

    for codigo in sorted(set(listas_antes) | set(listas_depois)):
        antes = set(listas_antes.get(codigo, {}).get("substancias", []))
        depois = set(listas_depois.get(codigo, {}).get("substancias", []))
        adicionadas = depois - antes
        removidas = antes - depois
        if adicionadas or removidas:
            mudou_algo = True
            print(f"4/4 ⚠️  MUDANÇA em {codigo}:")
            for s in sorted(adicionadas):
                print(f"       + {s}")
            for s in sorted(removidas):
                print(f"       - {s}")

    if not mudou_algo:
        print("4/4 Sem mudanças nas listas, em relação à última captura (controlados.json atual).")


def main():
    pasta = Path(__file__).parent
    caminho_saida = pasta / "controlados.json"

    anterior = {}
    if caminho_saida.exists():
        anterior = json.loads(caminho_saida.read_text(encoding="utf-8"))

    listas = montar_listas_portaria()
    listas["ANTIMICROBIANO"] = montar_lista_antimicrobianos()

    detalhes = carregar_json_opcional(pasta / "detalhes_farmacologicos.json", "Detalhes farmacológicos", {})
    excecoes = carregar_json_opcional(pasta / "excecoes.json", "Exceções de adendo", {})

    saida = {
        "_aviso": "Gerado automaticamente a partir da Portaria 344/98 e da IN vigente sobre antimicrobianos. Conferir contra o texto oficial antes de publicar mudanças.",
        "_fonte_controlados": URL_PORTARIA_344,
        "_fonte_antimicrobianos": URL_IN_ANTIMICROBIANOS,
        "_capturado_em": date.today().isoformat(),
        "listas": listas,
        "detalhes": detalhes,
        "excecoes": excecoes,
    }

    mostrar_diff(anterior, saida)

    caminho_saida.write_text(json.dumps(saida, ensure_ascii=False, indent=2), encoding="utf-8")

    total = sum(len(v["substancias"]) for v in listas.values())
    print(f"\nSalvo: {caminho_saida.name}")
    print(f"Listas: {len(listas)} | Substâncias: {total} | Detalhes curados: {len(detalhes)} | Exceções: {len(excecoes)}")
    print("\nProximo passo: python3 gerar_marcas.py (opcional) e depois python3 atualizar_pagina.py")


if __name__ == "__main__":
    main()
