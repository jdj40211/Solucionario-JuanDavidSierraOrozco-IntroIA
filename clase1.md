# Actividad de Clase: Analizando Agentes de IA con Hugging Face Spaces

## Objetivo

Explorar aplicaciones reales de Inteligencia Artificial en **Hugging
Face Spaces** y analizarlas desde la perspectiva de los **agentes
racionales**.

Al finalizar la actividad, los estudiantes deberán ser capaces de:

-   Identificar los componentes **PEAS** de un agente.
-   Clasificar las propiedades del entorno.
-   Proponer qué tipo de programa de agente podría implementarse detrás
    del sistema.
-   Justificar sus respuestas.

------------------------------------------------------------------------

## Instrucciones

1.  Ingresen a **https://huggingface.co/spaces**.
2.  Exploren diferentes Spaces.
3.  Seleccionen uno que les parezca interesante.
4.  Interactúen con el sistema durante algunos minutos.
5.  Completen la siguiente ficha de análisis.

------------------------------------------------------------------------

# Ficha de análisis

## 1. Nombre del Space 

**Nombre: Z-Image-Turbo**

**Enlace:** https://huggingface.co/spaces/mrfakename/Z-Image-Turbo

------------------------------------------------------------------------

## 2. ¿Qué hace el agente?

Es una herramienta de generación de imagenes a partir de texto

------------------------------------------------------------------------

## 3. Análisis PEAS

  Elemento          Respuesta
  ----------------- ----------------------------------------------------
  **Performance**   Genera imagenes a partir de texto
  **Environment**   Imagenes de referencia y texto
  **Actuators**     Imagenes generadas
  **Sensors**       Datos de texto e imagenes de referencia

------------------------------------------------------------------------

## 4. Clasificación del entorno

Complete la siguiente tabla y justifique brevemente cada respuesta.

  Propiedad      Clasificación     Justificación
  -------------- ----------------- ---------------
  Observable     Es parcial porque solo se ve la imagen generada 
  Determinista   No, porque la misma descripcion puede generar diferentes imagenes
  Episódico      No, porque la misma descripcion puede generar diferentes imagenes
  Estático       No, porque se pueden generar diferentes imagenes a partir de la misma descripcion
  Discreto       No, porque se pueden generar diferentes imagenes a partir de la misma descripcion
  Conocido       Sí, porque se puede generar diferentes imagenes a partir de la misma descripcion

------------------------------------------------------------------------

## 5. ¿Qué tipo de programa de agente creen que es?

Seleccione la opción que consideren más adecuada y explique por qué.

-   Agente de reflejo simple
-   Agente basado en modelo
-   Agente basado en objetivos
-   Agente basado en utilidad
-   Agente con aprendizaje

Respuesta: Agente con aprendizaje, porque se puede aprender a generar mejores imagenes a partir de la misma descripcion

> **Importante:** No existe una única respuesta correcta. Lo importante
> es justificar la elección a partir del comportamiento observado.

------------------------------------------------------------------------

# Discusión en clase

Después de las presentaciones, discutiremos preguntas como:

-   ¿Dos Spaces diferentes pueden compartir el mismo tipo de entorno?
-   ¿Es posible saber con certeza qué tipo de agente implementa un Space
    únicamente observándolo?
-   ¿Qué diferencia existe entre el comportamiento observable de un
    agente y su implementación interna?

------------------------------------------------------------------------

# Reto adicional

Encuentre un Space que pueda clasificarse como:

1.  **Totalmente observable, determinista y episódico.**

   -   Respuesta: 
        - **Nombre:** Sudoku Solver AI
        - **Enlace:** https://huggingface.co/spaces/adrian/sudoku-solver
        - **Clasificación:** Totalmente observable, determinista y episódico
    
    -   Justificación: 
        - **Totalmente observable:** Toda la información del tablero está disponible a la vista del agente sin información oculta.
        - **Determinista:** La aplicación de las reglas sobre el estado actual produce siempre el mismo resultado exacto sin aleatoriedad.
        - **Episódico:** La resolución de cada tablero es independiente de las partidas o ejecuciones previas.
2.  **Parcialmente observable, estocástico y secuencial.**
    -   Respuesta: 
        - **Nombre:** Texas Hold'em Poker Agent
        - **Enlace:** https://huggingface.co/spaces/poker-ai/texas-holdem
        - **Clasificación:** Parcialmente observable, estocástico y secuencial
    -   Justificación: 
        - **Parcialmente observable:** El agente no conoce las cartas ocultas de sus oponentes ni la estrategia interna no expuesta.
        - **Estocástico:** El reparto aleatorio de cartas y el comportamiento variado de otros jugadores introduce impredecibilidad.
        - **Secuencial:** Cada apuesta o acción condiciona el pozo, las fichas y los movimientos posibles en los siguientes turnos de la misma mano.

    -   Justificación: 

------------------------------------------------------------------------

# Rúbrica (10 puntos)

| Criterio | Puntos |
|-----------|:------:|
| Descripción correcta del Space | 2 |
| Identificación de PEAS | 3 |
| Clasificación del entorno | 3 |
| Justificación del tipo de agente | 2 |
| **Total** | **10** |

------------------------------------------------------------------------
