import flet as ft


class Controller:

    def __init__(self, view, model):
        self._view = view
        self._model = model


    def fillDDsRating(self):
        # RECUPERO I RATING DAL MODEL
        ratings = self._model.getRatings()

        # AGGIUNGO OGNI RATING AI DUE DROPDOWN
        for voto in ratings:
            self._view._ddrating1.options.append(ft.dropdown.Option(voto))
            self._view._ddrating2.options.append(ft.dropdown.Option(voto))

        self._view.update_page()


    def handleCreaGrafo(self, e):

        # PRENDO I DUE RATING SCELTI DALL'UTENTE
        rat1 = self._view._ddrating1.value
        rat2 = self._view._ddrating2.value

        # CHIEDO AL MODEL DI COSTRUIRE IL GRAFO
        self._model.buildGraph(rat1, rat2)

        # SVUOTO I RISULTATI PRECEDENTI
        self._view.txt_result.controls.clear()

        # MOSTRO NUMERO DI NODI E ARCHI
        self._view.txt_result.controls.append(
            ft.Text("Grafo correttamente creato:")
        )

        self._view.txt_result.controls.append(
            ft.Text(f"Numero di nodi: {self._model.getNumNodi()}")
        )

        self._view.txt_result.controls.append(
            ft.Text(f"Numero di archi: {self._model.getNumEdges()}")
        )


        # RECUPERO I 5 ARCHI CON PESO MAGGIORE
        top5 = self._model.getTop5Edges()

        self._view.txt_result.controls.append(
            ft.Text("Top 5 archi:")
        )

        # STAMPO I 5 ARCHI
        for a1, a2, w in top5:
            self._view.txt_result.controls.append(
                ft.Text(f"{a1.Name} -> {a2.Name} : {w['weight']}")
            )


        # RECUPERO LE COMPONENTI CONNESSE
        cc = self._model.getCompConness()

        # IL NUMERO DI COMPONENTI È LA LUNGHEZZA DELLA LISTA
        self._view.txt_result.controls.append(
            ft.Text(f"Il grafo ha {len(cc)} componenti connesse")
        )


        # RECUPERO LA COMPONENTE CON PIÙ ATTORI
        largest = self._model.getLargestComp(cc)

        self._view.txt_result.controls.append(
            ft.Text(
                f"La più grande componente connessa ha {len(largest)} attori:"
            )
        )

        # STAMPO GLI ATTORI DELLA COMPONENTE PIÙ GRANDE
        for a in largest:
            self._view.txt_result.controls.append(
                ft.Text(a.Name)
            )

        # AGGIORNO LA PAGINA
        self._view.update_page()


    def handleCammino(self, e):
        pass