# -*- coding: utf-8 -*-
"""
atualizar_pagina.py

Injeta controlados.json + marcas.json direto no index.html real da
ferramenta -- substituindo o conteúdo dos dois blocos
<script type="application/json" id="dados-controlados"> e
id="dados-marcas"> que já existem na página publicada.

Substitui o antigo gerar_pagina.py + template_consulta.html (um arquivo de
template HTML separado, mantido à parte da página real e sujeito a ficar
desatualizado em relação a ela). Aqui não existe template: o próprio
index.html em produção é editado no lugar, com backup automático e
verificação de que o restante do arquivo não foi alterado.

Uso:
    python3 atualizar_pagina.py

Requer, nesta mesma pasta:
    controlados.json   (gerado pelo atualizar_fontes.py)
    marcas.json         (gerado pelo gerar_marcas.py)
    index.html          (a página real da ferramenta)

Efeito:
    Reescreve index.html em produção com os dados novos.
    Guarda uma cópia de segurança em index.html.bak antes de alterar
    (sobrescrevendo um .bak de uma rodada anterior).
"""

import json
import re
from pathlib import Path

MARCADOR_CONTROLADOS = "dados-controlados"
MARCADOR_MARCAS = "dados-marcas"

PADRAO_BLOCO = (
    r'(<script type="application/json" id="{id}">)(.*?)(</script>)'
)


def montar_bloco_controlados(controlados: dict) -> dict:
    """
    Remonta controlados.json (formato de trabalho do atualizar_fontes.py,
    com _fonte_controlados/_fonte_antimicrobianos separados) no formato que
    a página realmente espera (_fonte único -- não é lido pelo JS da
    página, é só informativo, então o formato exato não quebra nada, mas
    mantemos compatível com o que já está publicado).
    """
    return {
        "_aviso": controlados.get(
            "_aviso",
            "Gerado automaticamente a partir da Portaria 344/98 e da IN vigente "
            "sobre antimicrobianos. Conferir contra o texto oficial antes de "
            "publicar mudanças.",
        ),
        "_fonte": {
            "portaria_344_98": controlados.get("_fonte_controlados", ""),
            "in_antimicrobianos": controlados.get("_fonte_antimicrobianos", ""),
        },
        "_capturado_em": controlados.get("_capturado_em", ""),
        "listas": controlados.get("listas", {}),
        "detalhes": controlados.get("detalhes", {}),
        "excecoes": controlados.get("excecoes", {}),
    }


def extrair_bloco(html: str, id_bloco: str) -> str:
    padrao = re.compile(PADRAO_BLOCO.format(id=id_bloco), re.DOTALL)
    m = padrao.search(html)
    if not m:
        raise RuntimeError(
            f'Não encontrei o bloco <script type="application/json" id="{id_bloco}"> '
            f"no index.html -- confira se a página mudou de estrutura antes de prosseguir."
        )
    return m.group(2)


def substituir_bloco(html: str, id_bloco: str, novo_json_texto: str) -> str:
    padrao = re.compile(PADRAO_BLOCO.format(id=id_bloco), re.DOTALL)
    m = padrao.search(html)
    if not m:
        raise RuntimeError(
            f'Não encontrei o bloco <script type="application/json" id="{id_bloco}"> '
            f"no index.html -- confira se a página mudou de estrutura antes de prosseguir."
        )
    novo_bloco = m.group(1) + "\n" + novo_json_texto + "\n" + m.group(3)
    return html[: m.start()] + novo_bloco + html[m.end() :]


def contar(dados_controlados: dict) -> dict:
    listas = dados_controlados.get("listas", {})
    return {
        "listas": len(listas),
        "substancias": sum(len(v.get("substancias", [])) for v in listas.values()),
        "detalhes": len(dados_controlados.get("detalhes", {})),
        "excecoes": len(dados_controlados.get("excecoes", {})),
    }


