

class Capitulo:
    def __init__(self, numero: int, num_paginas: int):
        self.__numero = None
        self.__num_paginas = None
        if isinstance(numero, int):
            self.__numero = numero
        if isinstance(num_paginas, int):
            self.__num_paginas = num_paginas

    @property
    def numero(self) -> int:
        return self.__numero

    @numero.setter
    def numero(self, numero: int):
        if isinstance(numero, int):
            self.__numero = numero

    @property
    def num_paginas(self) -> int:
        return self.__num_paginas

    @num_paginas.setter
    def num_paginas(self, num_paginas: int):
        if isinstance(num_paginas, int):
            self.__num_paginas = num_paginas

    def __repr__(self) -> int:
        return f"{self.numero}"
