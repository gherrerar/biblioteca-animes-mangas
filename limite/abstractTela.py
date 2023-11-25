from abc import ABC, abstractmethod
from exceptions.outOfRangeException import OutOfRangeException
import PySimpleGUI as sg


class AbstractTela(ABC):
    @abstractmethod
    def __init__(self):
        pass

    def le_num_inteiro(self,
                       titulo: str = "",
                       valor: str = "",
                    #    nums_validos: [] = None,
                       minimo: int = None,
                       maximo: int = None) -> int:
        try:
            inteiro = int(valor)
            # if nums_validos and inteiro not in nums_validos:
            #     raise ValueError
            if (minimo and inteiro < minimo):
                raise OutOfRangeException(minimo, 'min')
            if (maximo and inteiro > maximo):
                raise OutOfRangeException(maximo, 'max')
            return inteiro
        except ValueError:
            self.mostra_mensagem(
                f"{titulo}:\nValor incorreto! Digite um número inteiro valido")
            # if nums_validos:
            #     self.mostra_mensagem(">>> Valores válidos: ", *nums_validos)
        except OutOfRangeException as error:
            self.mostra_mensagem("Valor incorreto! Digite um número inteiro valido")
            self.mostra_mensagem(f"{error}")
        except KeyboardInterrupt:
            self.mostra_mensagem("Encerrando o sistema...")
            exit(0)
        except:
            self.mostra_mensagem("Ocorreu um erro")

    def le_texto(self,
                 titulo: str = "",
                 texto: str = "") -> str:
        try:
            if not texto or texto.isspace():
                raise ValueError
            return texto.strip()
        except ValueError:
            self.mostra_mensagem(
                f"{titulo}:\nValor incorreto! Insira um texto nao vazio")
        except KeyboardInterrupt:
            self.mostra_mensagem("Encerrando o sistema...")
            exit(0)
        except:
            self.mostra_mensagem("Ocorreu um erro")

    def mostra_mensagem(self, *msg: str):
        sg.Popup(*msg, button_color='white')
