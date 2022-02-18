'''Esse código tem a finalidade de criar uma tabela com os batimentos e
suas labels.
Obs: Para o código funcionar a tabela 'Total.csv' deve estar no mesmo 
local desse script.
'''

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import wfdb

# diretorio = '/home/matheus/Documentos/Facul/IC/ECG_classification/data/'

# Lista com os códigos que precisamos
# codigo = ['10370003', '164947007'] # PR e LPR

# Lista dos leads
# leads = [0,1,2]

def records(diretorio, codigo, leads):
    # Criar tabela que contenha os Datasets e os Arquivos com os códigos
    data_frame = pd.read_csv('Total.csv')

    # Cria tabela com apenas os códigos necessários
    df = pd.DataFrame(columns= ['arquivos', 'base', 'Dx'])
    for x in range(len(codigo)):
        df = df.append(data_frame.loc[lambda data_frame: data_frame['Dx'] == codigo[x]])

    df = df.reset_index()
    #Cria a tabela dos records
    records = pd.DataFrame()
    # Leitura dos records
    for x in range(len(df)):
        destino = diretorio + df.loc[x]['base'] + '/' + df.loc[x]['arquivos']
        record, fields = wfdb.rdsamp(destino, channels = leads)
        # Inserir linha de leads
        record = np.insert(record, 0 , leads, axis= 0)
        # Inserir lina de código de arritmia
        record = np.insert(record, 1, [df.loc[x]['Dx'] for x in range(len(leads))], axis= 0)
        # Colocar o record em uma data_frame Junto com seu código
        aux = pd.DataFrame(record.transpose())
        records = records.append(aux)

    # Gravar Tabela
    records.to_csv('records.csv')
