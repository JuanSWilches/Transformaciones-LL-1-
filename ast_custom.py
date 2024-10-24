# Clase para el nodo del Árbol de Sintaxis Abstracta (AST)
class NodoAST:
    def __init__(self, valor):
        self.valor = valor
        self.hijos = []

    def agregar_hijo(self, nodo):
        self.hijos.append(nodo)

# Función para crear el AST
def crear_ast(gramatica):
    raiz = NodoAST('S')  # Empezar desde el símbolo inicial
    crear_ast_recursivo(raiz, 'S', gramatica)
    return raiz

# Función recursiva para crear el AST
def crear_ast_recursivo(nodo, no_terminal, gramatica, visitados=None):
    if visitados is None:
        visitados = set()
    
    # Evitar recursión infinita detectando si ya se ha visitado este no terminal
    if no_terminal in visitados:
        return
    
    visitados.add(no_terminal)
    
    if no_terminal in gramatica:
        producciones = gramatica[no_terminal]
        
        # Procesar cada producción
        for produccion in producciones:
            for simbolo in produccion:
                nuevo_nodo = NodoAST(simbolo)
                nodo.agregar_hijo(nuevo_nodo)
                
                # Llamar recursivamente solo si es un no terminal
                if simbolo in gramatica:
                    crear_ast_recursivo(nuevo_nodo, simbolo, gramatica, visitados.copy())

# Función para imprimir el AST
def imprimir_ast(nodo, nivel=0):
    print("  " * nivel + str(nodo.valor))
    for hijo in nodo.hijos:
        imprimir_ast(hijo, nivel + 1)

