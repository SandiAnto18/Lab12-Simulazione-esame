import flet as ft

"""ricevi i dati da DAO e li mette dentro la view """

"""collego i bottoni della view a una funzione """

class Controller:
    """riceve view e model"""
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

        """fill riempe i dati in un menu a tendina"""
    def fillDDsRating(self):
        ratings = self._model.getRatings()

        """scrivo 2 dropdown per selezionare 
        il min e il max visto che è un rating
        """
        for voto in ratings:
            """ per accedere a qualunque elemento grafico
             nella view uso ._view._ """
            self._view._ddrating1.options.append(ft.dropdown.Option(voto))
            self._view._ddrating2.options.append(ft.dropdown.Option(voto))
        self._view.update_page()




        """handle da una risposta al click """
    def handleCreaGrafo(self, e):
        """informazioni per costruiire il grafo in model"""
        self._model.buildGraph(self._view._ddrating1.value, self._view._ddrating2.value)
        """fondamentale svuotare l'area dei risultati vecchi prima di mostrare quelli nuovi"""
        self._view.txt_result.controls.clear()
        """comando per aggiungere righe testuali/numero in output"""
        self._view.txt_result.controls.append(ft.Text("Grafo correttamente creato:"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di nodi:{self._model.getNumNodi()}"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di archi:{self._model.getNumEdges()}"))
        self._view.update_page()




    def handleCammino(self, e):
        pass