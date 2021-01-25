import random

class Simulador:

    def __init__(self):
        print()
        
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
            entidade.append(True)       # Se esta ativa ou não
            entidade.append("gerador")  # Onde está
            entidade.append(destino)    # Para onde vai
            entidade.append(0)          # Tempo gasto
            entidades_temporaria[count] = entidade
            entidade.append(count)
            edt += interval           
            
        return entidades_temporaria

    def __CalcEntidade__(self):
        # trabalha com as entidades
        ativa = True
        localizacao = "gerador_entidades_temporarias"
        destino = ""
        tempo_gasto = 0 # por entidade
        return {}


    # ROT - trabalha com o roteamento das entidades
    def __roteando_rota__(self, roteadores, entidades):
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

    def __CalcFila__(self, filas, entidade, modelo):
        chave_fila = entidade[3][1]
        chave_entidade = entidade[5]
        # print("\nEntidade: ", entidade)
        fila = modelo[entidade[3][0]].get(entidade[3][1])
        # print("\nfila: ", fila)
        atendimento = modelo[fila.get('destino')[0]].get(fila.get('destino')[1])
        # print("\nAtendimento: ", atendimento)
        estatisticas_atendimento = atendimento.get('estatistica_por_atendente')
        # print("\nEstatisticas por atendente: ", estatisticas_atendimento, "\n")
        
        entidade[2] = entidade[3][1]
        entidade[3] = [fila.get('destino')[0], fila.get('destino')[1]]
        fila.get('estatisticas')[0] += 1
        
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
        tmp_espera = (estatisticas_atendimento.get('fica_disponivel_em')[prox_atendente_disp]-entidade[0])
        fila.get('estatisticas')[1] += tmp_espera
        entidade[0] = tmp_prox_atendente_disp
        fila.get('estatisticas')[2] = fila.get('estatisticas')[1]/fila.get('estatisticas')[0]
        if fila.get('estatisticas')[3] < tmp_espera:
            fila.get('estatisticas')[3] = tmp_espera
        
        return [chave_fila, fila, chave_entidade, entidade]


    # GSF - trabalha com os componentes finitos
    def __StructComponenteFinito__(self, config_compsFinito):
        
        for comp_finito in config_compsFinito:
            config_compsFinito_x = config_compsFinito.get(comp_finito)
            comp_f = []
            comp_f.append(0) # quantidade_entidades = 0 # quantidade de entidades que passaram pela fila
            comp_f.append(0) # tempo_chegada ++
            comp_f.append(0) # tempo_saida ++
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

    def __CalcComponenteFinito__(self, comps_finito, entidade, modelo):
        chave_comps_finito = entidade[3][1]
        chave_entidade = entidade[5]
        
        print("\nentidade: ", entidade)
        componente = comps_finito.get(entidade[3][1])
        print("\ncomponente: ", componente)
        estatisticas_componente = componente.get('estatistica_por_atendente')
        print("\nestatisticas_componente: ", estatisticas_componente)
        
        posicoes = 0
        
        for disponivel in estatisticas_componente.get('fica_disponivel_em'):
            if disponivel < entidade[0]: 
                tmp_ent_atual = entidade[0]
                tempo_ocioso = estatisticas_componente.get('tempo_ocioso')[posicoes]
                tempo_ocioso = tmp_ent_atual - tempo_ocioso
                estatisticas_componente.get('tempo_ocioso')[posicoes] += tempo_ocioso
            elif tmp_prox_atendente_disp > estatisticas_atendimento.get('fica_disponivel_em')[posicoes]:
                    tmp_prox_atendente_disp = estatisticas_atendimento.get('fica_disponivel_em')[posicoes]
                    prox_atendente_disp = posicoes
            posicoes += 1
        


        
        return [chave_comps_finito, comps_finito, chave_entidade, entidade]

    

    # GSI - trabalha com os componentes infinitos
    def __StructComponenteInfinito__(self, config_compsInfinito):
        # 
        for comp_finito in config_compsInfinito:
            config_compsInfinito_x = config_compsInfinito.get(comp_finito)
            comp_inf = []
            comp_inf.append(0) # quantidade_entidades = 0 # quantidade de entidades que passaram pela fila
            comp_inf.append(0) # tempo_chegada ++
            comp_inf.append(0) # tempo_saida ++
            comp_inf.append(0) # tempo_permanencia
            comp_inf.append(0) # media_permanencia
            config_compsInfinito_x["estatisticas"] = comp_inf

        return config_compsInfinito

    def __CalcComponenteInfinito__(self, comps_infinito, entidades):
        # GSI - trabalha com os componentes infinitos
        quantidade_entidades = 0 # quantidade de entidades que passaram pela fila
        tempo_chegada = 0
        tempo_saida = 0
        tempo_permanencia = tempo_saida - tempo_chegada
        media_permanencia = tempo_permanencia / quantidade_entidades
        return {}


    # OUT - trabalha com os componentes de saída
    def __componenteSaida__(self, comps_saida, entidades):

        return {}

    def __del__(self):
        del self