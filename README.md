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
| 5 | Aprendizaje por refuerzo | [`clase5-reinforcement-learning/`](clase5-reinforcement-learning/) | Completa (2 entregas) |
| 7 | Clasificación supervisada | [`clase7-clasificacion/`](clase7-clasificacion/) | Completa |
| 8 | Regresión | [`clase8-regresion/`](clase8-regresion/) | Completa |

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

### Clase 5 — Aprendizaje por refuerzo

[`clase5-reinforcement-learning/ejercicio_grid15_vi_pi_qlearning.ipynb`](clase5-reinforcement-learning/ejercicio_grid15_vi_pi_qlearning.ipynb)

Ejercicio de clase: construir un grid de 15x15 con 5 obstáculos, un inicio y un final, y trazar el mejor camino entre ambos usando método de valores, política de dirección y aprendizaje por refuerzo, mostrando el avance a lo largo de las iteraciones.

El mismo mundo se resuelve de tres maneras para poder compararlas. Las transiciones son estocásticas (`0.8 / 0.1 / 0.1`, la convención usada en clase), de modo que los obstáculos representan un riesgo real y el problema no se reduce a un camino más corto.

**Método de valores (Value Iteration).** Converge en 58 iteraciones. Se incluyen imágenes del grid en las iteraciones 1, 2, 5, 15 y 30, donde se observa cómo el valor nace en la meta y se propaga hacia atrás una celda por barrido, más la curva de convergencia en escala logarítmica.

**Política de dirección (Policy Iteration).** Converge en 18 iteraciones de política que suman 2766 barridos de evaluación, y llega exactamente a la misma política que Value Iteration, con cero estados en desacuerdo.

**Aprendizaje por refuerzo (Q-Learning).** 5000 episodios con epsilon decreciente, partiendo de una tabla en cero y sin acceso a `T(s,a,s')`. El avance del entrenamiento se documenta con una tabla de progreso por checkpoint y con cuatro mapas de la política aprendida en distintos momentos.

Resultados sobre 300 episodios de evaluación:

| Método | Recompensa | Pasos | Llega a la meta |
|---|---|---|---|
| Value Iteration | 67.49 | 33.5 | 100% |
| Policy Iteration | 67.49 | 33.5 | 100% |
| Q-Learning | 67.11 | 33.9 | 100% |

Como en este mundo se conoce la solución óptima, es posible medir cuánto le falta al agente durante el entrenamiento: la pérdida media de valor cae de `52.5` en el primer episodio a `1.03` al final.

El análisis de cierre discute por qué solo el 74.9% de las acciones aprendidas coinciden con las óptimas y aun así el desempeño es prácticamente idéntico. La causa no son empates entre caminos equivalentes, que representan apenas el 1.4% de los estados, sino que los errores se concentran en zonas alejadas del corredor que el agente recorre. Q-Learning aprende bien únicamente lo que visita.

[`clase5-reinforcement-learning/verificacion_rostros_rl.ipynb`](clase5-reinforcement-learning/verificacion_rostros_rl.ipynb)

Segundo ejercicio: verificación de identidad facial donde la decisión la toma una política aprendida con Q-Learning.

El problema se separa en dos capas y solo la segunda usa refuerzo. La percepción se resuelve con PCA (eigenfaces) y distancia coseno contra una galería de 5 fotos por identidad, lo cual reduce cada caso a un número. Sobre esa señal, el agente aprende a elegir entre `aceptar`, `rechazar` y `pedir otra foto`, con un falso positivo penalizado cuatro veces más que un falso negativo.

El aporte del refuerzo es aprender **cuándo todavía no conviene decidir**. Sin que nadie se lo indique, el agente descubre la franja de distancias donde las distribuciones de "misma persona" y "persona distinta" se solapan, y en esa zona pide evidencia adicional en lugar de arriesgarse.

Resultados sobre identidades que el agente nunca vio durante el entrenamiento:

