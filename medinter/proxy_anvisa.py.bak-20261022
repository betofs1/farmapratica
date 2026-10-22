"""
FarmaDesk — Proxy CMED/ANVISA
================================
Baixa a tabela oficial de medicamentos da CMED (ANVISA) e serve buscas
localmente via API REST com headers CORS para uso pelo farma_equivalentes.html.

COMO USAR:
  pip install flask requests pandas xlrd openpyxl 
  python proxy_anvisa.py

  Atualizar base manualmenteee:
  python proxy_anvisa.py --atualizar

A página farma_equivalentes.html usa http://localhost:5000
"""

import sys
import os
import json
import time
import argparse
import re
import threading
import unicodedata
from pathlib import Path
from datetime import datetime

# ── Dependências opcionais com mensagem amigável ───────────────────────────────
try:
    from flask import Flask, request, jsonify
    import requests
    import pandas as pd
except ImportError as e:
    print(f"\n  ERRO: Dependência ausente — {e}")
    print("  Execute: pip install flask requests pandas xlrd openpyxl\n")
    sys.exit(1)

# ── Config ─────────────────────────────────────────────────────────────────────
PORTA       = 5000
CACHE_DIR   = Path(__file__).parent / "cmed_cache"
CACHE_JSON  = CACHE_DIR / "medicamentos.json"
CACHE_META  = CACHE_DIR / "meta.json"
MAX_CACHE_DAYS = 30   # atualiza automaticamente após 30 dias

# URLs candidatas da CMED (tenta em ordem até encontrar uma válida)
# O padrão é: xls_conformidade_site_AAAAMMDD_XXXXXXXX-N.xls
# A ANVISA publica mensalmente; tentamos os últimos 3 meses
def gerar_urls_cmed():
    from datetime import date
    from calendar import monthrange
    urls = []
    hoje = date.today()
    for delta_mes in range(0, 4):
        mes = hoje.month - delta_mes
        ano = hoje.year
        if mes <= 0:
            mes += 12
            ano -= 1
        # Padrões conhecidos de URL
        aamm = f"{ano}{mes:02d}"
        base = "https://www.gov.br/anvisa/pt-br/assuntos/medicamentos/cmed/precos/arquivos"
        urls += [
            f"{base}/xls_conformidade_site_{aamm}01_conformidade-1.xls",
            f"{base}/xls_conformidade_site_{aamm}20_conformidade-1.xls",
            f"{base}/conformidade_pmc_{ano}_{mes:02d}.xls",
            f"{base}/conformidade_gov_{ano}.xls",
        ]
    # URLs históricas conhecidas como fallback
    urls += [
        "https://www.gov.br/anvisa/pt-br/assuntos/medicamentos/cmed/precos/arquivos/xls_conformidade_site_20230320_19585047-1.xls",
    ]
    return urls

# ── Normalização ───────────────────────────────────────────────────────────────
def normalizar_str(s):
    if not isinstance(s, str):
        s = str(s) if s and str(s) != 'nan' else ""
    return unicodedata.normalize("NFD", s).encode("ascii", "ignore").decode().lower().strip()

def tipo_produto(raw):
    r = normalizar_str(raw)
    if "refer" in r:       return "referencia"
    if "generi" in r:      return "generico"
    if "simil" in r:       return "similar"
    if "biolog" in r:      return "biologico"
    if "fitote" in r:      return "fitoterapico"
    if "dinamiz" in r:     return "homeopatico"
    return "outros"

def fmt_preco(val):
    try:
        f = float(str(val).replace(",", "."))
        return f"R$ {f:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except:
        return None

