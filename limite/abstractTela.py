from abc import ABC, abstractmethod


class AbstractTela(ABC):
    @abstractmethod
    def __init__(self):
        pass

    def le_num_inteiro(self,
                       mensagem: str = "",
                       nums_validos: [] = None,
                       minimo: int = None,
                       maximo: int = None) -> int:
        while True:
            try:
                try:
                    valor = input(mensagem)
                except Exception as e:
                    self.mostra_mensagem(type(e))

                inteiro = int(valor)
                if nums_validos and inteiro not in nums_validos:
                    raise ValueError
                if (minimo and inteiro < minimo) or (maximo and inteiro > maximo):
                    raise ValueError
                return inteiro
            except ValueError:
                self.mostra_mensagem("Valor incorreto! Digite um número inteiro válido")
                if nums_validos:
                    self.mostra_mensagem(">>> Valores válidos: ", *nums_validos)
                if minimo:
                    self.mostra_mensagem(">>> Mínimo: ", minimo)
                if maximo:
                    self.mostra_mensagem(">>> Máximo: ", maximo)
            except KeyboardInterrupt:
                self.mostra_mensagem("\nEncerrando o sistema...")
                exit(0)
            except:
                self.mostra_mensagem("Ocorreu um erro")

    def le_texto(self, mensagem: str = "") -> str:
        while True:
            try:
                try:
                    texto = input(mensagem)
                except Exception as e:
                    self.mostra_mensagem(type(e))

                if not texto or texto.isspace():
                    raise ValueError
                return texto.strip()
            except ValueError:
                self.mostra_mensagem("Valor incorreto! Insira um texto não vazio")
            except KeyboardInterrupt:
                self.mostra_mensagem("\nEncerrando o sistema...")
                exit(0)
            except:
                self.mostra_mensagem("Ocorreu um erro")

    def mostra_mensagem(self, *msg: str):
        print(*msg)