def main():
    pasta = Path(__file__).parent
    caminho_controlados = pasta / "controlados.json"
    caminho_marcas = pasta / "marcas.json"
    caminho_pagina = pasta / "index.html"
    caminho_backup = pasta / "index.html.bak"

    for rotulo, caminho in [
        ("controlados.json", caminho_controlados),
        ("marcas.json", caminho_marcas),
        ("index.html", caminho_pagina),
    ]:
        if not caminho.exists():
            print(f"Não encontrei {rotulo} nesta pasta -- rode o passo anterior antes.")
            return

    controlados_bruto = json.loads(caminho_controlados.read_text(encoding="utf-8"))

    # Trava de segurança: a curadoria publicada tem que ser a mesma de
    # excecoes.json E tem que conferir com o texto de adendo capturado.
    caminho_excecoes = pasta / "excecoes.json"
    if caminho_excecoes.exists():
        excecoes_arquivo = json.loads(caminho_excecoes.read_text(encoding="utf-8"))
        if excecoes_arquivo != controlados_bruto.get("excecoes", {}):
            print("ABORTADO: excecoes.json foi editado depois do último atualizar_fontes.py. "
                  "Rode 'python3 atualizar_fontes.py --sem-rede' antes. Nada foi gravado.")
            return
    from atualizar_fontes import validar_excecoes, relatar_validacao
    erros, avisos = validar_excecoes(controlados_bruto.get("listas", {}), controlados_bruto.get("excecoes", {}))
    if not relatar_validacao(erros, avisos):
        print("ABORTADO: exceções inconsistentes com a norma capturada. Nada foi gravado.")
        return
    print()
    marcas = json.loads(caminho_marcas.read_text(encoding="utf-8"))
    html_original = caminho_pagina.read_text(encoding="utf-8")

    dados_controlados_final = montar_bloco_controlados(controlados_bruto)

    # Estado atual da página (antes de alterar), para mostrar o antes/depois.
    try:
        bloco_antigo = json.loads(extrair_bloco(html_original, MARCADOR_CONTROLADOS))
        contagem_antes = contar(bloco_antigo)
    except Exception:
        bloco_antigo = None
        contagem_antes = None

    try:
        marcas_antigo = json.loads(extrair_bloco(html_original, MARCADOR_MARCAS))
        total_marcas_antes = marcas_antigo.get("_total_marcas", "?")
    except Exception:
        total_marcas_antes = "?"

    texto_controlados = json.dumps(dados_controlados_final, ensure_ascii=False, indent=2)
    texto_marcas = json.dumps(marcas, ensure_ascii=False, indent=2)

    html_novo = substituir_bloco(html_original, MARCADOR_CONTROLADOS, texto_controlados)
    html_novo = substituir_bloco(html_novo, MARCADOR_MARCAS, texto_marcas)

    # Verificação ANTES de gravar: tudo fora dos dois blocos tem que ficar
    # byte-a-byte igual. Faz isso recortando os dois blocos de cada versão e
    # comparando o que resta.
    def remover_blocos(html: str) -> str:
        for id_bloco in (MARCADOR_CONTROLADOS, MARCADOR_MARCAS):
            padrao = re.compile(PADRAO_BLOCO.format(id=id_bloco), re.DOTALL)
            html = padrao.sub(r"\1\3", html)
        return html

    resto_antes = remover_blocos(html_original)
    resto_depois = remover_blocos(html_novo)
    if resto_antes != resto_depois:
        print(
            "ABORTADO: o restante da página (fora dos dois blocos de dados) mudaria "
            "com esta operação -- isso não deveria acontecer. Nada foi gravado. "
            "Avise antes de prosseguir."
        )
        return

    # Verificação de que os dois blocos novos são JSON válido e recuperável
    # (reler exatamente o que vai pro arquivo, não só o dict em memória).
    bloco_controlados_novo = json.loads(extrair_bloco(html_novo, MARCADOR_CONTROLADOS))
    bloco_marcas_novo = json.loads(extrair_bloco(html_novo, MARCADOR_MARCAS))
    contagem_depois = contar(bloco_controlados_novo)

    # Backup antes de gravar (sobrescreve o .bak de uma rodada anterior).
    caminho_backup.write_text(html_original, encoding="utf-8")

    caminho_pagina.write_text(html_novo, encoding="utf-8")

    # Verificação FINAL: reabre o arquivo gravado em disco (não o que ficou em
    # memória) e confere que é idêntico ao que se pretendia gravar.
    html_relido = caminho_pagina.read_text(encoding="utf-8")
    if html_relido != html_novo:
        print(
            "AVISO: o arquivo gravado em disco não ficou idêntico ao esperado -- "
            "restaurando o backup por segurança."
        )
        caminho_pagina.write_text(html_original, encoding="utf-8")
        return

    print(f"Backup salvo em: {caminho_backup.name}")
    print(f"Página atualizada: {caminho_pagina.name}\n")

    if contagem_antes:
        print(f"Listas:       {contagem_antes['listas']} -> {contagem_depois['listas']}")
        print(f"Substâncias:  {contagem_antes['substancias']} -> {contagem_depois['substancias']}")
        print(f"Detalhes:     {contagem_antes['detalhes']} -> {contagem_depois['detalhes']}")
        print(f"Exceções:     {contagem_antes['excecoes']} -> {contagem_depois['excecoes']}")
    else:
        print(f"Listas:       {contagem_depois['listas']}")
        print(f"Substâncias:  {contagem_depois['substancias']}")
        print(f"Detalhes:     {contagem_depois['detalhes']}")
        print(f"Exceções:     {contagem_depois['excecoes']}")
    print(f"Marcas:       {total_marcas_antes} -> {bloco_marcas_novo.get('_total_marcas', '?')}")

    print(
        "\nConfira a página no navegador antes de publicar (git add/commit/push). "
        "Se algo ficou errado, restaure o backup: cp index.html.bak index.html"
    )


if __name__ == "__main__":
    main()
