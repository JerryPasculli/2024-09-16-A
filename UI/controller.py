import flet as ft
from UI.view import View
from model.modello import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view: View = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._flag = False


    def handle_graph(self, e):
        self._flag = False
        self._view.txt_result1.controls.clear()
        v1 = self._view.txt_longitude.value
        v2 = self._view.txt_latitude.value
        shape = self._view.ddshape.value
        try:
            float(v1)
            float(v2)
        except:
            t1 = ft.Text("DEVI INSERIRE VALORI DI LATITUDINE E LONGITUDINE NUMERICI", color = "red")
            self._view.txt_result1.controls.append(t1)
            self._view.update_page()
            return
        if shape is None:
            t1 = ft.Text("DEVI INSERIRE UN VALORE PER LA SHAPE", color="red")
            self._view.txt_result1.controls.append(t1)
            self._view.update_page()
            return
        v1 = float(v1)
        v2 = float(v2)
        if v2>self._LatMax or v2<self._LatMin:
            t1 = ft.Text(f"La latitudine deve essere un valore numerico compreso tra {self._LatMin} e {self._LatMax}", color="red")
            self._view.txt_result1.controls.append(t1)
            self._view.update_page()
            return
        if v1>self._LngMax or v1<self._LngMin:
            t1 = ft.Text(f"La longitudine deve essere un valore numerico compreso tra {self._LngMin} e {self._LngMax}", color="red")
            self._view.txt_result1.controls.append(t1)
            self._view.update_page()
            return
        stringa = self._model.creaGrafo(v2, v1, shape)
        t1 = ft.Text(stringa)
        self._view.txt_result1.controls.append(t1)
        self._flag = True
        self._view.btn_path.disabled = False
        self._view.update_page()


    def handle_path(self, e):
        self._view.txt_result2.controls.clear()
        if self._flag == False:
            t1 = ft.Text(f"Devi prima creare un grafo",
                         color="red")
            self._view.txt_result2.controls.append(t1)
            self._view.update_page()
            return
        stringa = self._model.percorso()
        t1 = ft.Text(stringa)
        self._view.txt_result2.controls.append(t1)
        self._view.update_page()

    def fill_ddshape(self):
        pass

    def popola(self):
        lista = self._model.forme()
        for element in lista:
            opt = ft.dropdown.Option(element[0])
            self._view.ddshape.options.append(opt)

    def maxMin(self):
        lista = self._model.maxMin()
        for element in lista:
            self._LngMax = element[0]
            self._LngMin = element[1]
            self._LatMax = element[2]
            self._LatMin = element[3]