| Método | Recompensa | Fotos usadas | Exactitud | Falsos positivos |
|---|---|---|---|---|
| Umbral fijo óptimo, 1 foto | 0.655 | 1.00 | 89.6% | 273 |
| Política aprendida con RL | 0.679 | 1.77 | 91.2% | 215 |

La reducción de falsos positivos es del 21%. Un experimento adicional barre el costo de pedir evidencia y muestra que la ventaja desaparece cuando ese costo supera aproximadamente `0.05`: a partir de ahí el agente deja de pedir fotos y su política colapsa a la del umbral fijo.

---

### Clase 7 — Clasificación supervisada

[`clase7-clasificacion/clasificadores_iris.ipynb`](clase7-clasificacion/clasificadores_iris.ipynb)

Comparación de tres clasificadores sobre el dataset Iris (incluido en scikit-learn) — **LDA**, **K-NN (k=3)** y **Árbol de decisión** — repetida sobre tres particiones estratificadas distintas: **70/30**, **60/40** y **80/20**.

Cada modelo se entrena primero con las 4 características (largo y ancho de sépalo y pétalo), que es el resultado real reportado como desempeño, y luego solo con largo y ancho de pétalo, las dos variables que mejor separan las especies, para poder dibujar las fronteras de decisión. Esto se repite para las tres particiones, con una cuadrícula de 9 paneles (partición × modelo) para comparar las fronteras de un vistazo.

Resultados con las 4 características, en cada partición:

| Modelo | 70/30 | 60/40 | 80/20 |
|---|---|---|---|
| LDA | 97.8% (44/45) | 98.3% (59/60) | 100% (30/30) |
| K-NN (k=3) | 95.6% (43/45) | 96.7% (58/60) | 100% (30/30) |
| Árbol de decisión | 93.3% (42/45) | 95.0% (57/60) | 93.3% (28/30) |

Ningún modelo confunde jamás la especie *setosa*, que es linealmente separable de las otras dos. Todos los errores, en los tres clasificadores y en las tres particiones, ocurren distinguiendo *versicolor* de *virginica*, que es donde las mediciones de las dos especies genuinamente se solapan.

La jerarquía LDA ≥ K-NN ≥ Árbol se mantiene en las tres particiones y se confirma con una validación cruzada de 5 pliegues sobre los 150 datos completos (LDA 98.0%, K-NN 96.7%, Árbol 95.3%), lo que descarta que sea un efecto de haber elegido justo la partición 70/30. El 100% de LDA y K-NN con 80/20 no significa un clasificador perfecto: el conjunto de prueba se reduce a 30 muestras y, en esa partición particular, no incluyó ninguno de los casos límite entre las dos especies que sí aparecen con otras proporciones — una ilustración directa de por qué una sola partición puede ser optimista o pesimista según el azar del muestreo.

Las fronteras de decisión muestran el sesgo de cada algoritmo: LDA traza una única recta inclinada, K-NN una curva irregular ajustada al detalle local, y el árbol una sucesión de rectángulos por sus cortes perpendiculares a los ejes. Los casos mal clasificados de cada modelo aparecen siempre pegados a esa frontera, nunca dentro de una región limpia, lo que confirma que el error no es azar sino la zona genuinamente ambigua del problema.

[`clase7-clasificacion/ejercicio3_subajuste_sobreajuste.ipynb`](clase7-clasificacion/ejercicio3_subajuste_sobreajuste.ipynb)

Ejercicio 3: provocar subajuste y sobreajuste sobre Iris por dos vías —particiones inusuales (50/50, 60/40) y complejidad de modelo sin justificar (`k=7` en K-NN)— diagnosticando con la brecha entre exactitud de entrenamiento y de prueba.

**La partición (Opción 1) no demostró la hipótesis ingenua.** Promediando 30 semillas por partición, el sobreajuste del árbol (siempre con 100% de exactitud en entrenamiento) se mantiene prácticamente constante entre 50/50 y 90/10, entre 0.047 y 0.057 de brecha, sin empeorar de forma clara con menos datos. Lo que sí cambia con la partición es el **ruido de la medición**: con 90/10 la desviación estándar del test accuracy casi se triplica respecto a 50/50, porque el conjunto de prueba queda en solo 15 muestras. La lección real: una partición inusual no arruina al modelo, arruina la **confiabilidad del diagnóstico** si no se repite.

