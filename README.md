# Solucionario de Inteligencia Artificial (SI3003)

**Juan David Sierra Orozco**
Universidad EAFIT, semestre 2026-2

Repositorio con las actividades y laboratorios de clase resueltos. Cada carpeta corresponde a una clase del curso y contiene la entrega de esa sesión.

---

## Contenido

| Clase | Tema | Entrega | Estado |
|---|---|---|---|
| 1 | Agentes racionales | [`clase1-agentes-racionales/`](clase1-agentes-racionales/) | Completa |
| 3 | Optimización local | [`clase3-optimizacion/`](clase3-optimizacion/) | Completa |
| 4 | Procesos de decisión de Markov | [`clase4-mdps/`](clase4-mdps/) | Completa |

---

### Clase 1 — Agentes racionales

[`clase1-agentes-racionales/clase1.md`](clase1-agentes-racionales/clase1.md)

Ficha de análisis de un Space de Hugging Face desde la perspectiva de los agentes racionales. Incluye el análisis PEAS, la clasificación del entorno con su justificación, el tipo de programa de agente propuesto, y el reto adicional con dos Spaces más: uno totalmente observable, determinista y episódico, y otro parcialmente observable, estocástico y secuencial.

Space analizado: [Z-Image-Turbo](https://huggingface.co/spaces/mrfakename/Z-Image-Turbo), generación de imágenes a partir de texto.

---

### Clase 3 — Optimización local

[`clase3-optimizacion/02_simulated_annealing_resuelto.ipynb`](clase3-optimizacion/02_simulated_annealing_resuelto.ipynb)

Notebook de Simulated Annealing con las tres actividades resueltas, cada una con su análisis escrito:

- **Actividad 1, temperatura inicial.** Barrido de `T0` en `{0.01, 0.1, 0.5, 1, 3, 10}` con 30 corridas por valor, reportando media, desviación estándar y porcentaje de corridas que alcanzan el óptimo global.
- **Actividad 2, calendario de enfriamiento.** Comparación de `alpha` en `{0.85, 0.90, 0.95, 0.99, 0.992, 0.999, 1.0}`, con la verificación directa de por qué enfriar demasiado rápido degenera en Hill Climbing.
- **Actividad 3, problema discreto.** Adaptación de Simulated Annealing al problema de ubicación de hospitales del notebook anterior, usando la regla de aceptación para minimización, y comparación estadística contra Hill Climbing sobre 30 corridas.

[`clase3-optimizacion/actividad-asistencia.pdf`](clase3-optimizacion/actividad-asistencia.pdf)

Actividad de asistencia de la sesión, resuelta a mano: relación entre el método simplex y hill climbing, planteamiento del problema como flujo en red, definición de la función objetivo, y por qué los métodos de búsqueda local no garantizan el óptimo global.

---

### Clase 4 — Procesos de decisión de Markov

[`clase4-mdps/03_lab_warehouse_resuelto.ipynb`](clase4-mdps/03_lab_warehouse_resuelto.ipynb)

Laboratorio del robot de entregas en un almacén, resuelto de punta a punta.

**Parte 1.** Modelado del MDP a partir de la imagen del enunciado: grid de 5x6 con 26 estados transitables, cuatro estanterías, tres celdas de piso resbaloso, tres terminales y dos peligros no terminales. La transición `T(s,a,s')` reparte la probabilidad según el piso del estado actual, `0.90/0.05/0.05` en piso normal y `0.60/0.20/0.20` en piso resbaloso.

**Partes 2 y 3.** Value Iteration y Policy Iteration implementadas por separado. Ambas convergen a la misma política óptima: Value Iteration en 20 iteraciones, Policy Iteration en 4 iteraciones de política que suman 210 barridos de evaluación.

**Parte 5.** Las cinco preguntas de interpretación respondidas, más los tres experimentos y el bonus. Resultados principales:

- Con los parámetros base el robot prefiere la estación de carga `+2` antes que la zona de entrega `+10`, porque el costo por paso se come la diferencia.
- El estado `(1,2)` es la bisagra de todo el problema. Con `gamma = 0.99` cambia únicamente ese estado, y eso basta para redirigir la ruta completa hacia la entrega.
- El experimento del piso más resbaloso no cambia la política en ningún estado, solo empeora los valores, porque `(1,2)` es un cuello de botella sin ruta alternativa.
- El punto de quiebre del costo por paso está en `living_reward` cercano a `-0.80`, y el cambio de comportamiento es abrupto, no gradual.

---

## Cómo ejecutar los notebooks

Requieren `numpy` y `matplotlib`:

```bash
pip install numpy matplotlib jupyterlab
jupyter lab
```

Todos los notebooks están guardados con sus salidas ya calculadas, así que también se pueden leer directamente en GitHub sin ejecutarlos.
