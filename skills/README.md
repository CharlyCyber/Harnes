# skills/

Catálogo canónico. Ver `REGISTRO.md` para procedencia, licencias, stack base activo y decisiones (incluye difidas y descartadas con razón).

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
4. Variante upstream registrada en `REGISTRO.md` con commit + licencia + `LICENSE-upstream`.
