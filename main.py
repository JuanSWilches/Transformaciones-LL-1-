import sys
import grammar as gr
import ast_custom as ast_module  # Cambié ast por ast_custom para evitar conflicto

# Clase para Nodo del Árbol de Derivación por la Derecha (ASDR)
class NodoASDR:
    def __init__(self, valor):
        self.valor = valor
        self.hijos = []

    def agregar_hijo(self, nodo):
        self.hijos.append(nodo)

# Función para crear el ASDR para un no terminal
def crear_asdr(no_terminal, gramatica):
    raiz = NodoASDR(no_terminal)
    if no_terminal in gramatica:
        produccion = gramatica[no_terminal][-1]  # Derivación por la derecha (última producción)
        for simbolo in produccion:
            if simbolo in gramatica:
                hijo = crear_asdr(simbolo, gramatica)  # Recursión para no terminales
            else:
                hijo = NodoASDR(simbolo)  # Terminales como hojas
            raiz.agregar_hijo(hijo)
    return raiz

# Función para imprimir el ASDR
def imprimir_asdr(nodo, nivel=0):
    print("  " * nivel + str(nodo.valor))
    for hijo in nodo.hijos:
        imprimir_asdr(hijo, nivel + 1)

# Función para verificar si la gramática es LL(1)
def es_ll1(predicciones):
    for (nt, produccion), conjunto_prediccion in predicciones.items():
        for (nt_otro, produccion_otro), conjunto_prediccion_otro in predicciones.items():
            if nt == nt_otro and produccion != produccion_otro:
                if conjunto_prediccion.intersection(conjunto_prediccion_otro):
                    print(f"Conflicto entre producciones {produccion} y {produccion_otro} para el no terminal {nt}")
                    return False
    return True

def main(archivo):
    with open(archivo, 'r') as f:
        lineas = f.readlines()

    # Ejemplo de gramática
    gramatica = {
        "S": [["A", "a"], ["B", "b"], ["c"]],
        "A": [["A", "d"], ["e"]],
        "B": [["f"], ["g"]]
    }

    print("Gramática original:")
    print(gramatica)

    # Eliminar recursividad por la izquierda
    gramatica_sin_recursividad = gr.eliminar_recursividad_izquierda(gramatica)
    print("\nGramática después de eliminar recursividad por la izquierda:")
    print(gramatica_sin_recursividad)

    # Calcular conjuntos First y Follow
    primeros = gr.calcular_primeros(gramatica_sin_recursividad)
    print("\nPrimeros:")
    for nt, valores in primeros.items():
        print(f"Primeros({nt}): {valores}")

    siguientes = gr.calcular_siguientes(gramatica_sin_recursividad, primeros)
    print("\nSiguientes:")
    for nt, valores in siguientes.items():
        print(f"Siguientes({nt}): {valores}")

    # Calcular predicciones
    predicciones = gr.calcular_predicciones(gramatica_sin_recursividad, primeros, siguientes)
    print("\nPredicciones:")
    for clave, valores in predicciones.items():
        print(f"Predicciones({clave[0]} -> {' '.join(clave[1])}): {valores}")

    # Verificar si la gramática es LL(1)
    if es_ll1(predicciones):
        print("\nLa gramática es LL(1).")
    else:
        print("\nLa gramática NO es LL(1).")

    # Construir y mostrar el Árbol de Derivación por la Derecha (ASDR)
    asdr_raiz = crear_asdr('S', gramatica_sin_recursividad)
    print("\nÁrbol de Derivación por la Derecha (ASDR):")
    imprimir_asdr(asdr_raiz)

    # Mostrar el Árbol de Sintaxis Abstracta (AST)
    print("\nÁrbol de Sintaxis Abstracta (AST):")
    ast_raiz = ast_module.crear_ast(gramatica_sin_recursividad)
    ast_module.imprimir_ast(ast_raiz)

if __name__ == "__main__":
    main(sys.argv[1])

