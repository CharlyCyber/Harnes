---
name: security-audit
description: Auditoría de seguridad para webs y apps vibecodeadas: checklist de los 19 puntos (Cloudflare, HTTPS, .env en git, claves hardcodeadas, CSP, CORS, login seguro, rate limit, permisos en servidor, aislamiento por usuario, RLS, inyección) con script de verificación automatizada (secretos en árbol e historial de git, cabeceras HTTP, npm audit, debug/rutas de prueba). Use cuando se finalice o despliegue un sitio web, o cuando el operador diga "audita seguridad", "revisa seguridad" o "checklist de seguridad".
---

# security-audit — Auditoría de seguridad pre-entrega

> Convierte el checklist de 19 puntos anti-vibecoding en un informe PASS/FAIL por punto. Dos motores: un **script** que automatiza lo medible y una **revisión manual guiada** para lo que solo se juzga leyendo el código. Diseñada para web projects personales (Brand OS CHARLI aplica al 100% en el tono del informe).

## Cuándo se activa

- **Auto:** al terminar de construir o antes de desplegar cualquier sitio web/app.
- **Bajo demanda:** "audita seguridad", "revisa seguridad", "checklist de seguridad" de `<proyecto>`.

## Workflow (3 pasos)

1. **Correr el script** contra el proyecto auditado.
2. **Revisión manual** de los puntos que el script no puede juzgar (P1, P5 y P12–P19), con la guía de esta skill.
3. **Informe final** con los 19 puntos: estado + hallazgo + remediación.

## Paso 1 — Script automatizado

```sh
python skills/security-audit/scripts/audit.py RUTA_PROYECTO [--url https://sitio.com]
```

- Sin `--url` solo corre las checks locales (git, código, npm).
- Con `--url` añade las checks de cabeceras/HTTPS/CORS del sitio en vivo.
- Exit code: `0` sin FAIL · `1` hay FAIL · `2` error fatal.

| Punto | Check del script |
|---|---|
| P3 .env en git | `git ls-files` busca `.env*` trackeados (`.env.example` y similares permitidos) |
| P4 claves hardcodeadas | Regex sobre árbol actual (OpenAI, GitHub, AWS, Google, Slack, private keys, JWT) |
| P5 claves filtradas | Mismos patrones sobre el historial (`git log -p`, últimos 100 commits) |
| P6 secretos en logs | `console.log`/`print`/logger con token/password/secret/authorization |
| P8 debug en prod | `DEBUG = True` en Python, source maps (`dist/**.map`) trackeados |
| P9 rutas de prueba | Definiciones de rutas `/test`, `/debug`, `/dev` en frameworks |
| P10 cabeceras | CSP, HSTS, X-Content-Type-Options, X-Frame-Options/frame-ancestors (requiere `--url`) |
| P11 CORS | `Access-Control-Allow-Origin: *` con credenciales o en API auth (requiere `--url`) |
| P2 HTTPS | Redirección y URL final https (requiere `--url`) |
| P1 Cloudflare | Detecta `cf-ray` en la respuesta (requiere `--url`) |
| Extra | `npm audit` (vulnerabilidades high/critical) si hay `package.json` |

Resultado por hallazgo: `[PASS]` `[FAIL]` `[WARN]` `[INFO]` `[SKIP]` con el número de punto. `SKIP` = no aplica (sin git, sin npm, sin `--url`).

**Nota P4/P7:** la anon key de Supabase (`eyJ…` con `role: anon`) es pública por diseño → el script la marca `INFO`, no FAIL. La `service_role` sí es FAIL. Si el script encuentra cualquier clave filtrada (P5), la remediación **incluye rotación**: borrarla del repo no basta.

## Paso 2 — Revisión manual (P1, P5, P12–P19)