# ── Download e parse da CMED ───────────────────────────────────────────────────
def baixar_cmed(forcar=False):
    CACHE_DIR.mkdir(exist_ok=True)

    # Verifica cache válido (sem forçar)
    if not forcar and CACHE_JSON.exists() and CACHE_META.exists():
        meta = json.loads(CACHE_META.read_text())
        idade_dias = (time.time() - meta.get("ts", 0)) / 86400
        if idade_dias < MAX_CACHE_DAYS:
            print(f"  Cache válido ({idade_dias:.0f} dias). Use --atualizar para forçar.")
            return True

    # ── PRIORIDADE 1: arquivo local na pasta cmed_cache ───────────────────────
    # Procura pelo arquivo mais recente (maior data de modificação)
    xls_local = None
    candidatos = []
    for ext in [".xlsx", ".xls"]:
        for p in CACHE_DIR.glob(f"*{ext}"):
            candidatos.append(p)
    if candidatos:
        # Ordena pelo mais recente
        xls_local = sorted(candidatos, key=lambda p: p.stat().st_mtime, reverse=True)[0]
        print(f"  Arquivo local encontrado: {xls_local.name}")
        print(f"  Usando arquivo local (sem tentar download).")
        return parsear_xls(xls_local)

    # ── PRIORIDADE 2: tenta download automático ───────────────────────────────
    print("  Nenhum arquivo local encontrado. Tentando download...")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "*/*",
    }

    xls_path = None
    for url in gerar_urls_cmed():
        try:
            print(f"  Tentando: {url.split('/')[-1]}")
            r = requests.get(url, headers=headers, timeout=30, allow_redirects=True)
            if r.status_code == 200 and len(r.content) > 10000:
                ext = ".xlsx" if r.content[:4] == b"PK" else ".xls"
                xls_path = CACHE_DIR / f"conformidade{ext}"
                xls_path.write_bytes(r.content)
                print(f"  Download OK: {len(r.content)/1024:.0f} KB ({ext})")
                return parsear_xls(xls_path)
        except Exception:
            continue

    print()
    print("  ATENÇÃO: Nenhum arquivo encontrado.")
    print("  Coloque o arquivo XLS/XLSX baixado da ANVISA dentro da pasta cmed_cache/")
    print("  Site: https://www.gov.br/anvisa/pt-br/assuntos/medicamentos/cmed/precos")
    print("  Depois rode novamente: python proxy_anvisa.py --atualizar")
    return False

