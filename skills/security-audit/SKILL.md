---
name: security-audit
description: Auditoría de seguridad read-only de webs y apps (incluidas las vibecodeadas): escáner offline de stack, dependencias y CVEs, secretos, inyección (SQLi, XSS, SSRF, ejecución de comandos), auth/cookies/CORS/cabeceras, Docker, CI y servicios externos (Supabase, Firebase), más el checklist de 19 puntos y la revisión manual de lo que ningún escáner ve (IDOR, RLS, lógica de negocio). Informes en MD/JSON/SARIF con estados confirmed / needs-review / preventive. Use antes de desplegar, al terminar una web, o cuando el operador diga "audita seguridad", "revisa seguridad", "checklist de seguridad", "security review", "busca vulnerabilidades" o pregunte si su sitio está afectado por un CVE.
---

# security-audit — Auditoría de seguridad pre-entrega

> Una sola skill, dos capas que se complementan: un **escáner** que encuentra lo mecánico y un **checklist de 19 puntos** que obliga a mirar lo que ningún escáner ve. El escáner propone; tú verificas antes de llamar vulnerabilidad a un patrón.

## Cuándo se activa

- **Auto:** al terminar de construir o antes de desplegar cualquier sitio web/app.
- **Bajo demanda:** "audita seguridad", "revisa seguridad", "checklist de seguridad", "security review", "¿estoy afectado por el CVE X?" de `<proyecto>`.

## Reglas duras (siempre)

1. **Read-only por defecto.** No editas, borras, instalas, actualizas ni commiteas nada hasta que el usuario apruebe un arreglo concreto. Proponer un parche está bien; aplicarlo necesita un sí.
2. **Nada de ataques.** Nunca envíes payloads de explotación, fuzzes, fuerces login ni escanees sistemas. Las dos únicas acciones de red son opt-in y se explican en el paso 2.
3. **Nunca imprimas secretos.** Los informes los redactan; cuando cites código, redacta igual (4 primeros caracteres + `******`).
4. **Honestidad de certeza.** Un patrón no es una vulnerabilidad, y una vulnerabilidad no es un ataque. Nunca digas que un proyecto "fue hackeado" o "es explotable" sin evidencia.
5. **Un CVE de runtime se arregla subiendo el runtime.** Cambiar código de aplicación o plugins no arregla un PHP/Node vulnerable; una regla de WAF es defensa en profundidad, no el arreglo.

## Workflow (5 pasos)

1. **Alcance** → confirmar ruta, si es código propio y dónde van los informes (por defecto, temp del sistema, fuera del proyecto).
2. **Escaneo** → `nfaudit scan` offline.
3. **Checklist 19 puntos** → `audit.py` (incluye historial de git, que el escáner no cubre).
4. **Triage y revisión manual** → separar confirmed / needs-review / preventive y leer el código de los puntos P1, P5 y P12–P19.
5. **Informe y arreglos** → informe con los 19 puntos + secciones por estado; arreglos solo con aprobación, y re-escanear después.

## Paso 2 — Escáner profundo (`nfaudit`)

```sh
python skills/security-audit/scripts/nfaudit.py scan RUTA
```

Offline y read-only por defecto. Escribe el informe en el directorio temporal del sistema (fuera del proyecto) y muestra la ruta; `--out` para cambiarla, `--stdout json|md|sarif` para imprimir sin escribir, `--format md,json,sarif` para SARIF.

Cubre: detección de stack, secretos con entropía, patrones de inyección, configuración (cookies, CORS, cabeceras, Firebase/Supabase), Docker, CI, versiones de runtime y dependencias contra la lista local de avisos. El JSON trae `stack`, cada hallazgo con `status`/`severity`/`file`/`line`/`evidence`/`fingerprint`, más `entry_points` (superficie de ataque) y `notes` (huecos de cobertura).

**Dos opt-ins que se preguntan, nunca se asumen:**

- **CVEs reales de dependencias:** `--osv`. Envía *solo nombres y versiones* a OSV.dev, nunca código. Pregunta: *"¿Consulto tus dependencias en OSV.dev? Solo se envían nombres y versiones de paquetes."*
- **Cabeceras en vivo:** `nfaudit headers https://sitio-del-usuario`. Una única petición GET a un dominio que el usuario posea; comprueba HSTS, CSP, cookies, CORS y banners de versión. Sin crawling ni payloads.

Si ya están instalados `osv-scanner`, `gitleaks`, `trivy` o `semgrep`, puedes ofrecerlos como segunda opinión. No instales nada sin aprobación.

## Paso 3 — Checklist de 19 puntos (`audit.py`)

