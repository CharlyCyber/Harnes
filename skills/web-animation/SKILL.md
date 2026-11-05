---
name: web-animation
description: Animación web con Framer Motion (React) y GSAP (universal). Cubre motion components, timelines, scroll-triggered, layout transitions, stagger, y principios de motion design.
---

# Web Animation

Skill unificada para animación web. Cubre **Framer Motion** (React/Next.js, declarativo) y **GSAP** (universal, frame-accurate, scroll).

## Cuándo usar qué

| Situación | Herramienta |
|---|---|
| Animaciones en React/Next.js (UI, micro-interacciones) | Framer Motion |
| Transiciones de layout automáticas | Framer Motion `layout` / `layoutId` |
| Gestos (drag, hover, tap, focus) | Framer Motion |
| Scroll-triggered complejo (pin, scrub, horizontal) | GSAP ScrollTrigger |
| Timeline secuencial con control frame a frame | GSAP Timeline |
| Split text / scramble / drawSVG | GSAP plugins |
| Animaciones fuera de React | GSAP |
| 3D / canvas | Three.js / R3F (no cubierto aquí) |

**CRITICAL:** No mezclar GSAP y Framer Motion en el mismo árbol de componentes. Usar Framer para UI/interacciones. GSAP para scrolltelling o backgrounds aislados con cleanup en useEffect.

---

## Framer Motion

### Motion Components

```jsx
import { motion } from "framer-motion";

<motion.div animate={{ x: 100 }} />
<motion.button whileHover={{ scale: 1.1 }} whileTap={{ scale: 0.95 }} />
<motion.img src={"/photo.jpg"} whileInView={{ opacity: 1, y: 0 }} />
```

### Props principales

`initial`, `animate`, `exit`, `whileHover`, `whileTap`, `whileFocus`, `whileInView`, `transition`, `variants`, `layout`, `layoutId`.

### Transition

```jsx
<motion.div
  animate={{ x: 100, opacity: 1 }}
  transition={{ type: "spring", stiffness: 100, damping: 20, mass: 1 }}
/>
```

Tipos: `tween` (duración fija), `spring` (físico), `inertia` (desaceleración).
Easing presets: `linear`, `easeIn`, `easeOut`, `circIn`, `backOut`, etc.

### Variants + Stagger

```jsx
const variants = {
  hidden: { opacity: 0, y: 20 },
  visible: { opacity: 1, y: 0, transition: { staggerChildren: 0.1 } }
};
<motion.div variants={variants} initial="hidden" animate="visible">
  <motion.p variants={variants}>Item</motion.p>
</motion.div>
```

### AnimatePresence

```jsx
<AnimatePresence mode="wait">
  {isVisible && <motion.div key="modal" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} />}
</AnimatePresence>
```

### Layout Animations

```jsx
<motion.div layout /> {/* anima cambios de tamaño/posición automáticamente */}
<motion.div layoutId="card" /> {/* shared element transition entre vistas */}
```

### useScroll + useTransform (scroll performance)

```jsx
const { scrollYProgress } = useScroll();
const scale = useTransform(scrollYProgress, [0, 1], [1, 1.5]);
<motion.div style={{ scale }} />;
```

Performance: usar `useMotionValue` + `useTransform` en vez de `useState` para continuous animations. Evita re-renders.

---

## GSAP

### Core Methods

```js
gsap.to(target, vars)     // desde estado actual → vars
gsap.from(target, vars)   // desde vars → estado actual
gsap.fromTo(target, from, to)
gsap.set(target, props)   // aplicar inmediato (duration 0)
```

### Easing

Built-in: `power1`–`power4`, `back`, `bounce`, `circ`, `elastic`, `expo`, `sine`.

### Timelines

```js
const tl = gsap.timeline({ defaults: { duration: 0.5, ease: "power2.out" } });
tl.to(".a", { x: 100 })
  .to(".b", { y: 50 }, "<")     // mismo inicio que anterior
  .to(".c", { opacity: 0 }, "+=0.3"); // 0.3s después
```

### ScrollTrigger

```js
gsap.registerPlugin(ScrollTrigger);

gsap.to(".panel", {
  x: "-300vw", ease: "none",
  scrollTrigger: {
    trigger: ".container", start: "top top", end: "+=3000",
    scrub: 1, pin: true, toggleActions: "play none none reverse"
  }
});
```

### Plugins clave

| Plugin | Función |
|---|---|
| ScrollTrigger | Scroll-driven animations, pin, scrub |
| SplitText | Dividir texto en chars/words/lines para animar |
| Flip | Animación fluida entre estados del DOM |
| Draggable | Drag and drop |
| MotionPath | Animación a lo largo de SVG path |
| DrawSVG | Animar dibujo de paths SVG |
| MorphSVG | Morphing entre formas SVG |
| ScrambleText | Efecto matrix en texto |
| TextPlugin | Typewriter effect |
| CustomEase | Curvas de easing personalizadas |

### React Hook (useGSAP)

```jsx
import { useGSAP } from "@gsap/react";

function Component() {
  const container = useRef();
  useGSAP(() => {
    gsap.to(".box", { x: 100 }); // auto-cleanup on unmount
  }, { scope: container, dependencies: [] });
}
```

### Performance GSAP

- Animar solo `transform` y `opacity` (compositor)
- `gsap.quickTo()` para updates frecuentes (mouse followers)
- `gsap.context().revert()` para cleanup en SPAs/React
- Detectar reduced motion: `gsap.matchMedia()`

---

## Principios de motion design

- **Spring physics**: sin linear easing. Usar `type: "spring"` en FM o `ease: "power2.out"` en GSAP para sensación premium.
- **Staggered orchestration**: no montar listas/grids instantáneamente. Usar `staggerChildren` (FM) o `stagger` (GSAP).
- **Perpetual micro-interactions**: pulse, float, shimmer, carousel en componentes que deben sentirse "vivos". Aislar en componentes memoizados.
- **Layout transitions**: usar `layout`/`layoutId` (FM) o `Flip` (GSAP) para transiciones suaves entre estados.
- **Scroll-triggered reveals**: `whileInView` (FM) o `ScrollTrigger` (GSAP) para entradas por scroll.
- **Reduced motion**: respetar `prefers-reduced-motion`. Usar `gsap.matchMedia()` o CSS media query.
