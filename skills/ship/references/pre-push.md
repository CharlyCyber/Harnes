
# no-mistakes — Git Proxy Gate con Validación Autónoma

> Skill para integrar `no-mistakes` como git proxy gate que intercepta pushes, ejecuta pipeline de validación AI-driven en worktree aislado, y solo reenvía a remoto real cuando todo está verde.

## Descripción

`no-mistakes` pone un proxy git local delante de tu remoto real. Haces `git push no-mistakes <branch>` en vez de `git push origin`, y el proxy:
1. Crea un worktree descartable (tu trabajo no se toca)
2. Corre pipeline de validación: review → test → docs → lint → push → PR → CI
3. Cada check pasa solo o se detiene con un **hallazgo** (finding)
4. Arreglos mecánicos seguros se aplican automáticamente
5. Lo que necesita decisión humana se escala para **approve**, **fix** o **skip**
6. Nada llega al remoto hasta que todo está verde → PR limpio

## Instalación

```sh
curl -fsSL https://raw.githubusercontent.com/kunchenguid/no-mistakes/main/docs/install.sh | sh
```

O en Windows vía Go install / build desde source. Docs: <https://kunchenguid.github.io/no-mistakes/>

```sh
no-mistakes init   # configura el gate en el repo actual
```

## Tres formas de gatillar

| Forma | Cuándo usarla |
|---|---|
| `git push no-mistakes` | Push explícito a gate en vez de origin. Branch commiteada. |
| `no-mistakes` | TUI interactiva. Sin commit necesario — wizard crea branch, commitea y pushea. `-y` para automático. |
| `/no-mistakes <tarea>` | Agent skill. Dile al agente que haga una tarea y la pase por el gate. |

## Pipeline

```
branch ──> worktree descartable
               │
               ├── review (AI code review)
               ├── test  (test suite)
               ├── docs  (documentación)
               ├── lint  (linter/formatter)
               ├── push  (forward a remoto real)
               ├── PR    (auto-open PR)
               └── CI    (monitorear CI, auto-fix si falla)
               │
               ▼
         clean PR abierto
```

- **Auto-fix**: arreglos mecánicos se aplican solos (formato, typos, imports)
- **Ask-user**: decisiones de intención se escalan
- **Cada finding**: se puede approve / fix / skip desde TUI

## Uso diario

```sh
git checkout -b feature/nueva-funcionalidad
# ... trabajar ...
git add -A
git commit -m "feat: nueva funcionalidad"
git push no-mistakes feature/nueva-funcionalidad
no-mistakes
# TUI muestra findings, actúas sobre cada uno
# Al final: PR limpio abierto automáticamente
```

## Modo agente

```sh
# En sesión de Claude/opencode/codex:
/no-mistakes "implementa login con OAuth y pásalo por el gate"
```

El agent skill corre el pipeline headless, aplica auto-fixes, y solo para en findings que necesitan decisión humana.

## Configuración

Inicializado por repo. Estado en `~/.no-mistakes/repos/<hash>.git`. Skill instalado para el agente a nivel usuario.

## Referencias

- Referencia rápida: `references/quickstart.md`
- Documentación completa: <https://kunchenguid.github.io/no-mistakes/>
- Repo: <https://github.com/kunchenguid/no-mistakes>
