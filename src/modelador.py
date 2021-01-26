class Modelador:
    # MÉTODOS DO MODELADOR

    # SRC - trabalha com os geradores de entidades temporárias
    def __StructGerador__(self, config_entidade):
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
    def __StructRoteador__(self, config_roteadores):
        for comp_roteador in config_roteadores:
            comp_roteador_x = config_roteadores.get(comp_roteador)

        return config_roteadores

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
    