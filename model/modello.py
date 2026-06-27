import copy

from database.DAO import DAO
import networkx as nx

from model.arco import Arco


class Model:
    def __init__(self):
        self._G = nx.Graph()
        self._nodi = []
        self._Dnodi = {}
        self._archi = []


    def creaGrafo(self, v1, v2, shape):
        self._G = nx.Graph()
        self._nodi = DAO.getNodi(v1, v2, shape)
        self._Dnodi = {}
        self._archi = []
        self._G.add_nodes_from(self._nodi)
        for element in self._nodi:
            element.densita()
            self._Dnodi[element.id.upper()] = element
        lista = DAO.getArchi(v1, v2, shape)
        for element in lista:
            n1 = self._Dnodi[element[0]]
            n2 = self._Dnodi[element[1]]
            peso = element[2]
            arco = Arco(n1, n2, peso)
            self._archi.append(arco)
            self._G.add_edge(n1, n2, weight= peso)
        stringa = f"Numero di vertici:{self._G.number_of_nodes()}\nNumero di archi:{self._G.number_of_edges()}\n\nI 5 nodi di grado maggiore sono:"
        lista = sorted(self._nodi, key = lambda n:self._G.degree(n), reverse = True)
        for i in range(min(len(lista), 5)):
            stringa =stringa + "\n" + lista[i].__str__() + f"-> {self._G.degree(lista[i])}"
        stringa = stringa + f"\n5 archi di peso maggiore sono:"
        self._archi.sort(reverse=True)
        for j in range(min(len(self._archi), 5)):
            stringa = stringa + "\n" + self._archi[j].__str__()
        return stringa


    def forme(self):
        lista = DAO.getShape()
        return lista

    def maxMin(self):
        lista = DAO.getVal()
        return lista
    def calcolaPunteggio(self, lista):
        if len(lista) == 0 or len(lista) == 1:
            return 0
        totale = 0
        for i in range(len(lista)-1):
            n1 = lista[i]
            n2 = lista[i+1]
            punteggio = self._G[n1][n2]["weight"]
            distanza = n1.distance_HV(n2)
            totale = totale + punteggio/distanza
        return totale

    def percorso(self):
        self._cammino = []
        self._top = 0
        for element in self._nodi:
            parziale = [element]
            self.itera(parziale)
        stringa = f"Percorso massimo con {self._top}"
        for element in self._cammino:
            stringa = stringa + "\n" + element.__str__() + f": {str(element.d)}"
        return stringa



    def itera(self, parziale):
        if self.calcolaPunteggio(parziale)>self._top:
            self._top = self.calcolaPunteggio(parziale)
            self._cammino = copy.deepcopy(parziale)
        ultimo = parziale[-1]
        for element in self._G.neighbors(ultimo):
            if element not in parziale:
                if element.d>ultimo.d:
                    parziale.append(element)
                    self.itera(parziale)
                    parziale.pop()



