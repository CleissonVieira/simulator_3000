from pprint import pprint

class Analisador:
    def __init__(self):
        print()

    def __ResultsComponenteFinito__(self, comps_finitos):
        
        for comp in comps_finitos:
            i = 0
            soma_ocioso = 0

            dados_por_atendente = comps_finitos.get(comp).get('estatistica_por_atendente')
            dados_geral = comps_finitos.get(comp).get('estatisticas')
            
            print("\nDados do componente finito (" + comp + "):\n")
            
            print("Ociosidade individual por servidor: ")
            for temp in dados_por_atendente.get('tempo_ocioso'):
                
                print("Servidor {}: {} minutos" .format(i+1, temp))
                soma_ocioso += temp
                i += 1

            dados_geral[1] = soma_ocioso / len(dados_por_atendente.get('tempo_ocioso'))
            print("Média da ociosidade: {:0.2f} minutos" .format(dados_geral[1]))

            print("Tempo médio de atendimento das ETs: {}" .format(dados_geral[3]))

    def __ResultsComponenteFila__(self, filas):

        for fila in filas:
            dados_fila = filas.get(fila).get('estatisticas')

            print("\nDados da fila (" + fila + "):\n")

            print("Tempo médio de espera: {:0.2f} minutos" .format(dados_fila[2]))
            print("Tempo máximo de espera: {:0.2f} minutos" .format(dados_fila[3]))

    def __del__(self):
        del self