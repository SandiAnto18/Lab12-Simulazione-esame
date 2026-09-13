"""REGOLA: VIEW → CONTROLLER → MODEL → DAO → DATABASE"""

import networkx as nx

from database.DAO import DAO


class Model:

    def __init__(self):
        # CREO UN DIZIONARIO CHE ASSOCIA OGNI ACTORID AL RELATIVO OGGETTO ACTOR
        # ESEMPIO: 10 → OGGETTO ACTOR CON ID 10
        self._idMap = {}

        # CREO IL GRAFO VUOTO
        # GLI ATTORI SARANNO I NODI E LE RELAZIONI TRA ATTORI GLI ARCHI
        self._graph = nx.Graph()


    # RECUPERO TUTTI I RATING DISPONIBILI DAL DATABASE
    def getRatings(self):
        return DAO.getAllRatings()


    # COSTRUISCO IL GRAFO USANDO IL RANGE DI RATING SCELTO DALL'UTENTE
    def buildGraph(self, rat1, rat2):

        # PULISCO IL GRAFO NEL CASO VENGA COSTRUITO NUOVAMENTE
        self._graph.clear()

        # PULISCO ANCHE LA MAPPA DEGLI ATTORI
        self._idMap.clear()

        # RECUPERO DAL DATABASE GLI ATTORI DEI FILM
        # CHE HANNO UN RATING COMPRESO NEL RANGE SCELTO
        actors = DAO.getAllActorsbyRange(rat1, rat2)

        # INSERISCO GLI ATTORI NELLA MAPPA
        # LA CHIAVE È L'ACTORID
        # IL VALORE È L'OGGETTO ACTOR
        for a in actors:
            self._idMap[a.ActorID] = a

        # AGGIUNGO TUTTI GLI ATTORI COME NODI DEL GRAFO
        self._graph.add_nodes_from(actors)

        # RECUPERO DAL DATABASE LE COPPIE DI ATTORI
        # E IL PESO DELL'ARCO GIÀ CALCOLATO DAL DATABASE
        edges = DAO.getAllEdges(rat1, rat2)

        # SCORRO TUTTE LE COPPIE DI ATTORI
        for actor1, actor2, weight in edges:

            # USO GLI ID PER RECUPERARE DALLA MAPPA
            # I CORRISPONDENTI OGGETTI ACTOR
            a1 = self._idMap[actor1]
            a2 = self._idMap[actor2]

            # CREO L'ARCO TRA I DUE ATTORI
            # IL PESO È GIÀ STATO CALCOLATO DAL DATABASE
            self._graph.add_edge(a1, a2, weight=weight)


    # RESTITUISCO IL NUMERO DI NODI DEL GRAFO
    def getNumNodi(self):
        return len(self._graph.nodes())


    # RESTITUISCO IL NUMERO DI ARCHI DEL GRAFO
    def getNumEdges(self):
        return len(self._graph.edges())


    # RECUPERO I 5 ARCHI CON PESO MAGGIORE
    def getTop5Edges(self):

        # RECUPERO TUTTI GLI ARCHI DEL GRAFO
        # data=True SERVE PER AVERE ANCHE I DATI DELL'ARCO, QUINDI IL PESO
        edges = list(self._graph.edges(data=True))

        # ORDINO GLI ARCHI DAL PESO MAGGIORE AL PESO MINORE
        edges.sort(
            key=lambda e: e[2]["weight"],
            reverse=True
        )

        # RESTITUISCO SOLO I PRIMI 5 ARCHI
        return edges[:5]


    # RECUPERO TUTTE LE COMPONENTI CONNESSE DEL GRAFO
    def getCompConness(self):

        # connected_components TROVA I GRUPPI DI NODI COLLEGATI TRA LORO
        comp = list(nx.connected_components(self._graph))

        return comp


    # TROVO LA COMPONENTE CONNESSA CON IL MAGGIOR NUMERO DI NODI
    def getLargestComp(self, comp):

        # MAX CONFRONTA LE COMPONENTI IN BASE AL NUMERO DI NODI
        largest = max(comp, key=len)

        return largest