def parsear_xls(xls_path):
    ext = xls_path.suffix.lower()
    print(f"  Processando {ext.upper()}...")
    try:
        # ── Lê planilha conforme extensão ────────────────────────────────────
        if ext == ".xlsx":
            from openpyxl import load_workbook as _lw
            wb = _lw(str(xls_path), read_only=True, data_only=True)
            ws = wb.active
            rows_raw = list(ws.iter_rows(values_only=True))
        else:
            import xlrd as _xlrd
            wb2 = _xlrd.open_workbook(str(xls_path))
            ws2 = wb2.sheet_by_index(0)
            rows_raw = [[ws2.cell_value(r,c) for c in range(ws2.ncols)] for r in range(ws2.nrows)]

        print(f"  Planilha: {len(rows_raw)} linhas")

        # ── Extrai data de publicação (linha com "Publicada em") ──────────────
        data_publicacao = None
        for row in rows_raw[:10]:
            for v in row:
                if v and "Publicada" in str(v):
                    m = re.search(r"(\d{2}/\d{2}/\d{4})", str(v))
                    if m:
                        data_publicacao = m.group(1)
                        print(f"  Data CMED: {data_publicacao}")
                        break
            if data_publicacao:
                break
        if not data_publicacao:
            data_publicacao = datetime.now().strftime("%d/%m/%Y")
            print(f"  Data não encontrada, usando hoje: {data_publicacao}")

        # ── Encontra cabeçalho ────────────────────────────────────────────────
        header_row_idx = None
        header = []
        for i, row in enumerate(rows_raw):
            vals = [str(v).strip() if v is not None else "" for v in row]
            filled = sum(1 for v in vals if v and v != "nan")
            if filled >= 10:
                header_row_idx = i
                header = vals
                print(f"  Cabeçalho na linha {i}: {header[:5]}")
                break

        if header_row_idx is None:
            print("  ERRO: cabeçalho não encontrado.")
            return False

        # ── Mapeia colunas ────────────────────────────────────────────────────
        def col_idx(keywords):
            for kw in keywords:
                kw_n = unicodedata.normalize("NFD", kw.upper()).encode("ascii","ignore").decode()
                for i, h in enumerate(header):
                    h_n = unicodedata.normalize("NFD", h.upper()).encode("ascii","ignore").decode()
                    if kw_n in h_n:
                        return i
            return None

        c_subst  = col_idx(["SUBSTANCIA","SUBSTÂNCIA"])
        c_lab    = col_idx(["LABORATORIO","LABORATÓRIO"])
        c_prod   = col_idx(["PRODUTO"])
        c_apres  = col_idx(["APRESENTACAO","APRESENTAÇÃO"])
        c_classe = col_idx(["CLASSE"])
        c_tipo   = col_idx(["TIPO"])
        c_tarja  = col_idx(["TARJA"])
        c_reg    = col_idx(["REGISTRO"])
        c_pf     = col_idx(["PF SEM","PF 0%","PF 0"])
        c_pmc    = col_idx(["PMC 0%","PMC 0"])
        c_restr  = col_idx(["HOSPITALAR","RESTRICAO","RESTRIÇÃO"])

        print(f"  Índices: subst={c_subst} lab={c_lab} prod={c_prod} tipo={c_tipo} pf={c_pf} pmc={c_pmc}")

        # ── Processa linhas de dados ──────────────────────────────────────────
        medicamentos = []
        for row in rows_raw[header_row_idx + 1:]:
            def v(idx):
                if idx is None: return ""
                val = row[idx] if idx < len(row) else None
                return str(val).strip() if val is not None else ""

            subst = v(c_subst)
            prod  = v(c_prod)
            if not subst or not prod or subst == "nan" or prod == "nan":
                continue

            medicamentos.append({
                "nome":        prod,
                "principio":   subst,
                "laboratorio": v(c_lab),
                "apresentacao":v(c_apres),
                "tipo":        tipo_produto(v(c_tipo)),
                "classe":      v(c_classe),
                "tarja":       v(c_tarja).replace("(**)", "").replace("(*)", "").strip(),
                "registro":    v(c_reg),
                "situacao":    "ativo",
                "pf":          fmt_preco(v(c_pf)),
                "pmc":         fmt_preco(v(c_pmc)),
                "hospitalar":  "sim" in v(c_restr).lower() if c_restr else False,
            })

        print(f"  {len(medicamentos)} medicamentos indexados.")

        # ── Salva no formato { _meta, medicamentos: [] } ─────────────────────
        output = {
            "_meta": {
                "versao": "1.0",
                "data_atualizacao": data_publicacao,
                "fonte": "CMED/ANVISA — Câmara de Regulação do Mercado de Medicamentos",
                "total": len(medicamentos),
                "arquivo": xls_path.name,
                "processado_em": datetime.now().strftime("%d/%m/%Y %H:%M"),
            },
            "medicamentos": medicamentos,
        }

        CACHE_JSON.write_text(json.dumps(output, ensure_ascii=False, separators=(",",":")), encoding="utf-8")
        CACHE_META.write_text(json.dumps({
            "ts":    time.time(),
            "total": len(medicamentos),
            "data":  data_publicacao,
            "fonte": xls_path.name,
        }), encoding="utf-8")
        print(f"  Cache salvo: {CACHE_JSON}")
        print(f"  Data CMED gravada: {data_publicacao}")
        return True

    except Exception as e:
        print(f"  ERRO ao processar: {e}")
        import traceback; traceback.print_exc()
        return False

# ── Carrega dados em memória ───────────────────────────────────────────────────
DB = []
META = {}

def carregar_db():
    global DB, META
    if CACHE_JSON.exists():
        payload = json.loads(CACHE_JSON.read_text(encoding="utf-8"))
        if isinstance(payload, list):
            DB = payload
        else:
            DB = payload.get("medicamentos", [])
            if "_meta" in payload:
                META.update(payload["_meta"])
                META["total"] = len(DB)
        if CACHE_META.exists():
            META.update(json.loads(CACHE_META.read_text()))
        print(f"  Base carregada: {len(DB)} medicamentos ({META.get('data','?')})")
        return True
    return False

# ── Flask App ─────────────────────────────────────────────────────────────────
app = Flask(__name__)

@app.after_request
def cors(resp):
    resp.headers["Access-Control-Allow-Origin"]  = "*"
    resp.headers["Access-Control-Allow-Headers"] = "Content-Type"
    resp.headers["Access-Control-Allow-Methods"] = "GET,OPTIONS"
    return resp

@app.route("/status")
def status():
    return jsonify({
        "status":  "ok",
        "servico": "FarmaDesk CMED Proxy",
        "versao":  "2.0",
        "base":    META.get("data", "não carregada"),
        "total":   len(DB),
    })

