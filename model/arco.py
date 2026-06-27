class Arco:
    def __init__(self, p, s, p1):
        self._primo = p
        self._secondo = s
        self._peso = p1

    def __lt__(self, other):
        return self._peso<other._peso

    def __str__(self):
        return self._primo.__str__() + "<-->" + self._secondo.__str__() + f"| peso: {str(self._peso)}"
