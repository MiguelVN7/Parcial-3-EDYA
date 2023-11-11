class Nodo:
    def __init__(self, id, nombre, latitud, longitud, altura):
        self.id = id
        self.nombre = nombre
        self.latitud = latitud
        self.longitud = longitud
        self.altura = altura

    def __str__(self):
        return f'[({self.id}) {self.nombre} | lon:{self.longitud} lat:{self.latitud})\t]'

class Arista:
    def __init__(self, nodo_inicio, nodo_destino, peso):
        self.nodo_inicio = nodo_inicio
        self.nodo_destino = nodo_destino
        self.peso = peso

    def __str__(self):
        return f'ARISTA [{self.nodo_inicio} --> {self.nodo_destino}:: w:{self.peso}]'

class GrafoDirigido:
    def __init__(self):
        self.nodos = {}     # diccionario "HashTable"
        self.aristas = []   # lista

    def agregar_nodo(self, nodo):
        self.nodos[nodo.id] = nodo

    def agregar_arista(self, nodo_inicio, nodo_destino, peso):
        if nodo_inicio.id in self.nodos and nodo_destino.id in self.nodos:
            arista = Arista(nodo_inicio, nodo_destino, peso)
            self.aristas.append(arista)

    def mostrar_grafo(self):
        for arista in self.aristas:
            print(f"{arista}")

    def encontrar_camino(self, inicio_id, destino_id, camino_actual=None):
        if camino_actual is None:
            camino_actual = []  # lista
        inicio = self.nodos.get(inicio_id)
        destino = self.nodos.get(destino_id)
        if inicio is None or destino is None:
            print("\nADVERTENCIA: Nodo de inicio o destino no encontrado en el grafo.")
            return
        camino_actual = camino_actual + [inicio]
        if inicio == destino:
            self.mostrar_camino(camino_actual)
            return
        for arista in self.aristas:
            if arista.nodo_inicio == inicio and arista.nodo_destino not in camino_actual:
                self.encontrar_camino(arista.nodo_destino.id, destino_id, camino_actual[:])

    def mostrar_camino(self, camino):
        if camino:
            print("\nCAMINO ENCONTRADO:")
            costo_total = 0
            for i in range(len(camino) - 1):
                arista = self.buscar_arista(camino[i].id, camino[i + 1].id)
                print(f"{arista.nodo_inicio.nombre} -> {arista.nodo_destino.nombre} (Peso: {arista.peso})")
                costo_total += arista.peso
            print(f"Costo total del camino: [{costo_total} Km]\n")
            print('-'*20)


    def buscar_arista(self, inicio_id, destino_id):
        for arista in self.aristas:
            if arista.nodo_inicio.id == inicio_id and arista.nodo_destino.id == destino_id:
                return arista


    def encontrar_todos_los_caminos(self, inicio_id, destino_id):
        if inicio_id not in self.nodos or destino_id not in self.nodos:
            print("Nodo de inicio o destino no encontrado en el grafo.")
            return

        def dfs(camino, nodo_actual, nodos_visitados):
            if nodo_actual.id == destino_id:
                caminos.append(camino[:])
            else:
                nodos_visitados.add(nodo_actual.id)
                for arista in self.aristas:
                    if arista.nodo_inicio.id == nodo_actual.id and arista.nodo_destino.id not in nodos_visitados:
                        camino.append(arista.nodo_destino.id)
                        dfs(camino, arista.nodo_destino, nodos_visitados)
                        camino.pop()
                nodos_visitados.remove(nodo_actual.id)

        caminos = []
        nodo_inicio = self.nodos.get(inicio_id)
        dfs([inicio_id], nodo_inicio, set())

        caminos_dict = {}
        for camino in caminos:
            peso_total = 0
            for i in range(len(camino) - 1):
                arista = self.buscar_arista(camino[i], camino[i + 1])
                peso_total += arista.peso
            caminos_dict[tuple(camino)] = peso_total

        return caminos_dict

    def encontrar_camino_mas_corto(self, inicio_id, destino_id):
        caminos = self.encontrar_todos_los_caminos(inicio_id, destino_id)
        if not caminos:
            print(f"No hay caminos entre {self.nodos[inicio_id].nombre} y {self.nodos[destino_id].nombre}.")
            return

        camino_mas_corto = min(caminos, key=caminos.get)
        peso_mas_corto = caminos[camino_mas_corto]

        print(f"\nEl camino más corto entre {self.nodos[inicio_id].nombre} y {self.nodos[destino_id].nombre} es:")
        for i in range(len(camino_mas_corto) - 1):
            arista = self.buscar_arista(camino_mas_corto[i], camino_mas_corto[i + 1])
            print(
                f"{self.nodos[arista.nodo_inicio.id].nombre} -> {self.nodos[arista.nodo_destino.id].nombre} (Peso: {arista.peso} Km)")
        print(f"Costo total del camino más corto: {peso_mas_corto} Km")


    def encontrar_camino_ida_vuelta(self, inicio_id, destino_id):
        caminos_ida = self.encontrar_todos_los_caminos(inicio_id, destino_id)
        caminos_vuelta = self.encontrar_todos_los_caminos(destino_id, inicio_id)

        if not caminos_ida:
            print(f"No hay camino de ida desde {self.nodos[inicio_id].nombre} a {self.nodos[destino_id].nombre}.")
        else:
            print(f"Camino(s) de ida desde {self.nodos[inicio_id].nombre} a {self.nodos[destino_id].nombre}:")
            print()
            for camino in caminos_ida:
                self.imprimir_camino(camino)

        if not caminos_vuelta:
            print(f"No hay camino de vuelta desde {self.nodos[destino_id].nombre} a {self.nodos[inicio_id].nombre}.")
        else:
            print(f"\nCamino(s) de vuelta desde {self.nodos[destino_id].nombre} a {self.nodos[inicio_id].nombre}:")
            print()
            for camino in caminos_vuelta:
                self.imprimir_camino(camino)

    def imprimir_camino(self, camino):
        peso_total = 0
        for i in range(len(camino) - 1):
            peso_total += self.buscar_arista(camino[i], camino[i + 1]).peso
            arista = self.buscar_arista(camino[i], camino[i + 1])
            print(
                f"{self.nodos[arista.nodo_inicio.id].nombre} -> {self.nodos[arista.nodo_destino.id].nombre} (Peso: {arista.peso} Km)")
        print(f"Costo total del camino: {peso_total} Km")
        print('-'*20)




