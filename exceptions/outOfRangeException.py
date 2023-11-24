

class OutOfRangeException(Exception):
    def __init__(self, num: int, limit_type: str):
        msg = 'Minimo' if limit_type == 'min' else 'Maximo'
        super().__init__(f">>> {msg}: {num}")
