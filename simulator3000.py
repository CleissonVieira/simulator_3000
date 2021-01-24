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

if modelo['fila']:
    # origem, destino, estatísticas: [0]=qtd entidades | [1]=tmp chegada | [2]=tmp saida | [3]=tmp espera | [4]=media espera | [5]=entidade que mais esperou
    filas = s3000.__StructFila__(modelo['fila'])

if modelo['componentes_finito']:
    # origem, destino, intervalo_gasto, estatísticas: [0]=qtd entidades | [1]=tmp chegada | [2]=tmp saida | [3]=media de tmp ocioso | [4]=tmp permanencia | [5]=media permanencia, atendentes: tempo osioso p/ atendente [] | disponibilidade de cada atendente []
    componentes_finito = s3000.__StructComponenteFinito__(modelo['componentes_finito'])

if modelo['componentes_infinito']:
    # origem, destino, intervalo_gasto, estatísticas: [0]=qtd entidades | [1]=tmp chegada | [2]=tmp saida | [3]=tmp permanencia | [4]=media permanencia
    componentes_infinito = s3000.__StructComponenteInfinito__(modelo['componentes_infinito'])

if modelo['roteadores']:
    roteadores = modelo['roteadores']

if modelo['componentes_saida']:
    componentes_saida = modelo['componentes_saida']

# Verificar nos componentes se Origem da entidade é != do próprio componente onde chegou, então verificar se é origem da saída e eliminar x entidade