# Función para eliminar recursividad por la izquierda
def eliminar_recursividad_izquierda(gramatica):
    nueva_gramatica = {}
    for nt, producciones in gramatica.items():
        recursivas = []
        no_recursivas = []
        for produccion in producciones:
            if produccion[0] == nt:
                recursivas.append(produccion[1:])
            else:
                no_recursivas.append(produccion)
        
        if recursivas:
            nuevo_nt = nt + "'"
            nueva_gramatica[nt] = [p + [nuevo_nt] for p in no_recursivas]
            nueva_gramatica[nuevo_nt] = [p + [nuevo_nt] for p in recursivas] + [['ε']]
        else:
            nueva_gramatica[nt] = producciones
    return nueva_gramatica

# Función para calcular los conjuntos First
def calcular_primeros(gramatica):
    primeros = {nt: set() for nt in gramatica}

    def primeros_de(produccion):
        primeros_set = set()
        for simbolo in produccion:
            if simbolo in gramatica:  # Es un no terminal
                primeros_set.update(primeros[simbolo])
                if 'ε' not in primeros[simbolo]:
                    break
            else:
                primeros_set.add(simbolo)
                break
        return primeros_set

    cambio = True
    while cambio:
        cambio = False
        for nt, producciones in gramatica.items():
            for produccion in producciones:
                nuevos_primeros = primeros_de(produccion)
                if not nuevos_primeros.issubset(primeros[nt]):
                    primeros[nt].update(nuevos_primeros)
                    cambio = True
    return primeros

# Función para calcular los conjuntos Follow
def calcular_siguientes(gramatica, primeros):
    siguientes = {nt: set() for nt in gramatica}
    siguientes['S'].add('$')  # Añadir símbolo de fin de cadena

    def primeros_de(produccion):
        primeros_set = set()
        for simbolo in produccion:
            if simbolo in gramatica:
                primeros_set.update(primeros[simbolo])
                if 'ε' not in primeros[simbolo]:
                    break
            else:
                primeros_set.add(simbolo)
                break
        return primeros_set

    def seguir_a(no_terminal):
        for nt, producciones in gramatica.items():
            for produccion in producciones:
                if no_terminal in produccion:
                    idx = produccion.index(no_terminal)
                    siguiente_parte = produccion[idx + 1:]
                    if siguiente_parte:
                        siguientes[no_terminal].update(primeros_de(siguiente_parte) - {'ε'})
                    if not siguiente_parte or 'ε' in primeros_de(siguiente_parte):
                        siguientes[no_terminal].update(siguientes[nt])

    cambio = True
    while cambio:
        cambio = False
        for nt in gramatica:
            conjunto_anterior = siguientes[nt].copy()
            seguir_a(nt)
            if conjunto_anterior != siguientes[nt]:
                cambio = True

    return siguientes

# Función para calcular predicciones
def calcular_predicciones(gramatica, primeros, siguientes):
    def primeros_de(produccion):
        primeros_set = set()
        for simbolo in produccion:
            if simbolo in gramatica:
                primeros_set.update(primeros[simbolo])
                if 'ε' not in primeros[simbolo]:
                    break
            else:
                primeros_set.add(simbolo)
                break
        return primeros_set

    predicciones = {}
    for nt, producciones in gramatica.items():
        for produccion in producciones:
            if 'ε' in primeros_de(produccion):
                predicciones[(nt, tuple(produccion))] = (primeros_de(produccion) - {'ε'}) | siguientes[nt]
            else:
                predicciones[(nt, tuple(produccion))] = primeros_de(produccion)
    return predicciones