**La complejidad (Opción 2) sí mostró sub y sobreajuste genuinos, con una sorpresa.** `k=1` en K-NN sobreajusta de manual (train 100%, test 93.3%). Pero `k=7`, el valor que sugiere el enunciado como aumento injustificado, en realidad **mejora** la cross-validation (0.980 contra 0.967 de k=3), porque Iris es un dataset limpio y bien separado. El subajuste real solo aparece desde `k≈31`, y `k=105` (el tamaño exacto del set de entrenamiento) colapsa la exactitud a 0.333, el nivel de azar con 3 clases: el modelo pasa a votar siempre por la clase mayoritaria sin mirar dónde cae el punto, visible en la frontera de decisión como un plano de un solo color. El árbol de decisión repite la historia desde el otro extremo: `max_depth=1` subajusta (66.7% de exactitud, solo separa *setosa*), `max_depth=3` es el óptimo de cross-validation (0.973), y pasado ese punto el árbol "sin límite" no gana capacidad real —el número de hojas se estanca en 8 desde `depth=5`— pero sí sobreajusta visiblemente: una pequeña isla en la frontera de decisión existe únicamente para clasificar bien un solo punto de entrenamiento.

---

### Clase 8 — Regresión

[`clase8-regresion/regresion_california_housing.ipynb`](clase8-regresion/regresion_california_housing.ipynb)

Comparación de regresión **lineal**, **polinomial** (grados 2 y 3) y **logarítmica**, con métricas, líneas de estimación y validación cruzada de 5 pliegues.

**Nota sobre el dataset.** El enunciado pedía Boston Housing y California Housing. Boston Housing fue eliminado de scikit-learn desde la versión 1.2 por un problema ético documentado: incluye una variable que codifica composición racial bajo un supuesto discriminatorio. Este notebook usa solo California Housing (20640 viviendas, 8 variables), el reemplazo estándar en cualquier curso actual.

Como una línea de estimación necesita un eje X, los cuatro modelos se ajustan primero sobre `MedInc` (ingreso medio de la zona), la variable más correlacionada con el precio:

| Modelo | R² | MAE | RMSE | R² (5-fold CV) |
|---|---|---|---|---|
| Lineal | 0.473 | 0.623 | 0.832 | 0.421 |
| Polinomial (grado 2) | 0.478 | 0.622 | 0.828 | 0.425 |
| Polinomial (grado 3) | 0.483 | 0.616 | 0.824 | 0.433 |
| Logarítmica | 0.451 | 0.646 | 0.849 | 0.392 |

La curva logarítmica y las polinomiales capturan que el precio sube rápido con el ingreso bajo y se aplana después, algo que una recta no puede reproducir por no poder doblarse.

**El hallazgo no pedido por el enunciado**: al repetir el experimento con las 8 variables completas, el polinomio de grado 2 rinde bien en una sola partición (R² 0.65) pero su validación cruzada explota a un R² medio de -25, con una desviación de 51. La causa es un outlier extremo en `AveOccup` (máximo de 1243 frente a un percentil 99 de apenas 5.4): al elevarlo al cuadrado, el modelo polinomial genera coeficientes disparatados en el pliegue donde ese dato cae. Escalar las variables no lo arregla, porque el escalado no le quita peso al outlier. Filtrando menos del 3% de las filas más extremas, la validación cruzada del polinomial se estabiliza (R² medio 0.658) y de paso mejora también al modelo lineal (0.610). La lección: entre más flexible es un modelo, más sensible es a la calidad de los datos que se le entregan.

---

## Cómo ejecutar los notebooks

Requieren `numpy`, `matplotlib` y `scikit-learn`:

```bash
pip install numpy matplotlib scikit-learn jupyterlab
jupyter lab
```

Todos los notebooks están guardados con sus salidas ya calculadas, así que también se pueden leer directamente en GitHub sin ejecutarlos.
