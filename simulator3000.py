import json
import random
from pprint import pprint
from src.modelador import Modelador
from src.simulador import Simulador
from src.analisador import Analisador

m3000 = Modelador()
s3000 = Simulador()
a3000 = Analisador()

with open('model_config/model_config.json', 'r') as json_file:
    modelo = json.load(json_file)

# [0]=tempo gerado | [1]=localização | [2]=destino | [3]=tempo gasto | [4]=chave dict
if modelo['componente_gerador']:
    entidades = m3000.__StructGerador__(modelo['componente_gerador'])
    #pprint(entidades)

# origem, destino, estatísticas: [0]=qtd entidades | [1]=tmp espera | [2]=media espera | [3]=entidade que mais esperou
if modelo['componente_fila']:
    componentes_filas = m3000.__StructFila__(modelo['componente_fila'])
    #pprint(componentes_filas)

# origem, destinos [], estatísticas: [0]=qtd entidades | [1]=qtd entidades cada destino []
if modelo['componente_roteador']:
    componentes_roteadores = m3000.__StructRoteador__(modelo['componente_roteador'])
    #pprint(componentes_roteadores)

# origem, destino, intervalo_gasto, estatísticas: [0]=qtd entidades | [1]=media de tmp ocioso | [2]=tmp permanencia | [3]=media permanencia, atendentes: tempo osioso p/ atendente [] | disponibilidade de cada atendente []
if modelo['componente_finito']:
    componentes_finitos = m3000.__StructComponenteFinito__(modelo['componente_finito'])
    #pprint(componentes_finitos)

# origem, destino, intervalo_gasto, estatísticas: [0]=qtd entidades | [1]=tmp permanencia | [2]=media permanencia
if modelo['componente_infinito']:
    componentes_infinitos = m3000.__StructComponenteInfinito__(modelo['componente_infinito'])
    #pprint(componentes_infinitos)   

# origem, estatísticas: [0]=qtd entidades | [1]=tmp total | [2]=media tempo no modelo
if modelo['componente_saida']:
    componentes_saidas = m3000.__StructSaida__(modelo['componente_saida'])
    #pprint(componentes_saidas)

# Verificar nos componentes se Origem da entidade é != do próprio componente onde chegou, então verificar se é origem da saída e eliminar x entidade


#print("\n\n\nSIMULAÇAO A PARTIR DESSE PONTO: \n")

tempo_simulado = 0
while (tempo_simulado < modelo['tempo_simulacao']):
    entidade_atual = []


    for item in sorted(entidades, key = entidades.get):
        entidade_atual = entidades[item]
        break

    if entidade_atual == []: #caso todas as entidades já tenham saido do modelo encerra a simulacao
        print("tempo simulado \n\n\n", tempo_simulado)
        tempo_simulado = modelo['tempo_simulacao']
        break
    else:
        tempo_simulado = entidade_atual[0]
        destino_entidade = entidade_atual[2][0]   

    if destino_entidade == 'componente_fila':
        dados_alteracoes = s3000.__CalcFila__(componentes_filas, componentes_finitos, entidade_atual)
        componentes_filas[dados_alteracoes[0]] = dados_alteracoes[1]
        entidades[dados_alteracoes[2]] = dados_alteracoes[3]
    
    elif destino_entidade == 'componente_roteador':
        entidades[entidade_atual[4]] = s3000.__CalcRoteador__(componentes_roteadores, entidade_atual)

    elif destino_entidade == 'componente_finito':
        dados_alteracoes = s3000.__CalcComponenteFinito__(componentes_finitos, entidade_atual)
        componentes_finitos[dados_alteracoes[0]] = dados_alteracoes[1]
        entidades[dados_alteracoes[2]] = dados_alteracoes[3]
    
    elif destino_entidade == 'componente_infinito':
        dados_alteracoes = s3000.__CalcComponenteInfinito__(componentes_infinitos, entidade_atual)
        componentes_infinitos[dados_alteracoes[0]] = dados_alteracoes[1]
        entidades[dados_alteracoes[2]] = dados_alteracoes[3]

    elif destino_entidade == 'componente_saida':
        dados_alteracoes = s3000.__CalcComponenteSaida__(componentes_saidas, entidade_atual)
        componentes_saidas[dados_alteracoes[0]] = dados_alteracoes[1]
        entidades.pop(dados_alteracoes[2])

if tempo_simulado >= modelo['tempo_simulacao']:
    componentes_finitos = s3000.__CalcOciosidadeFinal__(componentes_finitos, tempo_simulado)


print("Resultados da Simulação:")

a3000.__ResultsComponenteFinito__(componentes_finitos)
a3000.__ResultsComponenteFila__(componentes_filas)
a3000.__ResultsComponenteSaida__(componentes_saidas)