| Punto | Cómo verificar | Cómo arreglar |
|---|---|---|
| **P1 Cloudflare** | `curl -I https://sitio` y mirar cabecera `cf-ray`; o DNS del dominio en el dashboard de Cloudflare | Dominio en Cloudflare → DNS naranja (proxy activo) → reglas TLS: "Always Use HTTPS" + WAF básico |
| **P5 Rotar claves filtradas** | Si el script marcó FAIL en P5/P4: ¿la clave sigue viva en su proveedor? | Rotar en el proveedor (OpenAI dashboard, AWS IAM → deactivate+new, Supabase → rotate service_role), purgar historial (`git filter-repo`) y considerar el compromiso como real |
| **P12 Login seguro** | Hash de contraseñas: ¿bcrypt/argon2? ¿Nunca MD5/SHA1? ¿Cookies `httpOnly`+`secure`+`sameSite`? | Migrar a argon2id/bcrypt; usar Auth.js/Supabase Auth/Clerk en vez de roll-your-where sea posible |
| **P13 Limita intentos** | ¿Hay límite de intentos en login/OTP/reset por IP y por usuario? | Rate limit en middleware o en Cloudflare (WAF → Rate limiting rules); backoff exponencial |
| **P14 Permisos en servidor** | Prueba del intruso: copia la URL de un recurso de usuario A, cámbiala por el de B (o cambia `user_id` en el body) con la sesión de A → ¿el servidor rechaza? | Toda mutación valida sesión **y** pertenencia en el backend; nunca confiar en ids enviados por el cliente |
| **P15 Protege por defecto** | ¿Una ruta nueva queda protegida sin acordarte de protegerla? (middleware global vs rutas sueltas) | Auth global por defecto + whitelist explícita de rutas públicas; políticas por defecto = deny |
| **P16 Aísla datos** | Cada query ¿filtra por `user_id`? Busca `select`/`find`/`get` sin filtro de owner | Añadir `where owner_id = user.id` en todas las queries; test A-vs-B automatizado |
| **P17 RLS y buckets** | Supabase → Authentication → Policies: ¿tablas sin policy? ¿buckets `public` con datos privados? | Activar RLS en TODAS las tablas + policy de `using (auth.uid() = user_id)`; buckets privados; `service_role` solo en servidor |
| **P18 Valida datos** | ¿El backend valida schema (zod/yup) además del frontend? ¿Uploads: MIME, tamaño, extensión? | Validación server-side obligatoria; sanitizar archivos subidos; limitar tamaño y tipos permitidos |
| **P19 SQL/NoSQL injection** | Busca concatenación de strings en queries (`"... WHERE id = " + id`) y `literal()`/`$queryRaw` crudo | Queries parametrizadas / ORM / supabase-js (parametriza por defecto); inputs validados con schema |

## Paso 3 — Informe final

Formato obligatorio: los 19 puntos numerados, cada uno con estado y remediación. Ejemplo:

```
SECURITY AUDIT — <proyecto> — <fecha>
[FAIL] P3   .env y .env.production trackeados en git
[WARN] P6   console.log con 'token' en src/api/client.js:12
[PASS] P10  CSP + HSTS + X-Content-Type-Options presentes
[REVISAR] P14  Sin prueba A-vs-B de permisos — revisión manual pendiente
...
Resumen: 6 FAIL · 3 WARN · 7 PASS · 4 SKIP · 4 manuales pendientes
```

- `FAIL` bloquea el deploy: arreglar y re-correr el script.
- `WARN` no bloquea pero entra en el plan de remediación.
- Nada se da por bueno sin evidencia (script, curl o lectura de código).

## Extras incluidos

- **npm audit:** vulnerabilidades high/critical en dependencias → FAIL.
- **Historial git:** secretos en commits pasados → FAIL + obliga a P5 (rotación).

## Límites

- No sustituye un pentest: cubre los 19 puntos conocidos, no bugs desconocidos.
- La validación de RLS/authz (P14–P17) es semi-automática por naturaleza: la guía obliga a probar, no a leer y asumir.