```sh
python skills/security-audit/scripts/audit.py RUTA_PROYECTO [--url https://sitio.com]
```

- Sin `--url` corre solo las checks locales (git, código, npm). Con `--url` añade cabeceras/HTTPS/CORS del sitio en vivo.
- Exit code: `0` sin FAIL · `1` hay FAIL · `2` error fatal.

| Punto | Check del script |
|---|---|
| P3 .env en git | `git ls-files` busca `.env*` trackeados (`.env.example` y similares permitidos) |
| P4 claves hardcodeadas | Regex sobre el árbol actual (OpenAI, GitHub, AWS, Google, Slack, private keys, JWT) |
| P5 claves filtradas | Mismos patrones sobre el historial (`git log -p`, últimos 100 commits) |
| P6 secretos en logs | `console.log`/`print`/`logger` con token/password/secret/authorization |
| P8 debug en prod | `DEBUG = True` en Python, source maps (`dist/**.map`) trackeados |
| P9 rutas de prueba | Definiciones de rutas `/test`, `/debug`, `/dev` en frameworks |
| P10 cabeceras | CSP, HSTS, X-Content-Type-Options, X-Frame-Options/frame-ancestors (requiere `--url`) |
| P11 CORS | `Access-Control-Allow-Origin: *` con credenciales o en API auth (requiere `--url`) |
| P2 HTTPS | Redirección y URL final https (requiere `--url`) |
| P1 Cloudflare | Detecta `cf-ray` en la respuesta (requiere `--url`) |
| Extra | `npm audit` (vulnerabilidades high/critical) si hay `package.json` |

Resultado por hallazgo: `[PASS]` `[FAIL]` `[WARN]` `[INFO]` `[SKIP]` con el número de punto. `SKIP` = no aplica (sin git, sin npm, sin `--url`).

**Nota P4/P7:** la anon key de Supabase (`eyJ…` con `role: anon`) es pública por diseño → `INFO`, no FAIL. La `service_role` sí es FAIL. Si aparece cualquier clave filtrada (P5), la remediación **incluye rotación**: borrarla del repo no basta.

## Paso 4 — Triage y revisión manual

Ordena los hallazgos así: `confirmed` → `suspected` high/critical → el resto.

| Estado | Qué significa | De dónde sale |
|---|---|---|
| `confirmed` | Evidencia inequívoca: versión vulnerable fijada en lockfile, reglas de Firebase abiertas, `.env` commiteado. Aun así, comprueba que el archivo escaneado es el que corre en producción. | match de aviso, valor exacto de configuración |
| `suspected` (*needs review*) | Patrón de riesgo. Solo es vulnerabilidad si un dato controlado por el atacante llega ahí sin protección. | reglas de código, secretos en fuente |
| `preventive` | Hardening. No es vulnerabilidad por sí solo. | cabeceras ausentes, imágenes sin pin, contenedores root |

**Rastrea source → sink** en cada `suspected`: el sink es la línea marcada (query, `exec`, `innerHTML`, `fetch(url)`, `include`); la source es de dónde viene el valor (params, body, cabeceras, cookies, URL, uploads, webhooks, respuestas de terceros); el camino es lo que hay en medio (consultas parametrizadas, bindings de ORM, escape del motor de plantillas, allow-lists, coerción de tipo). **Intenta refutarlo.** Si la protección aguanta, descarta el hallazgo y anota por qué; si no puedes saberlo, déjalo como *needs review* con la pregunta abierta.

**No merece la pena reportar:** DoS por peticiones pesadas, falta de rate limit (salvo que proteja login/OTP), open redirect sin fuga de token, hallazgos en tests/fixtures/docs/generados, y secretos que son placeholders obvios o claves públicas por diseño (Supabase anon, Firebase web config, Stripe publishable) — para esas, revisa las reglas del servidor (RLS, security rules).

**Revisión manual (P1, P5, P12–P19):**

