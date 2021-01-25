import json
import random
from pprint import pprint
from simulador.simulador import Simulador

with open('model_config/model_config.json', 'r') as json_file:
    modelo = json.load(json_file)

s3000 = Simulador()

if modelo['gerador_entidades_temporarias']:
    # [0]=tempo gerado | [1]=ativo ou não | [2]=localização | [3]=destino | [4]=tempo gasto
    entidades = s3000.__GeradorEntidades__(modelo['gerador_entidades_temporarias'])
    pprint(entidades)
    
if modelo['fila']:
    # origem, destino, estatísticas: [0]=qtd entidades | [1]=tmp espera | [2]=media espera | [3]=entidade que mais esperou
    filas = s3000.__StructFila__(modelo['fila'])
    pprint(filas)

if modelo['componentes_finito']:
    # origem, destino, intervalo_gasto, estatísticas: [0]=qtd entidades | [1]=tmp chegada | [2]=tmp saida | [3]=media de tmp ocioso | [4]=tmp permanencia | [5]=media permanencia, atendentes: tempo osioso p/ atendente [] | disponibilidade de cada atendente []
    componentes_finito = s3000.__StructComponenteFinito__(modelo['componentes_finito'])
    pprint(componentes_finito)

if modelo['componentes_infinito']:
    # origem, destino, intervalo_gasto, estatísticas: [0]=qtd entidades | [1]=tmp chegada | [2]=tmp saida | [3]=tmp permanencia | [4]=media permanencia
    componentes_infinito = s3000.__StructComponenteInfinito__(modelo['componentes_infinito'])
    pprint(componentes_infinito)

if modelo['roteadores']:
    roteadores = modelo['roteadores']
    pprint(roteadores)

if modelo['componentes_saida']:
    componentes_saida = modelo['componentes_saida']
    pprint(componentes_saida)

# Verificar nos componentes se Origem da entidade é != do próprio componente onde chegou, então verificar se é origem da saída e eliminar x entidade


print("\n\n\nSIMULAÇAO A PARTIR DESSE PONTO: \n")

count = 0
while (count < modelo['tempo_simulacao']):
    for item in sorted(entidades, key = entidades.get):
        entidade_atual = entidades[item]
        break
    
    count = entidade_atual[0]

    if entidade_atual[3][0] == 'roteadores':
        roteadores, entidade_atual = s3000.__roteando_rota__(roteadores, entidade_atual)
    elif entidade_atual[3][0] == 'fila':
        vector = s3000.__CalcFila__(filas, entidade_atual, modelo)
        filas[vector[0]] = vector[1]
        entidades[vector[2]] = vector[3]
    elif entidade_atual[3][0] == 'componentes_finito':
        vector = s3000.__CalcComponenteFinito__(componentes_finito, entidade_atual, modelo)
        componentes_finito[vector[0]] = vector[1]
        entidades[vector[2]] = vector[3]
        break
    elif entidade_atual[3][0] == 'componentes_infinito':
        componentes_infinito, entidade_atual = s3000.__CalcComponenteInfinito__(componentes_infinito, entidade_atual)
    elif entidade_atual[3][0] == 'componentes_saida':
        componentes_saida, entidade_atual = s3000.__componenteSaida__(componentes_saida, entidade_atual)


# pprint(modelo)
# pprint(entidades)



