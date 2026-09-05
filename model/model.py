"""regola view --> C--> M--> DAO.database"""
import networkx as nx

"""la logica/i metodi li definisco nel model """

from database.DAO import DAO


class Model:
    def __init__(self):
        #crea grafo vuoto per poi aggiugnere nodi e archi durnate "build graph"
        self._idMap ={}
        self._graph = nx.Graph()
    def getRatings(self):
        return DAO.getAllRatings()
      #il metodo deve sapere che argomenti sta ricevendo da controller,il rating che chiameremo, rat1 2 rat2"""
    def buildGraph(self,rat1,rat2):
        self._graph.clear()
        #self._actor variabile interna alla classe
        #viene inizializzato come lista vuota (successivamente riempiremo con lista di oggeti actor)
        #in output Actors dei film che rientrano nel range (nodi filtrati per range)
        self._actors = DAO.getAllActorsbyRange(rat1, rat2)

        #variabile a è un oggetto di tipo Actor (preso da self._actors)
        for a in self._actors:
            self._idMap[a.ActorID] = a
        #inserisce attori come nodi del grafo
        self._graph.add_nodes_from(self._actors)
        #resituisce tutte le coppie di attori e il loro peso (ID e pesi)
        #funzione() quello tra parentesi lo usa come input
        #e in output avrò (a1,a2,e w)
        self._edges=DAO.getAllEdges(rat1, rat2)
        #creiamo una lista di tuple (a1,a2,w) con ciclo for
        #con _idMap mappo ogni ActorID all'oggetto Attore corrispondente,
        #così posso creare archi esistenti,usando i pesi forniti dalDB
        for e1,e2,w in self._edges:
            self._graph.add_edge(self._idMap[e1],self._idMap[e2],weight=w)

#legge solo il numero di nodi (quanti attori ci sono)
    def getNumNodi(self):
        return len(self._graph.nodes())
 #legge il numero di archi (relazioni comuni tra attori)  
    def getNumEdges(self):
        return len(self._graph.edges())
#visualizza i 5 archi di peso maggiore
    def getTop5Edges(self):
        #dammi tutti gli archi del grafo (self._graph.) insieme ai loro dati, quindi anche il weight
        #(Actor1, Actor2, {"weight": 5000000}) , che sono posizione 0,1,2

        #NOTA:self._edges = dati degli archi ricevuti dal DAO.
        #self._graph.edges(...) = archi effettivamente presenti nel grafo NetworkX.
        edges=sorted(self._graph.edges(data=True), #SORTED ORDINA ARCHI IN BASE AL WEIGHT
                     key=lambda e: e[2]['weight'], #che cosa? variabile peso posizione [2][weight]
                     reverse=True #dal max al min (top 5 di peso maggiore)
                     )
        return edges[:5] #ATTENZIONE POSZIONE 5 ESCLUSA
    #   quindi edges = [A, B, C, D, E, F, G] resituisce [A, B, C, D, E] ($)

#PER DEFINIRE LE COMPONENTI CONNESSE IL MODEL INTERROGA (nx.connected_components(self._graph))
    #individua tutti i gruppi di nodi collegati tra loro
    #con list trasformiamo in una lista :components = [
   # {A, B, C},
  #  {D, E},
 #   {F}
#     ]
    def getCompConness(self):
        comp= list(nx.connected_components(self._graph))
        return comp
    def getLargestComp(self, comp):
        largest = max(comp,key=len) # scegli il max (confronta le componenti in base alla loro lunghezza ($))
        return largest
        




