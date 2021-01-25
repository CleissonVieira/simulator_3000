import json
import random
from pprint import pprint
from simulador.simulador import Simulador

with open('model_config/model_config.json', 'r') as json_file:
    modelo = json.load(json_file)

s3000 = Simulador()

# [0]=tempo gerado | [1]=localização | [2]=destino | [3]=tempo gasto | [4]=chave dict
if modelo['gerador_entidades_temporarias']:
    entidades = s3000.__GeradorEntidades__(modelo['gerador_entidades_temporarias'])
    pprint(entidades)

# origem, destino, estatísticas: [0]=qtd entidades | [1]=tmp espera | [2]=media espera | [3]=entidade que mais esperou
if modelo['fila']:
    filas = s3000.__StructFila__(modelo['fila'])
    pprint(filas)
    
# origem, destino, intervalo_gasto, estatísticas: [0]=qtd entidades | [1]=media de tmp ocioso | [2]=tmp permanencia | [3]=media permanencia, atendentes: tempo osioso p/ atendente [] | disponibilidade de cada atendente []
if modelo['componentes_finito']:
    componentes_finito = s3000.__StructComponenteFinito__(modelo['componentes_finito'])
    pprint(componentes_finito)

# origem, destino, intervalo_gasto, estatísticas: [0]=qtd entidades | [1]=tmp permanencia | [2]=media permanencia
if modelo['componentes_infinito']:
    componentes_infinito = s3000.__StructComponenteInfinito__(modelo['componentes_infinito'])
    pprint(componentes_infinito)

if modelo['roteadores']:
    roteadores = modelo['roteadores']
    pprint(roteadores)

# origem, estatísticas: [0]=qtd entidades | [1]=tmp total | [2]=media tempo no modelo
if modelo['componentes_saida']:
    componentes_saida = s3000.__StructSaida__(modelo['componentes_saida'])
    pprint(componentes_saida)

# Verificar nos componentes se Origem da entidade é != do próprio componente onde chegou, então verificar se é origem da saída e eliminar x entidade


print("\n\n\nSIMULAÇAO A PARTIR DESSE PONTO: \n")

tempo_simulado = 0
while (tempo_simulado < modelo['tempo_simulacao']):
    for item in sorted(entidades, key = entidades.get):
        entidade_atual = entidades[item]
        break
    
    tempo_simulado = entidade_atual[0]
    destino_entidade = entidade_atual[2][0]

    print(tempo_simulado)
    print('\n')
    print(entidade_atual)

    if destino_entidade == 'roteadores':
        roteadores, entidade_atual = s3000.__roteando_rota__(roteadores, entidade_atual)
    
    elif destino_entidade == 'fila':
        vector = s3000.__CalcFila__(filas, entidade_atual, modelo)
        filas[vector[0]] = vector[1]
        entidades[vector[2]] = vector[3]
    
    elif destino_entidade == 'componentes_finito':
        vector = s3000.__CalcComponenteFinito__(componentes_finito, entidade_atual, modelo)
        componentes_finito[vector[0]] = vector[1]
        entidades[vector[2]] = vector[3]
    
    elif destino_entidade == 'componentes_infinito':
        vector = s3000.__CalcComponenteInfinito__(componentes_infinito, entidade_atual, modelo)
        componentes_infinito[vector[0]] = vector[1]
        entidades[vector[2]] = vector[3]

    elif destino_entidade == 'componentes_saida':
        vector = s3000.__CalcFila__(componentes_saida, entidade_atual, modelo)
        componentes_saida[vector[0]] = vector[1]
        # entidades.pop(vector[2])
        break

pprint(modelo)
# print("\n")
pprint(entidades)



