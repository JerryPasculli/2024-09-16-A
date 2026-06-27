from model.modello import Model

self_model = Model()
t1 = self_model.creaGrafo(41, -100, "sphere")
print(t1)
t2 = self_model.percorso()
print(t2)
