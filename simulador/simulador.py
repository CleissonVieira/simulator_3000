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
            edt += interval

            entidade = []
            entidade.append(edt)        # Tempo inicial
            entidade.append(True)       # Se esta ativa ou não
            entidade.append("gerador")  # Onde está
            entidade.append(destino)    # Para onde vai
            entidade.append(0)          # Tempo gasto
            entidades_temporaria[edt] = entidade            
            
        return entidades_temporaria

    def __CalcEntidade__(self):
        # trabalha com as entidades
        ativa = True
        localizacao = "gerador_entidades_temporarias"
        destino = ""
        tempo_gasto = 0 # por entidade
        return {}


    # ROT - trabalha com o roteamento das entidades
    def __roteando_rota__(self, config_roteador):
        return {}


    # QUE - trabalha com as filas das entidades
    def __StructFila__(self, config_fila):
          
        for fila in config_fila:
            fila_x = config_fila.get(fila)
            fila = []
            fila.append(0) # quantidade_entidades = 0 # quantidade de entidades que passaram pela fila
            fila.append(0) # tempo_chegada ++
            fila.append(0) # tempo_saida ++
            fila.append(0) # tempo_espera = tempo_saida - tempo_chegada
            fila.append(0) # media_espera = tempo_espera / quantidade_entidades
            fila.append(0) # maior_tempo_espera_entidade = 0
            fila_x["estatisticas"] = fila

        return config_fila

    def __CalcFila__(self, QUE):
        # QUE - trabalha com as filas das entidades
        quantidade_entidades = 0 # quantidade de entidades que passaram pela fila
        tempo_chegada = 0
        tempo_saida = 0
        tempo_espera = tempo_saida - tempo_chegada
        media_espera = tempo_espera / quantidade_entidades
        maior_tempo_espera_entidade = 0
        return {}


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
            for atend in range(0, n_atendentes):
                tempo_ocioso_individual_atendente.append(0)
                disponibilidade_individual_atendente.append(0)
            
            atendentes['tempo_ocioso'] = tempo_ocioso_individual_atendente
            atendentes['disponibilidade'] = disponibilidade_individual_atendente
            config_compsFinito_x['estatistica_por_atendente'] = atendentes
        return config_compsFinito

    def __CalcComponenteFinito__(self, GSF, quant_atend):
        # GSF - trabalha com os componentes finitos
        # estruturar pra receber N componentes finitos com n atendentes e retornar um dicionarios com a estrutura e variáveis necessárias
        quantidade_entidades = 0 # quantidade de entidades que passaram pela fila
        tempo_chegada = 0
        tempo_saida = 0
        tempo_ocioso_individual_atendente = [] # verificar a quant de atendentes
        disponibilidade_individual_atendente = []
        for atend in range(0, quant_atend):
            tempo_ocioso_individual_atendente.append(0)
            disponibilidade_individual_atendente.append(0) # 0 free 1 occuped
        tempo_ocioso_media = sum(tempo_ocioso_individual_atendente) / quant_atend # sum soma dos vetores
        tempo_permanencia = tempo_saida - tempo_chegada
        media_permanencia = tempo_permanencia / quantidade_entidades
        return {}

    

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

    def __CalcComponenteInfinito__(self, GSI):
        # GSI - trabalha com os componentes infinitos
        quantidade_entidades = 0 # quantidade de entidades que passaram pela fila
        tempo_chegada = 0
        tempo_saida = 0
        tempo_permanencia = tempo_saida - tempo_chegada
        media_permanencia = tempo_permanencia / quantidade_entidades
        return {}


    # OUT - trabalha com os componentes de saída
    def __componenteSaida__(self, OUT):

        return {}

    def __del__(self):
        del self