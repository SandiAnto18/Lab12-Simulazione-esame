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
        pass

    def handleCammino(self, e):
        pass