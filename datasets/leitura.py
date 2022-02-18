'''Esse código tem a finalidade de criar as tabalas de cada
banco de dados com todos os seus diagnósticos'''

'''Bases de dados:
"WFDB_ChapmanShaoxing 10,247 recordings ok 0 erros"
"WFDB_CPSC2018 6,877 recordings ok 0 erros"
"WFDB_CPSC2018_2 3,453 recordings ok 0 erros"
"WFDB_Ningbo 34,905 records ok 0 erros"
"WFDB_PTB  516 recordings ok 0 erros"
"WFDB_PTBXL 21,837 recordings ok 0 erros"
"WFDB_StPetersburg 74 recordings ok 0 erros"
'''

import wfdb
import os
import numpy as np
import pandas as pd

pd.options.mode.chained_assignment = None

diretorio = '/home/matheus/Documentos/Facul/IC/ECG_classification/data/'

def salvar(base):
    problemas = 0

    fields = [] # Campos dos fields
    nomes = [] # Nome dos files

    # Caminhar pelo diretório escolhido
    for root, dirs, files in os.walk(diretorio+base, topdown=False):
        for name in files:
            temp = name.split('.')
            if len(temp)==2:
                if name.split('.')[1] == 'hea':
                    arquivo = os.path.join(root, temp[0])
                    try:
                        # Leitura dos fields e dos records
                        # Não é necessário a leitura dos recors agora
                        record, field = wfdb.rdsamp(arquivo, channels=[1]) 
                        # Colocar nomes dos arquivos na lista de nomes
                        nomes.append(name.split('.')[0])
                        fields.append(field)
                    except:
                        problemas += 1
    print('base: ', base, ' problemas: ', problemas)

    # Criar tabela com os fields separados
    for y in range(len(fields)):
        for x in range(len(fields[y]['comments'])):
            # Transformar os comentários em apenas os números
            fields[y][fields[y]['comments'][x].split(": ")[0]] = fields[y]['comments'][x].split(": ")[1]

    df = pd.DataFrame(fields)
    df['arquivos'] = nomes
    df['base'] = base
    df = df.drop('comments', 1)

    # Substituir as linhas com mais de um diagnóstico
    for x in range(len(df)):
        # Caso haja mais de um diagnóstico
        if len(df.loc[x]['Dx'].split(',')) > 1:
            valores = df.loc[x]['Dx'].split(',')
            # Criar lista de valores para substituírem
            lista = [df.loc[x] for y in range(len(valores))]
            # Modificar a lista com cada diagnóstico correto
            for y in range(len(lista)):
                lista[y]['Dx'] = valores[y]
                # Colocar lista na data frame
                df = df.append(lista[y])

    df = df.reset_index()

    # Remover as linhas com mais de um diagnóstico
    for x in range(len(df)):
        if len(df.loc[x]['Dx'].split(',')) > 1:
            df = df.drop(x)

    # Salva a dataframe em um .csv
    df.to_csv(base+'.csv')

salvar(base = 'WFDB_PTBXL')
salvar(base = 'WFDB_PTB')
salvar(base = 'WFDB_StPetersburg')