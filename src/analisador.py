class Analisador:

    #Métodos para calcular e exibir os resultados

    def __ResultsComponenteInfinito__(self, comps_infinitos):
        
        for comp in comps_infinitos:
            i = 0

            dados_geral = comps_infinitos.get(comp).get('estatisticas')
            
            print("\nDados do componente infinito (" + comp + "):\n")
   
            print("Tempo médio de atendimento das ETs: {:0.2f}" .format(dados_geral[3]))

    def __ResultsComponenteFinito__(self, comps_finitos, fileName):

        for comp in comps_finitos:
            i = 0
            soma_ocioso = 0

            dados_por_atendente = comps_finitos.get(comp).get('estatistica_por_atendente')
            dados_geral = comps_finitos.get(comp).get('estatisticas')
            
            fileName.writelines("\n\nDados do componente finito (" + comp + "):\n\n")
            print("\nDados do componente finito (" + comp + "):\n")
            
            fileName.writelines("Ociosidade individual por servidor: ")
            print("Ociosidade individual por servidor: ")
            
            for temp in dados_por_atendente.get('tempo_ocioso'):
                
                fileName.writelines("\nServidor {}: {} minutos" .format(i+1, temp))
                print("Servidor {}: {} minutos" .format(i+1, temp))
                
                soma_ocioso += temp
                i += 1

            dados_geral[1] = soma_ocioso / len(dados_por_atendente.get('tempo_ocioso'))
            
            fileName.writelines("\nMédia da ociosidade: {:0.2f} minutos" .format(dados_geral[1]))
            print("Média da ociosidade: {:0.2f} minutos" .format(dados_geral[1]))

            fileName.writelines("\nTempo médio de atendimento das ETs: {:0.2f}" .format(dados_geral[3]))
            print("Tempo médio de atendimento das ETs: {:0.2f}" .format(dados_geral[3]))

    def __ResultsComponenteFila__(self, filas, fileName):
        for fila in filas:
            dados_fila = filas.get(fila).get('estatisticas')

            fileName.writelines("\n\nDados da fila (" + fila + "):\n")
            print("\nDados da fila (" + fila + "):\n")
            
            fileName.writelines("\nQuantidade média de Entidades Temporárias: {:0.2f}" .format(dados_fila[4]/dados_fila[5]))
            print("Quantidade média de Entidades Temporárias: {:0.2f}" .format(dados_fila[4]/dados_fila[5]))
            
            fileName.writelines("\nTempo médio de espera: {:0.2f} minutos" .format(dados_fila[2]))
            print("Tempo médio de espera: {:0.2f} minutos" .format(dados_fila[2]))
            
            fileName.writelines("\nTempo máximo de espera: {:0.2f} minutos" .format(dados_fila[3]))
            print("Tempo máximo de espera: {:0.2f} minutos" .format(dados_fila[3]))

    def __ResultsComponenteSaida__(self, comps_saidas, fileName):
        media_permanencia = 0
        total_et = 0

        for saida in comps_saidas: #caso haja mais de uma saida devemos somar os dados
            dados_saida = comps_saidas.get(saida).get('estatisticas')
            
            total_et += dados_saida[0]
            media_permanencia += dados_saida[2]

        media_permanencia /= len(comps_saidas)

        fileName.writelines("\n\nTotal de entidades temporarias que entraram e sairam do modelo: {}" .format(total_et))
        print("\nTotal de entidades temporarias que entraram e sairam do modelo: {}" .format(total_et))
        
        fileName.writelines("\nTempo médio de permanencia das ETs no modelo: {:0.2f} minutos" .format(media_permanencia))
        print("Tempo médio de permanencia das ETs no modelo: {:0.2f} minutos" .format(media_permanencia))
        