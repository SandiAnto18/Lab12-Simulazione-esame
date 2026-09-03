"""regola view --> C--> M--> DAO.database"""
import networkx as nx

"""la logica/i metodi li definisco nel model """

from database.DAO import DAO


class Model:
    def __init__(self):
        #crea grafo vuoto per poi aggiugnere nodi e archi durnate "build graph"
        self._graph = nx.Graph()
    def getRatings(self):
        return DAO.getAllRatings()
      #il metodo deve sapere che argomenti sta ricevendo da controller,il rating che chiameremo, rat1 2 rat2"""
    def buildGraph(self,rat1,rat2):
        self._graph.clear()
        #self._ variabile interna alla classe"""
        self._actors = DAO.getAllActorsbyRange(rat1, rat2)

#legge solo il numero di nodi (quanti attori ci sono)
    def getNumNodi(self):
        return len(self._graph.nodes())
 #legge il numero di archi (relazioni comuni tra attori)  
    def getNumEdges(self):
        return len(self._graph.edges())



