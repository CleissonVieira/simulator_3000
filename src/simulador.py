import random as rd

class Simulador:

    # MÉTODOS DO SIMULADOR

    def __CalcMediaFila__(self, filas, entidades):

        for fila in filas:
            dados_fila = filas.get(fila).get('estatisticas')

            contador_entidades = 0

            for entidade in entidades:
                if entidades.get(entidade)[2][1] == fila:
                    contador_entidades += 1

            dados_fila[5] += 1
            dados_fila[4] += contador_entidades

        return filas

    def __CalcOciosidadeFinal__(self, comps_finito, temp_simulacao):
        
        for comp in comps_finito:
            ociosidade_ind = comps_finito.get(comp).get('estatistica_por_atendente').get('tempo_ocioso')
            disponivel_em = comps_finito.get(comp).get('estatistica_por_atendente').get('fica_disponivel_em')
            tempo_gasto = comps_finito.get(comp).get('estatistica_por_atendente').get('tempo_gasto')

            for i in range(len(ociosidade_ind)):
                ociosidade_ind[i] += (temp_simulacao - disponivel_em[i])

        return comps_finito
    
    def __CalcFila__(self, filas, comps_finito, entidade):
        chave_fila = entidade[2][1]
        chave_entidade = entidade[4]

        fila = filas.get(chave_fila)

        # print("\nfila: ", fila)

        destino_fila = fila.get('destino')
        fila.get('estatisticas')[0] += 1

        estatisticas_atendimento = comps_finito.get(destino_fila[1]).get('estatistica_por_atendente')

        # print("\nEstatisticas por atendente: ", estatisticas_atendimento, "\n")
        
        entidade[1] = entidade[2][1]
        entidade[2] = [destino_fila[0], destino_fila[1]]
        
        pos = 0
        prox_atendente_disp = 0
        tmp_prox_atendente_disp = 9999999
        
        for disponivel in estatisticas_atendimento.get('fica_disponivel_em'):
            if disponivel <= entidade[0]: 
                return [chave_fila, fila, chave_entidade, entidade]
            elif tmp_prox_atendente_disp > estatisticas_atendimento.get('fica_disponivel_em')[pos]:
                    tmp_prox_atendente_disp = estatisticas_atendimento.get('fica_disponivel_em')[pos]
                    prox_atendente_disp = pos
            pos += 1
        

        tmp_espera = (estatisticas_atendimento.get('fica_disponivel_em')[prox_atendente_disp]-entidade[0])
        entidade[0] = tmp_prox_atendente_disp
        fila.get('estatisticas')[1] += tmp_espera
        fila.get('estatisticas')[2] = fila.get('estatisticas')[1]/fila.get('estatisticas')[0]
        if fila.get('estatisticas')[3] < tmp_espera:
            fila.get('estatisticas')[3] = tmp_espera
        
        return [chave_fila, fila, chave_entidade, entidade]

    def __CalcRoteador__(self, roteadores, entidade):
        roteador = roteadores.get(entidade[2][1])

        pesos =[]

        pop = roteador.get('destinos')
        pesos = roteador.get('probabilidades_destinos')

        destino_final = rd.choices(pop, pesos)[0]

        # print("destino",destino_final)

        entidade[1] = entidade[2][1]
        entidade[2] = [destino_final[0], destino_final[1]]

        return entidade

    def __CalcComponenteFinito__(self, comps_finito, entidade):
        chave_comps_finito = entidade[2][1]
        chave_entidade = entidade[4]
        componente = comps_finito.get(entidade[2][1])
        estatisticas_componente = componente.get('estatistica_por_atendente')

        posicoes = 0
        pos_menor = 0
        menor_atend = 99999999

        for disponivel in estatisticas_componente.get('fica_disponivel_em'):
            if menor_atend > disponivel:
                menor_atend = disponivel
                pos_menor = posicoes
            posicoes += 1

        interval = componente.get('intervalo_gasto')
        temp_gasto = rd.randint(interval[0], interval[1])

        entidade[0] += temp_gasto
        entidade[1] = entidade[2][1]
        entidade[2] = [componente.get('destino')[0], componente.get('destino')[1]]
        entidade[3] += temp_gasto

        componente.get('estatisticas')[0] += 1
        componente.get('estatisticas')[2] += temp_gasto
        componente.get('estatisticas')[3] = componente.get('estatisticas')[2] / componente.get('estatisticas')[0]

        estatisticas_componente.get('fica_disponivel_em')[pos_menor] = entidade[0]
        estatisticas_componente.get('tempo_gasto')[pos_menor] += temp_gasto

        # print("\nentidade: ", entidade)
        
        # print("\ncomponente: ", componente)
        
        # print("\nestatisticas_componente: ", estatisticas_componente)
        
        return [chave_comps_finito, componente, chave_entidade, entidade]

    def __CalcComponenteInfinito__(self, comps_infinito, entidade):
        
        chave_comps_infinito = entidade[2][1]
        chave_entidade = entidade[4]
        componente = comps_infinito.get(entidade[2][1])

        interval = componente.get('intervalo_gasto')
        temp_gasto = rd.randint(interval[0], interval[1])

        entidade[0] += temp_gasto
        entidade[1] = entidade[2][1]
        entidade[2] = [componente.get('destino')[0], componente.get('destino')[1]]
        entidade[3] += temp_gasto

        componente.get('estatisticas')[0] += 1
        componente.get('estatisticas')[1] += temp_gasto
        componente.get('estatisticas')[2] = componente.get('estatisticas')[2] / componente.get('estatisticas')[0]

        return [chave_comps_infinito, componente, chave_entidade, entidade]
    
    def __CalcComponenteSaida__(self, comps_saida, entidade):
        chave_saida = entidade[2][1]
        chave_entidade = entidade[4]
        saida = comps_saida.get(entidade[2][1])

        saida.get('estatisticas')[0] += 1
        saida.get('estatisticas')[1] += entidade[3]
        saida.get('estatisticas')[2] = saida.get('estatisticas')[1] / saida.get('estatisticas')[0]

        return [chave_saida, saida, chave_entidade, entidade]
