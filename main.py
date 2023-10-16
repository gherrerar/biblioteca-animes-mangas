from controle.ctrlPrincipal import CtrlPrincipal
import sys, os


if __name__ == "__main__":
    sys.path.insert(0, os.path.abspath(os.curdir))
    CtrlPrincipal().inicializar_sistema()
