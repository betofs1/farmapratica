# -*- coding: utf-8 -*-
"""
gerar_marcas.py

Cruza o banco CMED/ANVISA (medicamentos.json, o mesmo usado no módulo
Equivalentes) com as substâncias controladas/antimicrobianas já estruturadas
em controlados.json, gerando marcas.json: um mapa compacto de
nome comercial -> substância rastreada (com o código da lista).

Só entram marcas cujo princípio ativo bate com uma das substâncias já
presentes no controlados.json -- ou seja, medicamentos "comuns" (não
controlados) NÃO entram aqui, porque não têm nenhuma informação de receita/
retenção pra mostrar na página.

Uso:
    python3 gerar_marcas.py

Requer:
    controlados.json    (gerado pelo atualizar_fontes.py, nesta mesma pasta)
    medicamentos.json   (export CMED, usado também pelo módulo Equivalentes --
                         procurado primeiro nesta pasta e, se não encontrado,
                         em ../medinter/medicamentos.json, para não precisar
                         copiar o arquivo manualmente a cada atualização)

Gera:
    marcas.json
"""

import json
import re
import unicodedata
from pathlib import Path


def normaliza(texto: str) -> str:
    """minúsculas, sem acento, sem pontuação -- para comparação robusta."""
    texto = texto.strip().lower()
    texto = unicodedata.normalize('NFD', texto)
    texto = ''.join(c for c in texto if unicodedata.category(c) != 'Mn')
    texto = re.sub(r'[^a-z0-9\s]', ' ', texto)
    texto = re.sub(r'\s+', ' ', texto).strip()
    return texto


def gerar_candidatos(nome_oficial: str):
    """
    Gera variações plausíveis de um nome de substância da Portaria 344/98
    para bater com o jeito mais "comum" que o CMED costuma escrever
    (ex.: "Ftalimidoglutarimida (talidomida)" -> também tenta "talidomida").
    """
    candidatos = {nome_oficial}

    m = re.match(r'^(.*?)\s*\((.*?)\)\s*$', nome_oficial)
    if m:
        antes, dentro = m.groups()
        candidatos.add(antes.strip())
        candidatos.add(dentro.strip())

    novos = set()
    for c in list(candidatos):
        if re.search(r'\bou\b', c, flags=re.IGNORECASE):
            partes = re.split(r'\s+ou\s+', c, flags=re.IGNORECASE)
            novos.update(p.strip() for p in partes)
    candidatos.update(novos)

    return {normaliza(c) for c in candidatos if len(normaliza(c)) > 2}


def localizar_medicamentos_json(pasta: Path):
    candidato_local = pasta / "medicamentos.json"
    if candidato_local.exists():
        return candidato_local
    candidato_medinter = pasta.parent / "medinter" / "medicamentos.json"
    if candidato_medinter.exists():
        return candidato_medinter
    return None


def main():
    pasta = Path(__file__).parent
    caminho_controlados = pasta / "controlados.json"
    caminho_meds = localizar_medicamentos_json(pasta)

    if caminho_meds is None:
        print("Não encontrei medicamentos.json nesta pasta nem em ../medinter/ -- "
              "copie o export CMED aqui, ou confira o caminho do módulo Equivalentes.")
        return
    if not caminho_controlados.exists():
        print("Não encontrei controlados.json nesta pasta -- rode o atualizar_fontes.py antes.")
        return

    print(f"Usando medicamentos.json em: {caminho_meds}")
    meds = json.loads(caminho_meds.read_text(encoding="utf-8"))["medicamentos"]
    controlados = json.loads(caminho_controlados.read_text(encoding="utf-8"))["listas"]

    # Monta o índice: candidato normalizado -> (nome oficial da substância, código da lista)
    indice = {}
    for codigo, lista in controlados.items():
        for substancia in lista["substancias"]:
            for candidato in gerar_candidatos(substancia):
                # Em caso de colisão, mantém o primeiro (evita sobrescrever silenciosamente)
                indice.setdefault(candidato, (substancia, codigo))

    total_substancias = sum(len(l["substancias"]) for l in controlados.values())
    print(f"Índice de busca: {len(indice)} variações de nome, cobrindo {total_substancias} substâncias.")

    marcas = {}
    substancias_encontradas = set()

    # Um único regex compilado com todas as variações, em vez de checar
    # candidato por candidato em laço (dezenas de milhares de medicamentos x
    # centenas de variações ficaria lento demais). Ordena do mais longo pro
    # mais curto para que "acido clavulanico" não seja ofuscado por um
    # candidato mais genérico.
    candidatos_ordenados = sorted(indice.keys(), key=len, reverse=True)
    padrao = re.compile(r'\b(' + '|'.join(re.escape(c) for c in candidatos_ordenados) + r')\b')

    for med in meds:
        principio_bruto = med.get("principio", "")
        if not principio_bruto:
            continue
        ingredientes = [p.strip() for p in principio_bruto.split(";") if p.strip()]

        for ingrediente in ingredientes:
            ingrediente_norm = normaliza(ingrediente)
            m = padrao.search(ingrediente_norm)
            if not m:
                continue

            substancia_oficial, codigo = indice[m.group(1)]
            nome_marca = med["nome"].strip()
            if normaliza(nome_marca) == ingrediente_norm:
                continue  # é o próprio nome genérico do princípio ativo, não uma marca
            marcas[nome_marca] = {"substancia": substancia_oficial, "codigo": codigo}
            substancias_encontradas.add(substancia_oficial)
            break

    saida = {
        "_aviso": "Gerado cruzando o CMED/ANVISA com as substâncias controladas/antimicrobianas do controlados.json. Cobre só marcas cujo princípio ativo é uma substância rastreada nesta consulta.",
        "_total_marcas": len(marcas),
        "_total_substancias_com_marca": len(substancias_encontradas),
        "marcas": marcas,
    }

    (pasta / "marcas.json").write_text(json.dumps(saida, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"\nMarcas encontradas: {len(marcas)}")
    print(f"Substâncias rastreadas com pelo menos 1 marca: {len(substancias_encontradas)} de {total_substancias}")
    print("Salvo: marcas.json")
    print("\nProximo passo: python3 atualizar_pagina.py")


if __name__ == "__main__":
    main()
