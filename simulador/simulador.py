import random

class Simulador:

    def __init__(self):
        print()

    # MÉTODOS DO MODELADOR

    # SRC - trabalha com os geradores de entidades temporárias
    def __GeradorEntidades__(self, config_entidade):
        init = config_entidade.get('intervalo_tempo_de_operação')[0]
        end = config_entidade.get('intervalo_tempo_de_operação')[1]
        interval = config_entidade.get('intervalo_entre_geracao')
        limit = config_entidade.get('limite')
        destino = config_entidade.get('destino')

        count = 0
        edt = init
        entidades_temporaria = {}

        for minute  in range(init, end+1, interval):
            if count == limit: break
            count += 1

            entidade = []
            entidade.append(edt)        # Tempo inicial
            entidade.append("gerador")  # Onde está
            entidade.append(destino)    # Para onde vai
            entidade.append(0)          # Tempo gasto
            entidades_temporaria[count] = entidade
            entidade.append(count)
            edt += interval           
            
        return entidades_temporaria

    # ROT - trabalha com o roteamento das entidades
    def __roteando_rota__(self, roteadores, entidades):
        #aqui tem que ser feito ainda
        return {}

    # QUE - trabalha com as filas das entidades
    def __StructFila__(self, config_fila):          
        for fila in config_fila:
            fila_x = config_fila.get(fila)
            fila = []
            fila.append(0) # quantidade_entidades = 0 # quantidade de entidades que passaram pela fila
            fila.append(0) # tempo_espera = tempo_saida - tempo_chegada
            fila.append(0) # media_espera = tempo_espera / quantidade_entidades
            fila.append(0) # maior_tempo_espera_entidade = 0
            fila_x["estatisticas"] = fila

        return config_fila

    # GSF - trabalha com os componentes finitos
    def __StructComponenteFinito__(self, config_compsFinito):
        
        for comp_finito in config_compsFinito:
            config_compsFinito_x = config_compsFinito.get(comp_finito)
            comp_f = []
            comp_f.append(0) # quantidade_entidades = 0 # quantidade de entidades que passaram pela fila
            comp_f.append(0) # tempo_ocioso_media
            comp_f.append(0) # tempo_permanencia
            comp_f.append(0) # media_permanencia
            config_compsFinito_x["estatisticas"] = comp_f

            n_atendentes = config_compsFinito.get(comp_finito).get('n_atendentes')
            atendentes = {}
            tempo_ocioso_individual_atendente = []
            disponibilidade_individual_atendente = []
            fica_disponivel_em = []
            for atend in range(0, n_atendentes):
                tempo_ocioso_individual_atendente.append(0)
                disponibilidade_individual_atendente.append(True)
                fica_disponivel_em.append(0)
            
            atendentes['tempo_ocioso'] = tempo_ocioso_individual_atendente
            atendentes['disponibilidade'] = disponibilidade_individual_atendente
            atendentes['fica_disponivel_em'] = fica_disponivel_em
            config_compsFinito_x['estatistica_por_atendente'] = atendentes
        return config_compsFinito

    # GSI - trabalha com os componentes infinitos
    def __StructComponenteInfinito__(self, config_compsInfinito):
 
        for comp_finito in config_compsInfinito:
            config_compsInfinito_x = config_compsInfinito.get(comp_finito)
            comp_inf = []
            comp_inf.append(0) # quantidade_entidades = 0 # quantidade de entidades que passaram pela fila
            comp_inf.append(0) # tempo_permanencia
            comp_inf.append(0) # media_permanencia
            config_compsInfinito_x["estatisticas"] = comp_inf

        return config_compsInfinito

    # OUT - trabalha com os componentes de saída
    def __StructSaida__(self, config_saida):
        for saida in config_saida:
            saida_x = config_saida.get(saida)
            saida = []
            saida.append(0) # quantidade_entidades = 0 # quantidade de entidades que passaram pela saida
            saida.append(0) # tempo_total = tempo total da entidade até sair do modelo
            saida.append(0) # media_espera = tempo_total / quantidade_entidades
            saida_x["estatisticas"] = saida

        return config_saida    
    
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
        
        posicoes = 0
        prox_atendente_disp = 0
        tmp_prox_atendente_disp = 9999999
        
        for disponivel in estatisticas_atendimento.get('fica_disponivel_em'):
            if disponivel <= entidade[0]: 
                fila.get('estatisticas')[2] = fila.get('estatisticas')[1]/fila.get('estatisticas')[0]
                return [chave_fila, fila, chave_entidade, entidade]
            elif tmp_prox_atendente_disp > estatisticas_atendimento.get('fica_disponivel_em')[posicoes]:
                    tmp_prox_atendente_disp = estatisticas_atendimento.get('fica_disponivel_em')[posicoes]
                    prox_atendente_disp = posicoes
            posicoes += 1
        
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
        temp_gasto = random.randint(interval[0], interval[1])

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
        temp_gasto = random.randint(interval[0], interval[1])

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

        print(saida)

        saida.get('estatisticas')[0] += 1
        saida.get('estatisticas')[1] += entidade[3]
        saida.get('estatisticas')[2] = saida.get('estatisticas')[1] / saida.get('estatisticas')[0]

        return [chave_saida, saida, chave_entidade, entidade]

    def __del__(self):
        del self