| Punto | Cómo verificar | Cómo arreglar |
|---|---|---|
| **P1 Cloudflare** | `curl -I https://sitio` y mirar `cf-ray`; o el DNS en el dashboard | Dominio en Cloudflare → DNS naranja → "Always Use HTTPS" + WAF básico |
| **P5 Rotar claves filtradas** | Si el script marcó FAIL en P5/P4: ¿la clave sigue viva en el proveedor? | Rotar en el proveedor (OpenAI, AWS IAM, Supabase service_role), purgar historial (`git filter-repo`) y tratar el compromiso como real |
| **P12 Login seguro** | ¿bcrypt/argon2? ¿Nunca MD5/SHA1? ¿Cookies `httpOnly`+`secure`+`sameSite`? | argon2id/bcrypt; Auth.js/Supabase Auth/Clerk antes que hacerlo a mano |
| **P13 Limita intentos** | ¿Límite en login/OTP/reset por IP y por usuario? | Rate limit en middleware o Cloudflare (WAF → rate limiting); backoff exponencial |
| **P14 Permisos en servidor** | Prueba del intruso: URL de un recurso de A cambiada por la de B con la sesión de A → ¿el servidor rechaza? | Toda mutación valida sesión **y** pertenencia en backend; nunca confiar en ids del cliente |
| **P15 Protege por defecto** | ¿Una ruta nueva queda protegida sin acordarte? | Auth global por defecto + whitelist explícita; política por defecto = deny |
| **P16 Aísla datos** | Cada query ¿filtra por `user_id`? Busca `select`/`find`/`get` sin filtro de owner | `where owner_id = user.id` en todas; test A-vs-B automatizado |
| **P17 RLS y buckets** | Supabase → Policies: ¿tablas sin policy? ¿buckets `public` con datos privados? | RLS en todas las tablas + policy `using (auth.uid() = user_id)`; buckets privados; `service_role` solo en servidor |
| **P18 Valida datos** | ¿El backend valida schema (zod/yup)? ¿Uploads: MIME, tamaño, extensión? | Validación server-side obligatoria; sanitizar uploads; limitar tamaño y tipos |
| **P19 SQL/NoSQL injection** | Concatenación en queries (`"... WHERE id = " + id`), `literal()`, `$queryRaw` crudo | Consultas parametrizadas / ORM / supabase-js; inputs validados con schema |

Para el detalle por stack (Next.js, Laravel/PHP, Django/Flask, Express, Supabase/Firebase, Docker, CI) usa `references/checklists.md`. Para el método de severidad y la lista de falsos positivos, `references/methodology.md`.

## Paso 5 — Informe y arreglos

Formato: los 19 puntos numerados con estado y remediación, seguidos de las tres secciones de estado. Plantilla completa: `references/report-template.md`.

```
SECURITY AUDIT — <proyecto> — <fecha>
[FAIL] P3   .env y .env.production trackeados en git
[WARN] P6   console.log con 'token' en src/api/client.js:12
[PASS] P10  CSP + HSTS + X-Content-Type-Options presentes
[REVISAR] P14  Sin prueba A-vs-B de permisos — revisión manual pendiente
...
Resumen: 6 FAIL · 3 WARN · 7 PASS · 4 SKIP · 4 manuales pendientes

Confirmed: 2 (1 critical) · Needs review: 5 · Preventive: 3
No cubierto: infraestructura, flujo de pago, versión real del runtime en el servidor
```

- `FAIL` bloquea el deploy: arreglar y re-correr.
- `WARN` no bloquea, pero entra en el plan de remediación.
- Nada se da por bueno sin evidencia (script, curl o lectura de código).
- Cierra siempre con **lo que no se cubrió**.

**Arreglos:** ofrécelos ordenados por riesgo, muestra el cambio exacto (diff o comando) y espera aprobación. Después de aplicar, re-escanea para confirmar. Nunca rotes claves, hagas push ni despliegues por el usuario: dile qué hacer (p. ej. "rota esta key en el dashboard de Stripe primero").

## Configuración

`.nfaudit.json` opcional en la raíz del proyecto:

```json
{ "exclude": ["legacy/**"], "disable_rules": ["js-weak-hash"], "ignore": ["<fingerprint>"], "include_tests": true }
```

`nfaudit-ignore` en la línea (o encima) silencia esa línea. `--fail-on high` hace que CI falle con hallazgos no preventivos de esa severidad o superior.

## Límites (dilos cuando vengan al caso)

- Las reglas de patrón son por línea, no análisis de flujo de datos: habrá falsos positivos y omisiones.
- La lista local de avisos es pequeña y fechada (`data/known-advisories.json` → `updated`); para cobertura real usa `--osv`.
- No ve la versión real del runtime en el servidor, ni el WAF, ni la red, ni la configuración cloud.
- No sustituye un pentest: cubre lo conocido, no bugs desconocidos.
- La validación de RLS/authz (P14–P17) es semi-automática por naturaleza: la guía obliga a probar, no a leer y asumir.

## Procedencia

Motor `nfaudit` y referencias: [notfound404es/notfound-security-audit](https://github.com/notfound404es/notfound-security-audit) @ `c5d7c0e`, licencia MIT (`LICENSE-upstream`). El checklist de 19 puntos y `scripts/audit.py` son propios del harnés CHARLI.
