

class ExistenceException(Exception):
    def __init__(self, classe: str, exists = True):
        status = "ja existe" if exists else "nao existe"
        super().__init__(f"Atencao! Este(a) {classe} {status}!\n")
