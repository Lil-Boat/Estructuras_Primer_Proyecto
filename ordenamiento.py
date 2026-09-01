class ordenamiento:
    """
    Clase que implementa diferentes algoritmos de ordenamiento optimizados.
    Puede ser utilizada de forma reutilizable en diferentes proyectos.
    """

    def __init__(self, lista=None):
        """Inicializa con una lista opcional"""
        self.lista = lista if lista else []

    def shortBurbuja(self, lista=None, ascendente=True):
        """
        Bubble Sort Optimizado (Short Bubble).
        
        Args:
            lista: Lista a ordenar. Si no se proporciona, usa self.lista
            ascendente: True para orden ascendente, False para descendente
            
        Retorna:
            Lista ordenada
            
        Complejidad:
            - Mejor caso: O(n)
            - Promedio/Peor: O(n²)
            - Espacio: O(1)
        """
        datos = lista if lista else self.lista
        n = len(datos)
        
        for i in range(n):
            intercambio = False
            for j in range(0, n - i - 1):
                # Comparación según orden
                condicion = datos[j] > datos[j + 1] if ascendente else datos[j] < datos[j + 1]
                
                if condicion:
                    datos[j], datos[j + 1] = datos[j + 1], datos[j]
                    intercambio = True
                    
            if not intercambio:
                break
                
        return datos

    def MergeSort(self, lista=None, ascendente=True):
        """
        Merge Sort (Divide y Vencerás).
        
        Args:
            lista: Lista a ordenar. Si no se proporciona, usa self.lista
            ascendente: True para orden ascendente, False para descendente
            
        Retorna:
            Lista ordenada
            
        Complejidad:
            - Temporal: O(n log n) en todos los casos
            - Espacial: O(n)
        """
        datos = lista if lista else self.lista
        self.ascendente = ascendente  # Guardar para usar en _merge
        
        if len(datos) <= 1:
            return datos

        mid = len(datos) // 2
        L = self.MergeSort(datos[:mid], ascendente)
        R = self.MergeSort(datos[mid:], ascendente)

        return self._merge(L, R)

    def _merge(self, izquierda, derecha):
        """Fusiona dos listas ordenadas"""
        resultado = []
        i = j = 0
        len_izq, len_der = len(izquierda), len(derecha)

        while i < len_izq and j < len_der:
            # Comparación según orden (ascendente o descendente)
            if self.ascendente:
                condicion = izquierda[i] <= derecha[j]
            else:
                condicion = izquierda[i] >= derecha[j]
                
            if condicion:
                resultado.append(izquierda[i])
                i += 1
            else:
                resultado.append(derecha[j])
                j += 1

        resultado.extend(izquierda[i:])
        resultado.extend(derecha[j:])
        return resultado
    
    def obtener_lista(self):
        """Retorna la lista actual"""
        return self.lista
    
    def establecer_lista(self, lista):
        """Establece una nueva lista"""
        self.lista = lista
    def quickSort(self, lista=None, ascendente=True):
        """
        Quick Sort (Divide y Vencerás).
        
        Args:
            lista: Lista a ordenar. Si no se proporciona, usa self.lista
            ascendente: True para orden ascendente, False para descendente
            
        Retorna:
            Lista ordenada
            
        Complejidad:
            - Mejor caso: O(n log n)
            - Promedio: O(n log n)
            - Peor caso: O(n²)
            - Espacio: O(log n) debido a la recursión
        """
        datos = lista if lista else self.lista
        
        if len(datos) <= 1:
            return datos
        
        pivot = datos[len(datos) // 2]
        left = [x for x in datos if (x < pivot if ascendente else x > pivot)]
        middle = [x for x in datos if x == pivot]
        right = [x for x in datos if (x > pivot if ascendente else x < pivot)]
        
        return self.quickSort(left, ascendente) + middle + self.quickSort(right, ascendente)