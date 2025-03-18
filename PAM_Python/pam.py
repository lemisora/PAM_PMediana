class PAM:
    def __init__(self):
        self.d = None  # Matriz de disimilitud
        self.nObjects = 0  # Número de objetos
        self.k = 0  # Número de clusters
        self.medoid = None  # Centroides
        self.sClusters = None  # Estructura de clusters
        self.kClusters = None  # Grupos de clusters
        self.dCostoSolucion = 0  # Costo de la solución

    # Estructura para almacenar clusters
    class Clusters:
        def __init__(self):
            self.item = 0  # Objeto
            self.cluster = 0  # Cluster al que pertenece

    # Estructura para almacenar grupos
    class Group:
        def __init__(self):
            self.items = []  # Elementos del cluster
            self.n = 0  # Número de elementos

    # Algoritmo PAM
    def pam(self, nclusters):
        self.k = nclusters
        self.kClusters = [self.Group() for _ in range(self.k)]
        self.sClusters = [self.Clusters() for _ in range(self.nObjects)]
        self.medoid = [0] * self.k

        self.calculateM1()  # Calcular el primer centroide
        for i in range(1, self.k):
            self.buildInitMedoids(i)  # Calcular el resto de los centroides

        self.stepSwap()  # Intercambio de centroides
        self.calculateClusters()  # Calcular los clusters

    # Calcula el primer centroide
    def calculateM1(self):
        m1 = 0
        smallest = float('inf')
        for i in range(self.nObjects):
            sum_val = 0
            for j in range(self.nObjects):
                sum_val += self.d[i][j]
            if sum_val < smallest:
                smallest = sum_val
                m1 = i
        self.medoid[0] = m1

    # Construye los centroides iniciales
    def buildInitMedoids(self, i):
        smallest = float('inf')
        m = 0
        for obj in range(self.nObjects):
            if not self.inMedoids(obj, self.medoid):
                self.medoid[i] = obj
                sum_val = 0
                for j in range(self.nObjects):
                    if not self.inMedoids(j, self.medoid):
                        sum_val += self.dMinimal(j, self.medoid, i)
                if sum_val < smallest:
                    m = obj
                    smallest = sum_val
        self.medoid[i] = m

    # Verifica si un objeto es un centroide
    def inMedoids(self, obj, m):
        for i in range(self.k):
            if obj == m[i]:
                return True
        return False

    # Devuelve la disimilitud mínima de un objeto a los centroides
    def dMinimal(self, obj, m, n):
        minimal = self.d[obj][m[0]]
        for i in range(1, n):
            if self.d[obj][m[i]] < minimal:
                minimal = self.d[obj][m[i]]
        return minimal

    # Intercambio de centroides
    def stepSwap(self):
        centroid = [0] * self.k
        v = [0] * (self.nObjects - self.k)
        minimal = self.objectiveFunction(self.medoid)
        i = 0
        while i < self.k:
            centroid = self.medoid.copy()
            self.setNoMedoids(v)
            n = self.nObjects - self.k
            ret = False
            for j in range(n):
                centroid[i] = v[j]
                totald = self.objectiveFunction(centroid)
                if totald < minimal:
                    self.medoid[i] = v[j]
                    minimal = totald
                    ret = True
            if ret and i != 0:
                self.moveInitPos(self.medoid, i)
                i = 1
            else:
                i += 1
        self.dCostoSolucion = minimal

    # Función objetivo
    def objectiveFunction(self, m):
        sum_val = 0
        for i in range(self.nObjects):
            if not self.inMedoids(i, m):
                sum_val += self.dMinimal(i, m, self.k)
        return sum_val

    # Copia los objetos que no son centroides
    def setNoMedoids(self, v):
        n = 0
        for i in range(self.nObjects):
            if not self.inMedoids(i, self.medoid):
                v[n] = i
                n += 1

    # Mueve un centroide a la posición inicial
    def moveInitPos(self, m, pos):
        aux = [0] * self.k
        j = 1
        for i in range(self.k):
            if i == pos:
                aux[0] = m[i]
            else:
                aux[j] = m[i]
                j += 1
        for i in range(self.k):
            m[i] = aux[i]

    # Calcula los clusters
    def calculateClusters(self):
        v = [0] * (self.nObjects - self.k)
        self.setNoMedoids(v)
        pos = 0
        for i in range(self.nObjects - self.k):
            min_val = self.d[v[i]][self.medoid[0]]
            g = 0
            for j in range(1, self.k):
                if self.d[v[i]][self.medoid[j]] < min_val:
                    min_val = self.d[v[i]][self.medoid[j]]
                    g = j
            self.kClusters[g].n += 1
            self.sClusters[pos].cluster = g
            self.sClusters[pos].item = v[i]
            pos += 1
        for i in range(self.k):
            self.sClusters[pos].cluster = i
            self.sClusters[pos].item = self.medoid[i]
            pos += 1
        for i in range(self.k):
            self.kClusters[i].items = [0] * (self.kClusters[i].n + 1)
            self.getCluster(i, self.kClusters[i].items, self.kClusters[i].n)

    # Obtiene los elementos de un cluster
    def getCluster(self, noCluster, items, noItems):
        items[0] = self.medoid[noCluster]
        pos = 1
        for i in range(self.nObjects - self.k):
            if self.sClusters[i].cluster == noCluster:
                items[pos] = self.sClusters[i].item
                pos += 1
        noItems = pos - 1
