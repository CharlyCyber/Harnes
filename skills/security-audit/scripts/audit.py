#!/usr/bin/env python3
"""
security-audit — verificación automatizada de los puntos medibles del
checklist de 19 puntos para webs vibecodeadas.

Uso:
    python audit.py RUTA [--url https://sitio.com]

Exit codes: 0 = sin FAIL, 1 = al menos un FAIL, 2 = error fatal.
Stdlib de Python únicamente (sin dependencias externas).
"""

from __future__ import annotations

import argparse
import base64
import json
import re
import shutil
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

MAX_FILE_BYTES = 1_000_000
MAX_SCAN_BYTES = 80_000_000
MAX_EXAMPLES = 5
HISTORY_COMMITS = 100

SELF = Path(__file__).resolve()

SECRET_PATTERNS = [
    ("OpenAI", re.compile(r"sk-[A-Za-z0-9]{20,}")),
    ("GitHub", re.compile(r"ghp_[A-Za-z0-9]{36}|github_pat_[A-Za-z0-9_]{22,}")),
    ("AWS", re.compile(r"AKIA[0-9A-Z]{16}")),
    ("Google", re.compile(r"AIza[0-9A-Za-z_\-]{35}")),
    ("Slack", re.compile(r"xox[baprs]-[A-Za-z0-9-]{10,}")),
    ("PrivateKey", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----")),
    ("JWT", re.compile(r"eyJ[A-Za-z0-9_\-]{8,}\.[A-Za-z0-9_\-]{8,}\.[A-Za-z0-9_\-]{8,}")),
]

ENV_NAME_RE = re.compile(r"^\.env($|\.)")
ENV_EXAMPLE_OK = (".env.example", ".env.sample", ".env.template", ".env.dist")

LOG_RE = re.compile(
    r"(?:console\.log|print|logger\.(?:info|debug|warn)|\blog\()[^\n]{0,160}?"
    r"(?<![\w])(?:token|apikey|api_key|secret|password|authorization)(?![\w])",
    re.I,
)

DEBUG_RE = re.compile(r"^\s*DEBUG\s*=\s*True", re.M)

ROUTE_RE = re.compile(
    r"(?:app|router|fastify|server|bp|blueprint)\s*\.\s*(?:get|post|put|delete|all)\s*"
    r"\(\s*[`'\"]/(?:api/)?(?:test|debug|dev)(?:[`'\"/?]|$)"
    r"|@app\.route\(\s*[`'\"]/(?:test|debug|dev)",
    re.I,
)

MANUAL_POINTS = [1, 5, 12, 13, 14, 15, 16, 17, 18, 19]

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

findings: list[tuple[int, str, str]] = []


def add(point: int, level: str, msg: str) -> None:
    findings.append((point, level, msg))


def run_git(root: Path, *args: str) -> subprocess.CompletedProcess | None:
    try:
        return subprocess.run(
            ["git", *args], cwd=root, capture_output=True,
            text=True, encoding="utf-8", errors="replace", timeout=60,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None


def is_repo(root: Path) -> bool:
    r = run_git(root, "rev-parse", "--is-inside-work-tree")
    return bool(r and r.returncode == 0 and r.stdout.strip() == "true")


def list_scan_files(root: Path, repo: bool) -> list[Path]:
    if repo:
        r = run_git(root, "ls-files", "-co", "--exclude-standard", "-z")
        if r and r.returncode == 0:
            return [root / p for p in r.stdout.split("\0") if p]
    out: list[Path] = []
    skip_dirs = {".git", "node_modules", ".venv", "venv", "__pycache__", ".next", "dist", "build"}
    for p in root.rglob("*"):
        if p.is_file() and not any(d in p.parts for d in skip_dirs):
            out.append(p)
    return out


def read_text(path: Path) -> str | None:
    try:
        if path == SELF or not path.is_file():
            return None
        if path.stat().st_size > MAX_FILE_BYTES:
            return None
        data = path.read_bytes()
    except OSError:
        return None
    if b"\0" in data[:8192]:
        return None
    return data.decode("utf-8", errors="replace")


def jwt_role(token: str) -> str | None:
    try:
        payload = token.split(".")[1]
        payload += "=" * (-len(payload) % 4)
        data = json.loads(base64.urlsafe_b64decode(payload))
        return data.get("role") if isinstance(data, dict) else None
    except Exception:
        return None


def rel(root: Path, path: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


# ---------------------------------------------------------------- checks

def check_env_en_git(root: Path, repo: bool) -> None:
    point = 3
    if not repo:
        add(point, "SKIP", "no es un repo git")
        return
    r = run_git(root, "ls-files", "-z")
    if not r or r.returncode != 0:
        add(point, "SKIP", "git ls-files falló")
        return
    bad = [
        f for f in r.stdout.split("\0")
        if f and ENV_NAME_RE.match(Path(f).name)
        and not any(Path(f).name.startswith(ok) for ok in ENV_EXAMPLE_OK)
    ]
    if bad:
        show = ", ".join(bad[:MAX_EXAMPLES])
        more = f" (+{len(bad) - MAX_EXAMPLES} más)" if len(bad) > MAX_EXAMPLES else ""
        add(point, "FAIL", f".env* trackeados en git: {show}{more}")
    else:
        add(point, "PASS", "ningún .env trackeado (solo plantillas)")


def check_secretos_arbol(root: Path, files: list[Path]) -> None:
    p4, p7 = 4, 7
    scanned = 0
    budget = 0
    examples: list[str] = []
    info_anon = 0
    for path in files:
        if scanned >= 50_000 or budget >= MAX_SCAN_BYTES:
            break
        text = read_text(path)
        if text is None:
            continue
        scanned += 1
        budget += len(text)
        where = rel(root, path)
        for name, pat in SECRET_PATTERNS:
            for m in pat.finditer(text):
                token = m.group(0)
                if name == "JWT":
                    role = jwt_role(token)
                    if role == "anon":
                        info_anon += 1
                        continue
                    if role == "service_role":
                        examples.append(f"{where}: Supabase service_role (SERVIDOR-ONLY)")
                    else:
                        examples.append(f"{where}: JWT no identificado ({role or 'payload ilegible'})")
                else:
                    examples.append(f"{where}: patrón {name}")
                break
            if len(examples) >= MAX_EXAMPLES + 3:
                break
        if len(examples) >= MAX_EXAMPLES + 3:
            break
    if examples:
        shown = examples[:MAX_EXAMPLES]
        rest = len(examples) - len(shown)
        msg = "; ".join(shown) + (f" (+{rest} más)" if rest > 0 else "")
        add(p4, "FAIL", f"claves sospechosas en el árbol actual: {msg}")
        add(p7, "FAIL", "si alguno de esos archivos lo sirve el frontend, la clave es pública en el navegador")
    else:
        add(p4, "PASS", "sin claves hardcodeadas detectadas")
    if info_anon:
        add(p7, "INFO", f"{info_anon} anon key de Supabase (pública por diseño, verificar que no sea service_role)")


def check_secretos_historial(root: Path, repo: bool) -> None:
    point = 5
    if not repo or not shutil.which("git"):
        add(point, "SKIP", "no es un repo git")
        return
    try:
        proc = subprocess.Popen(
            ["git", "log", "-p", "-n", str(HISTORY_COMMITS), "--no-merges"],
            cwd=root, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
            text=True, encoding="utf-8", errors="replace",
        )
    except OSError:
        add(point, "SKIP", "git log no disponible")
        return
    hits: list[str] = []
    commit, where = "", "?"
    assert proc.stdout is not None
    for line in proc.stdout:
        if line.startswith("commit "):
            commit = line.split()[1][:7]
        elif line.startswith("+++ b/"):
            where = line[6:].strip()
        elif line.startswith(("diff --git", "--- ", "+++ ", "@@")):
            continue
        else:
            for name, pat in SECRET_PATTERNS:
                if name == "JWT":
                    continue
                if pat.search(line):
                    hits.append(f"{commit}:{where}: {name}")
                    break
        if len(hits) >= MAX_EXAMPLES + 3:
            break
    proc.terminate()
    if hits:
        shown = hits[:MAX_EXAMPLES]
        rest = len(hits) - len(shown)
        add(point, "FAIL",
            f"secretos en historial (últimos {HISTORY_COMMITS} commits): "
            + "; ".join(shown) + (f" (+{rest} más)" if rest else "")
            + " → ROTAR la clave, borrar del historial y re-publicar")
    else:
        add(point, "PASS", f"sin secretos en los últimos {HISTORY_COMMITS} commits")


def check_logs(root: Path, files: list[Path]) -> None:
    point = 6
    hits: list[str] = []
    for path in files:
        if len(hits) >= MAX_EXAMPLES + 3:
            break
        if path.suffix not in {".js", ".jsx", ".ts", ".tsx", ".py", ".mjs", ".cjs", ".rb", ".php", ".go"}:
            continue
        text = read_text(path)
        if text is None:
            continue
        for i, line in enumerate(text.splitlines(), 1):
            if LOG_RE.search(line):
                hits.append(f"{rel(root, path)}:{i}")
                if len(hits) >= MAX_EXAMPLES + 3:
                    break
    if hits:
        shown = hits[:MAX_EXAMPLES]
        rest = len(hits) - len(shown)
        add(point, "WARN", "posibles secretos en logs: " + "; ".join(shown) + (f" (+{rest} más)" if rest else ""))
    else:
        add(point, "PASS", "sin logs evidentes con tokens/passwords")


def check_debug_y_rutas(root: Path, repo: bool, files: list[Path]) -> None:
    p8, p9 = 8, 9
    if repo:
        r = run_git(root, "ls-files", "*.map")
        if r and r.returncode == 0:
            maps = [m for m in r.stdout.split("\0") if m]
            dist_maps = [m for m in maps if re.search(r"(^|/)(dist|build|out)/", m)]
            if dist_maps:
                add(p8, "FAIL", f"source maps de build trackeados (info del código expuesta): {dist_maps[0]}" + (f" (+{len(dist_maps)-1} más)" if len(dist_maps) > 1 else ""))
            elif maps:
                add(p8, "WARN", f"{len(maps)} archivos .map trackeados — confirmar que no se sirven en producción")
            else:
                add(p8, "PASS", "sin source maps trackeados")
        else:
            add(p8, "SKIP", "git ls-files falló")
    else:
        add(p8, "SKIP", "no es un repo git")

    debug_hits, route_hits = [], []
    for path in files:
        if len(debug_hits) + len(route_hits) >= 2 * (MAX_EXAMPLES + 3):
            break
        text = read_text(path)
        if text is None:
            continue
        where = rel(root, path)
        if path.suffix == ".py" and len(debug_hits) < MAX_EXAMPLES + 3:
            if DEBUG_RE.search(text):
                debug_hits.append(where)
        if path.suffix in {".js", ".jsx", ".ts", ".tsx", ".py", ".mjs"} and len(route_hits) < MAX_EXAMPLES + 3:
            if ROUTE_RE.search(text):
                route_hits.append(where)
    if debug_hits:
        add(p8, "WARN", "DEBUG = True en: " + "; ".join(debug_hits[:MAX_EXAMPLES]))
    if route_hits:
        add(p9, "FAIL", "rutas de prueba/debug definidas en: " + "; ".join(route_hits[:MAX_EXAMPLES]))
    elif not repo:
        add(p9, "SKIP", "no es un repo git")
    else:
        add(p9, "PASS", "sin rutas /test o /debug evidentes")


def check_headers(url: str) -> None:
    p1, p2, p10, p11 = 1, 2, 10, 11
    req = urllib.request.Request(url, headers={"User-Agent": "security-audit/1.0"})
    try:
        resp = urllib.request.urlopen(req, timeout=15)
        code, hdrs, final = resp.status, resp.headers, resp.geturl()
    except urllib.error.HTTPError as e:
        code, hdrs, final = e.code, e.headers, url
    except Exception as e:
        add(p2, "SKIP", f"no se pudo contactar {url}: {type(e).__name__}")
        return

    if final.startswith("https://"):
        add(p2, "PASS", f"URL final https (HTTP {code})")
    else:
        add(p2, "FAIL", f"servido por HTTP sin TLS: {final}")

    server = (hdrs.get("Server") or "").lower()
    if hdrs.get("cf-ray") or "cloudflare" in server:
        add(p1, "PASS", "Cloudflare detectado (cf-ray)")
    else:
        add(p1, "WARN", "sin cabeceras de Cloudflare — poner el proxy delante")

    missing, present = [], []
    (present if hdrs.get("Content-Security-Policy") else missing).append("CSP")
    (present if hdrs.get("Strict-Transport-Security") else missing).append("HSTS")
    (present if hdrs.get("X-Content-Type-Options") else missing).append("X-Content-Type-Options")
    frame = hdrs.get("X-Frame-Options") or (
        "frame-ancestors" if "frame-ancestors" in (hdrs.get("Content-Security-Policy") or "") else None
    )
    (present if frame else missing).append("X-Frame-Options/frame-ancestors")
    if missing:
        add(p10, "FAIL", "cabeceras ausentes: " + ", ".join(missing) + (f" (presentes: {', '.join(present)})" if present else ""))
    else:
        add(p10, "PASS", "cabeceras de seguridad completas: " + ", ".join(present))

    acao = hdrs.get("Access-Control-Allow-Origin")
    if acao == "*":
        add(p11, "WARN", "Access-Control-Allow-Origin: * — restringir a orígenes concretos si hay API con auth")
    elif acao:
        add(p11, "PASS", f"CORS explícito: {acao}")
    else:
        add(p11, "INFO", "sin cabecera CORS (same-origin por defecto — correcto si no hay API cross-origin)")


def check_npm(root: Path) -> None:
    point = 0  # EXTRA
    pkg = root / "package.json"
    if not pkg.is_file():
        add(point, "SKIP", "sin package.json (npm audit no aplica)")
        return
    if not shutil.which("npm"):
        add(point, "SKIP", "npm no está instalado")
        return
    try:
        r = subprocess.run(
            ["npm", "audit", "--json"], cwd=root, capture_output=True,
            text=True, encoding="utf-8", errors="replace", timeout=120,
        )
    except (OSError, subprocess.TimeoutExpired):
        add(point, "SKIP", "npm audit no respondió")
        return
    try:
        data = json.loads(r.stdout)
        vulns = data.get("metadata", {}).get("vulnerabilities", {})
    except json.JSONDecodeError:
        add(point, "SKIP", "npm audit devolvió JSON ilegible")
        return
    crit = vulns.get("critical", 0)
    high = vulns.get("high", 0)
    mod = vulns.get("moderate", 0)
    total = vulns.get("total", 0)
    if crit or high:
        add(point, "FAIL", f"npm audit: {crit} critical + {high} high (de {total} total)")
    elif mod:
        add(point, "WARN", f"npm audit: {mod} moderate (de {total} total)")
    elif total:
        add(point, "WARN", f"npm audit: {total} vulnerabilidades de baja severidad")
    else:
        add(point, "PASS", "npm audit sin vulnerabilidades")


# ---------------------------------------------------------------- main

def main() -> int:
    ap = argparse.ArgumentParser(description="Auditoría de seguridad (checklist 19 puntos)")
    ap.add_argument("ruta", nargs="?", default=".", help="proyecto a auditar")
    ap.add_argument("--url", help="URL del sitio en vivo (activa checks de cabeceras)")
    args = ap.parse_args()

    root = Path(args.ruta).resolve()
    if not root.is_dir():
        print(f"ERROR: no existe el directorio {root}", file=sys.stderr)
        return 2

    repo = is_repo(root)
    files = list_scan_files(root, repo)

    check_env_en_git(root, repo)
    check_secretos_arbol(root, files)
    check_secretos_historial(root, repo)
    check_logs(root, files)
    check_debug_y_rutas(root, repo, files)
    if args.url:
        check_headers(args.url)
    check_npm(root)

    if not args.url:
        for p in (1, 2, 10, 11):
            add(p, "SKIP", "sin --url: añadir la URL del sitio para verificar")

    order = {"FAIL": 0, "WARN": 1, "PASS": 2, "INFO": 3, "SKIP": 4}
    findings.sort(key=lambda f: (f[0], order.get(f[1], 9)))

    print(f"SECURITY AUDIT — {root}")
    print("-" * 60)
    counts: dict[str, int] = {}
    fails = 0
    for point, level, msg in findings:
        if point == 0:
            label = "EXTRA"
        else:
            label = f"P{point}"
        print(f"[{level:4}] {label:5} {msg}")
        counts[level] = counts.get(level, 0) + 1
        if level == "FAIL":
            fails += 1
    print("-" * 60)
    resumen = " · ".join(f"{k}={v}" for k, v in sorted(counts.items(), key=lambda kv: order.get(kv[0], 9)))
    print(f"Resumen: {resumen}")
    if any(l == "SKIP" and "sin --url" in m for _, l, m in findings):
        print("Sin --url no se verificaron: P1, P2, P10, P11")
    print(f"Manuales (guía en SKILL.md): {', '.join(f'P{p}' for p in MANUAL_POINTS)}")
    if any(p == 5 and l == "FAIL" for p, l, _ in findings):
        print(">> P5 con FAIL: la clave filtrada debe ROTARSE en su proveedor, no solo borrarse del repo.")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
