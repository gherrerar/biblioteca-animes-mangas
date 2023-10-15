from limite.abstractTela import AbstractTela


class TelaManga(AbstractTela):
    def __init__(self):
        pass

    def mostra_opcoes(self) -> int:
        print(f"{'MANGAS':-^30}")
        print("1 - Listar")
        print("2 - Cadastrar")
        print("3 - Editar")
        print("4 - Remover")
        print("5 - Volumes")
        print("0 - Voltar")
        
        opcao = super().le_num_inteiro("Escolha uma opcao: ", range(6))
        return opcao
    
    def mostra_opcoes_volume(self) -> int:
        print(f"{'VOLUMES':-^30}")
        print("1 - Listar")
        print("2 - Cadastrar")
        print("3 - Remover")
        print("4 - Incluir Capitulo")
        print("5 - Remover Capitulo")
        print("0 - Voltar")

        opcao = super().le_num_inteiro("Escolha uma opcao: ", range(6))
        return opcao

    def mostra_manga(self, dados_manga: {}):
        if not dados_manga:
            self.mostra_mensagem("Nenhum manga foi cadastrado!")
        else:
            print(f"{'TITULO:':<15} {dados_manga['titulo']}")
            print(f"{'ANO:':<15} {dados_manga['ano']}")
            print(f"{'GENERO:':<15} {dados_manga['genero'].nome}")
            print(f"{'AUTOR:':<15} "
                  "{}".format(
                      dados_manga['autor'].nome
                      if dados_manga['autor']
                      else 'Nenhum vinculado')
                )
            print(f"{'VOLUMES:':<15} "
                "{}".format(
                    str(len(dados_manga['volumes']))
                    + ' / '
                    + str(dados_manga['num_volumes'])
                )
                )
            print()

    def recolhe_dados_manga(self) -> dict:
        print(f"{'DADOS MANGA':-^30}")
        titulo = super().le_texto("Titulo: ")
        ano = super().le_num_inteiro("Ano: ", minimo=1000, maximo=2024)
        genero = super().le_texto("Genero: ")
        num_volumes = super().le_num_inteiro("N° Volumes: ", minimo=1)
    
        return {'titulo': titulo, 'ano': ano, 'genero': genero, 'num_volumes': num_volumes}

    def seleciona_manga(self) -> str:
        print(f"{'SELECIONAR MANGA':-^30}")
        titulo = super().le_texto("Titulo: ")
        return titulo

    def mostra_volume(self, dados_volume: {}):
        if not dados_volume:
            self.mostra_mensagem("Nenhum volume cadastrado neste manga")
        else:
            print(f"{'NUMERO:':<15} {dados_volume['numero']}")
            print(f"{'Nº CAPITULOS:':<15} {dados_volume['num_capitulos']}")
            print()

    def recolhe_dados_volume(self, n_vols: int) -> dict:
        print(f"{'DADOS VOLUME':-^30}")
        numero = super().le_num_inteiro("Numero: ", minimo=1, maximo=n_vols)
        num_capitulos = super().le_num_inteiro("N° Capitulos: ", minimo=1)

        return {'numero': numero, 'num_capitulos': num_capitulos}

    def seleciona_volume(self, n_vols: int) -> int:
        print(f"{'SELECIONAR VOLUME':-^30}")
        numero = super().le_num_inteiro("Numero: ", minimo=1, maximo=n_vols)
        return numero

    def recolhe_dados_capitulo(self, n_caps: int) -> dict:
        print(f"{'DADOS CAPITULO':-^30}")
        numero = super().le_num_inteiro("Numero: ", minimo=1, maximo=n_caps)
        num_paginas = super().le_num_inteiro("Numero de Paginas: ", minimo=10)

        return {'numero': numero, 'num_paginas': num_paginas}

    def seleciona_capitulo(self, n_caps: int) -> int:
        print(f"{'SELECIONAR CAPITULO':-^30}")
        numero = super().le_num_inteiro("Numero: ", minimo=1, maximo=n_caps)
        return numero
