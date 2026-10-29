# skills/

Catálogo **intencionalmente vacío**. Las skills se instalarán aquí bajo demanda, siguiendo el estándar de agentskills.io:

```
mi-skill/
├── SKILL.md        # requerido: frontmatter (name, description) + instrucciones
├── scripts/        # opcional: código ejecutable
├── references/     # opcional: documentación on-demand
└── assets/         # opcional: plantillas, recursos
```

Condiciones para añadir una skill (ratchet):

1. Existe un comportamiento o fallo que la justifica (trazable en `knowledge/failures.md`).
2. `SKILL.md` < 500 líneas; cuerpo < 5000 tokens; recursos con disclosure progresiva.
3. Solo rutas relativas.
