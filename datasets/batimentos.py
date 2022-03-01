'''Esse código tem a finalidade de criar uma tabela com os batimentos e
suas labels.
Obs: Para o código funcionar a tabela 'Total.csv' deve estar no mesmo 
local desse script.
'''

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import wfdb

diretorio = '/home/matheus/Documentos/Facul/IC/ECG_classification/data/'

# Lista com os códigos que precisamos
codigo = ['426627000']

# Lista dos leads
leads = [0,1,2]

def records(diretorio, codigo, leads):
    # Criar tabela que contenha os Datasets e os Arquivos com os códigos
    data_frame = pd.read_csv('/home/matheus/Documentos/Facul/IC/ECG_classification/ic-ecg/datasets/Total.csv')
    print(data_frame)
    # Cria tabela com apenas os códigos necessários
    df = pd.DataFrame(columns= ['arquivos', 'base', 'Dx'])
    df = df.append(data_frame.loc[lambda data_frame: data_frame['Dx'] == codigo[x]])

    df = df.reset_index()
    print(df)
    #Cria a tabela dos records
    records = pd.DataFrame()
    # Leitura dos records
    for x in range(len(df)):
        destino = diretorio + df.loc[x]['base'] + '/' + df.loc[x]['arquivos']
        print(destino)

        if df.loc[x]['fs'] == 500.0:
            record, fields = wfdb.rdsamp(destino, channels = leads, sampto= 5000)
        elif df.loc[x]['fs'] == 1000.0:
            record, fields = wfdb.rdsamp(destino, channels = leads, sampto= 5000)
        elif df.loc[x]['fs'] == 257:
            record, fields = wfdb.rdsamp(destino, channels = leads, sampto= 5000)

        # Colocar o record em uma data_frame Junto com seu código
        aux = pd.DataFrame(record.transpose())
        # Inserir a linha com o nome da arritmia
        aux['arritmia'] = int(df.loc[x]['Dx'])
        # Inserir coluna de leads
        aux['leads'] = leads
        # Inserir a coluna com nome do arquivo
        aux['arquivo'] = df.loc[x]['arquivos']
        records = records.append(aux)

    # Gravar Tabela
    records.to_csv('records1.csv')

records(diretorio,codigo,leads)