if __name__ == "__main__":
    grafo = GrafoDirigido()

    avila = Nodo("1", "Ávila", 40.655071, -4.70100, 1132)
    segovia = Nodo("2", "Segovia", 40.942903, -4.123201, 1000)
    guadalajara = Nodo("3", "Guadalajara", 40.633190, -3.163360, 708)
    madrid = Nodo("4", "Madrid", 40.416775, -3.703790, 667)
    toledo = Nodo("5", "Toledo", 39.858938, -4.024472, 529)

    grafo.agregar_nodo(avila)
    grafo.agregar_nodo(segovia)
    grafo.agregar_nodo(guadalajara)
    grafo.agregar_nodo(madrid)
    grafo.agregar_nodo(toledo)

    grafo.agregar_arista(avila, guadalajara, 171)
    grafo.agregar_arista(segovia, avila, 64.3)
    grafo.agregar_arista(segovia, guadalajara, 153)
    grafo.agregar_arista(segovia, madrid, 91.6)
    grafo.agregar_arista(guadalajara, madrid, 66.6)
    grafo.agregar_arista(guadalajara, avila, 193)
    grafo.agregar_arista(madrid, segovia, 97.3)
    grafo.agregar_arista(madrid, guadalajara, 59.4)
    grafo.agregar_arista(madrid, toledo, 72.5)
    grafo.agregar_arista(toledo, madrid, 81.2)
    grafo.agregar_arista(toledo, segovia, 159)
    grafo.agregar_arista(toledo, avila, 113)



    grafo.mostrar_grafo()
    print("-"*20)
    print("\nBUSCAR CAMINOS: \n")

    estado = True
    while estado:
        inicio_id = input("ID de nodo de inicio: ")
        destino_id = input("ID de nodo de destino: ")

        grafo.encontrar_camino(inicio_id, destino_id)

        print("\n\n\nBUSCAR CAMINO MAS CORTO:")
        grafo.encontrar_camino_mas_corto(inicio_id, destino_id)

        print("\n\n\nBUSCAR CAMINOS IDA Y VUELTA: \n")
        grafo.encontrar_camino_ida_vuelta(inicio_id, destino_id)


        resp = input("\n¿Desea continuar? (S/N): ").strip().upper()
        if resp=='S':
            estado = True
        else:
            estado = False