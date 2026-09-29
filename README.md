# Matemática Computacional 💻 - Grupo 2

| Integrantes |
| ----------- |
| Luis Enrique Sedano Barreda |
| Carlos Orlando Horna Cueva |
| Angela Bibiana Cóndor Velásquez |
| Johan Micael Quispe Laura |
| Adrian Alejandro Leon Ojeda |

## Caso del proyecto

**Caso 2: Problema del camino mínimo**

Desarrolle un programa que resuelva el problema del camino mínimo en un grafo ponderado.

El programa deberá solicitar al usuario el número de vértices 𝑛, con _5 ≤ 𝑛 ≤ 15_, y ofrecer dos opciones para construir la matriz de adyacencia ponderada de tamaño 𝑛 × 𝑛:

- Generación automática: crear aleatoriamente una matriz cuyos elementos
sean pesos no negativos, representando las aristas del grafo.
- Ingreso manual: permitir que el usuario introduzca los pesos de la matriz.

Una vez construida la matriz, el programa deberá generar y mostrar el grafo ponderado correspondiente.

Posteriormente, el usuario seleccionará un vértice de origen y un vértice de destino, y el programa determinará el camino mínimo entre ambos, indicando la secuencia de vértices que lo conforman, el costo total del recorrido y el desarrollo paso a paso del algoritmo empleado para obtener la
solución.

## Ensayo escrito

https://docs.google.com/document/d/1fkgKkOlmoDAklxEF-dcQPGk53CMKxI-PJQ0BN2SKPco/edit?usp=sharing

## Presentación

```
(Colocar link del Canva)
```

## Estructura del proyecto

```text
└── aleon30-matematica-computacional/
    ├── .gitignore             # Archivos ignorados por Git (pycache y .vscode)
    ├── Grafo.py               # Implementación de la clase Grafo
    ├── README.md              # Resumen del proyecto, archivos y documentación
    ├── dibujarGrafo.py        # Visualización del grafo
    ├── main.py                # Ejecutable principal
    ├── requirements.txt       # Dependencias del proyecto
    └── assets/ 
        └── diagrama_flujo.png   # Diagrama de flujo del proyecto
```

<img src="assets/diagrama_flujo.png">

## Requisitos

Este proyecto está desarrollado para ejecutarse localmente con:

- Python 3.11

### Dependencias principales

| Librería | Versión recomendada | Uso dentro del proyecto |
| --- | --- | --- |
| `networkx` | `>= 3.4.2` | Modelización del grafo |
| `matplotlib` | `>= 3.10.0` | Visualización del grafo |

### Instalación local

Puedes instalar las dependencias usando el archivo `requirements.txt` en la terminal:

```bash
pip install -r requirements.txt
```