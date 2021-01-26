import json
import random
from pprint import pprint
from simulador.simulador import Simulador

with open('model_config/model_config.json', 'r') as json_file:
    modelo = json.load(json_file)

s3000 = Simulador()

# [0]=tempo gerado | [1]=localização | [2]=destino | [3]=tempo gasto | [4]=chave dict
if modelo['componente_gerador']:
    entidades = s3000.__StructGerador__(modelo['componente_gerador'])
    pprint(entidades)

# origem, destino, estatísticas: [0]=qtd entidades | [1]=tmp espera | [2]=media espera | [3]=entidade que mais esperou
if modelo['componente_fila']:
    componentes_filas = s3000.__StructFila__(modelo['componente_fila'])
    pprint(componentes_filas)
    
# origem, destino, intervalo_gasto, estatísticas: [0]=qtd entidades | [1]=media de tmp ocioso | [2]=tmp permanencia | [3]=media permanencia, atendentes: tempo osioso p/ atendente [] | disponibilidade de cada atendente []
if modelo['componente_finito']:
    componentes_finitos = s3000.__StructComponenteFinito__(modelo['componente_finito'])
    pprint(componentes_finitos)

# origem, destino, intervalo_gasto, estatísticas: [0]=qtd entidades | [1]=tmp permanencia | [2]=media permanencia
if modelo['componente_infinito']:
    componentes_infinitos = s3000.__StructComponenteInfinito__(modelo['componente_infinito'])
    pprint(componentes_infinitos)

if modelo['componente_roteador']:
    componentes_roteadores = s3000.__StructRoteador__(modelo['componente_roteador'])
    pprint(componentes_roteadores)
    

# origem, estatísticas: [0]=qtd entidades | [1]=tmp total | [2]=media tempo no modelo
if modelo['componente_saida']:
    componentes_saidas = s3000.__StructSaida__(modelo['componente_saida'])
    pprint(componentes_saidas)

# Verificar nos componentes se Origem da entidade é != do próprio componente onde chegou, então verificar se é origem da saída e eliminar x entidade


print("\n\n\nSIMULAÇAO A PARTIR DESSE PONTO: \n")

# tempo_simulado = 0
# while (tempo_simulado < modelo['tempo_simulacao']):
#     entidade_atual = []
#     for item in sorted(entidades, key = entidades.get):
#         entidade_atual = entidades[item]
#         break

#     if entidade_atual == []:
#         tempo_simulado = modelo['tempo_simulacao']
#         break
#     else:
#         tempo_simulado = entidade_atual[0]
#         destino_entidade = entidade_atual[2][0]

#     print(tempo_simulado)
#     print('\n')
#     print(entidade_atual)
        

#     if destino_entidade == 'componente_roteador':
#         componentes_roteadores, entidade_atual = s3000.__roteando_rota__(componentes_roteadores, entidade_atual)
    
#     elif destino_entidade == 'componente_fila':
#         vector = s3000.__CalcFila__(componentes_filas, componentes_finitos, entidade_atual, modelo)
#         componentes_filas[vector[0]] = vector[1]
#         entidades[vector[2]] = vector[3]
    
#     elif destino_entidade == 'componente_finito':
#         vector = s3000.__CalcComponenteFinito__(componentes_finitos, entidade_atual, modelo)
#         componentes_finitos[vector[0]] = vector[1]
#         entidades[vector[2]] = vector[3]
    
#     elif destino_entidade == 'componente_infinito':
#         vector = s3000.__CalcComponenteInfinito__(componentes_infinitos, entidade_atual, modelo)
#         componentes_infinitos[vector[0]] = vector[1]
#         entidades[vector[2]] = vector[3]

#     elif destino_entidade == 'componente_saida':
#         vector = s3000.__CalcComponenteSaida__(componentes_saidas, entidade_atual)
#         componentes_saidas[vector[0]] = vector[1]
#         entidades.pop(vector[2])
#         pprint(entidades)

        

#pprint(modelo)
# print("\n")