@app.route("/anvisa/medicamentos")
def buscar():
    if not DB:
        return jsonify({"erro": "Base CMED não carregada. Reinicie o proxy."}), 503

    q     = normalizar_str(request.args.get("q", ""))
    tipo  = request.args.get("tipo", "")
    count = min(int(request.args.get("count", "100")), 500)

    if not q or len(q) < 2:
        return jsonify({"erro": "Parâmetro 'q' muito curto"}), 400

    # Tokeniza a query (ex: "diosmina hesperidina" ou "diosmina + hesperidina")
    termos = [t for t in re.split(r"[\s+,]+", q) if len(t) >= 3]

    resultados = []
    for med in DB:
        haystack = normalizar_str(
            med["nome"] + " " + med["principio"] + " " + med["laboratorio"]
        )
        if all(t in haystack for t in termos):
            if not tipo or med["tipo"] == tipo:
                resultados.append(med)
        if len(resultados) >= count:
            break

    # Ordena: referência > genérico > similar > outros
    ordem = ["referencia", "generico", "similar", "biologico", "fitoterapico", "homeopatico", "outros"]
    resultados.sort(key=lambda m: ordem.index(m["tipo"]) if m["tipo"] in ordem else 99)

    return jsonify({
        "fonte":      "cmed",
        "query":      q,
        "total":      len(resultados),
        "base_data":  META.get("data", "?"),
        "resultados": resultados,
    })

@app.route("/anvisa/sugestoes")
def sugestoes():
    if not DB:
        return jsonify([])
    q = normalizar_str(request.args.get("q", ""))
    if len(q) < 2:
        return jsonify([])
    vistos = set()
    res = []
    for med in DB:
        p = med["principio"]
        pn = normalizar_str(p)
        if q in pn and p not in vistos:
            vistos.add(p)
            res.append(p)
        if len(res) >= 8:
            break
    return jsonify(res)

@app.route("/")
def index():
    total = len(DB)
    data  = META.get("data", "não disponível")
    return f"""<html><body style="font-family:sans-serif;background:#0a1628;color:#e2e8f0;padding:40px">
    <h2 style="color:#60a5fa">FarmaDesk — Proxy CMED v2.0</h2>
    <p style="color:#94a3b8">Base: <strong style="color:#34d399">{total:,} medicamentos</strong> · Atualizado em {data}</p>
    <hr style="border-color:#1e3254;margin:20px 0">
    <p style="color:#64748b;font-size:13px">Endpoints:</p>
    <code style="color:#34d399">/anvisa/medicamentos?q=diosmina</code><br><br>
    <code style="color:#34d399">/anvisa/medicamentos?q=diosmina+hesperidina&tipo=referencia</code><br><br>
    <code style="color:#34d399">/anvisa/sugestoes?q=dio</code><br><br>
    <code style="color:#34d399">/status</code>
    <hr style="border-color:#1e3254;margin:20px 0">
    <p style="color:#64748b;font-size:12px">Fonte: Tabela CMED/ANVISA — Câmara de Regulação do Mercado de Medicamentos</p>
    </body></html>"""

# ── Main ───────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="FarmaDesk CMED Proxy")
    parser.add_argument("--atualizar", action="store_true", help="Força re-download da tabela CMED")
    parser.add_argument("--porta", type=int, default=PORTA, help="Porta do servidor (padrão: 5000)")
    args = parser.parse_args()

    print()
    print("  ╔══════════════════════════════════════════════╗")
    print("  ║   FarmaDesk — Proxy CMED v2.0               ║")
    print("  ╚══════════════════════════════════════════════╝")
    print()

    # Inicializa base
    if args.atualizar or not CACHE_JSON.exists():
        ok = baixar_cmed(forcar=args.atualizar)
        if not ok and not CACHE_JSON.exists():
            print()
            print("  IMPORTANTE: Baixe manualmente a tabela XLS em:")
            print("  https://www.gov.br/anvisa/pt-br/assuntos/medicamentos/cmed/precos")
            print("  Salve o arquivo como:  cmed_cache/conformidade.xls")
            print("  E execute novamente:   python proxy_anvisa.py --atualizar")
            print()
            sys.exit(1)

    carregar_db()

    if not DB:
        print("  ERRO: Base vazia. Execute: python proxy_anvisa.py --atualizar")
        sys.exit(1)

    porta = args.porta
    print()
    print(f"  Servidor ativo em http://localhost:{porta}")
    print(f"  Base: {len(DB):,} medicamentos")
    print(f"  Ctrl+C para encerrar")
    print()

    app.run(host="127.0.0.1", port=porta, debug=False)
