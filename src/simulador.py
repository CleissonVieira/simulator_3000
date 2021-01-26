import random as rd

class Simulador:

    def __init__(self):
        print()
    
    # MÉTODOS DO SIMULADOR


    # def __CalcEntidade__(self):
    #     # trabalha com as entidades
    #     localizacao = "gerador_entidades_temporarias"
    #     destino = ""
    #     tempo_gasto = 0 # por entidade
    #     return {}
    
    def __CalcFila__(self, filas, comps_finito, entidade, modelo):
        chave_fila = entidade[2][1]
        chave_entidade = entidade[4]

        fila = modelo[entidade[2][0]].get(entidade[2][1])
        destino_fila = fila.get('destino')[1]
        fila.get('estatisticas')[0] += 1

        atendente = comps_finito.get(destino_fila)
        estatisticas_atendimento = atendente.get('estatistica_por_atendente')

        #print("\nEntidade: ", entidade)
        
        #print("\nfila: ", fila)

        #print("\nAtendimento: ", atendente)
        #print("\nEstatisticas por atendente: ", estatisticas_atendimento, "\n")
        
        entidade[1] = entidade[2][1]
        entidade[2] = [fila.get('destino')[0], fila.get('destino')[1]]
        
        pos = 0
        prox_atendente_disp = 0
        tmp_prox_atendente_disp = 9999999
        
        for disponivel in estatisticas_atendimento.get('fica_disponivel_em'):
            if disponivel <= entidade[0]: 
                fila.get('estatisticas')[2] = fila.get('estatisticas')[1]/fila.get('estatisticas')[0]
                return [chave_fila, fila, chave_entidade, entidade]
            elif tmp_prox_atendente_disp > estatisticas_atendimento.get('fica_disponivel_em')[pos]:
                    tmp_prox_atendente_disp = estatisticas_atendimento.get('fica_disponivel_em')[pos]
                    prox_atendente_disp = pos
            pos += 1
        
        entidade[0] = tmp_prox_atendente_disp

        tmp_espera = (estatisticas_atendimento.get('fica_disponivel_em')[prox_atendente_disp]-entidade[0])
        fila.get('estatisticas')[1] += tmp_espera
        fila.get('estatisticas')[2] = fila.get('estatisticas')[1]/fila.get('estatisticas')[0]
        if fila.get('estatisticas')[3] < tmp_espera:
            fila.get('estatisticas')[3] = tmp_espera
        
        return [chave_fila, fila, chave_entidade, entidade]

    def __CalcComponenteFinito__(self, comps_finito, entidade, modelo):
        chave_comps_finito = entidade[2][1]
        chave_entidade = entidade[4]
        componente = comps_finito.get(entidade[2][1])
        estatisticas_componente = componente.get('estatistica_por_atendente')

        posicoes = 0
        
        for disponivel in estatisticas_componente.get('fica_disponivel_em'):
            if disponivel <= entidade[0]:
                tmp_ent_atual = entidade[0]
                tempo_ocioso = estatisticas_componente.get('tempo_ocioso')[posicoes]
                tempo_ocioso = tmp_ent_atual - tempo_ocioso
                estatisticas_componente.get('tempo_ocioso')[posicoes] += tempo_ocioso 
                break
            posicoes += 1
        
        if posicoes == componente.get('n_atendentes'):
            posicoes -= 1

        interval = componente.get('intervalo_gasto')
        temp_gasto = rd.randint(interval[0], interval[1])

        entidade[0] += temp_gasto
        entidade[1] = entidade[2][1]
        entidade[2] = [componente.get('destino')[0], componente.get('destino')[1]]
        entidade[3] += temp_gasto

        componente.get('estatisticas')[0] += 1
        componente.get('estatisticas')[2] += temp_gasto
        componente.get('estatisticas')[3] = componente.get('estatisticas')[2] / componente.get('estatisticas')[0]

        estatisticas_componente.get('fica_disponivel_em')[posicoes] = entidade[0]

        # print("\nentidade: ", entidade)
        
        # print("\ncomponente: ", componente)
        
        # print("\nestatisticas_componente: ", estatisticas_componente)
        
        return [chave_comps_finito, componente, chave_entidade, entidade]

    def __CalcComponenteInfinito__(self, comps_infinito, entidade, modelo):
        
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

    def __del__(self):
        del self