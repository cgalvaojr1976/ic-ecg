'''Esse código tem a finalidade de criar uma tabela com os batimentos e
suas labels.

TODO:
    use input and output directories as arguments
    fix sampling rate

    
'''

import pandas as pd
import numpy as np
from scipy import signal
import wfdb
    
def records(diretorio, codigo, leads, n_Files):


    # Criar tabela que contenha os Datasets e os Arquivos com os códigos
    data_frame = pd.read_csv('/home/matheus/Documentos/Facul/IC/ECG_classification/ic-ecg/datasets/Total.csv')
    # Cria tabela com apenas os códigos necessários
    df = pd.DataFrame(columns= ['arquivos', 'base', 'Dx', 'fs'])

    for x in range(len(codigo)):
        df = df.append(data_frame.loc[data_frame['Dx'] == codigo[x]])
    
    df = df.sample(frac=1).reset_index(drop=True)

    #Cria a tabela dos records
    records = pd.DataFrame()

    # Leitura dos records
    for x in range(min(len(df),n_Files)):

        destino = diretorio + df.loc[x]['base'] + '/' + df.loc[x]['arquivos']
         
        if df.loc[x]['fs'] == 500.0:
            record, fields = wfdb.rdsamp(destino, channels = leads, sampto= int(df.loc[x]['fs']*10))
        elif df.loc[x]['fs'] == 1000:
            record, fields = wfdb.rdsamp(destino, channels = leads, sampto= int(df.loc[x]['fs']*10))
            record = signal.resample(record,5000)
        elif df.loc[x]['fs'] == 254:
            record, fields = wfdb.rdsamp(destino, channels = leads, sampto= int(df.loc[x]['fs']*10))
            record = signal.resample(record,5000)
            
        # Colocar o record em uma data_frame Junto com seu código
        aux = pd.DataFrame(record.transpose())
        # Inserir a linha com o nome da arritmia
        aux['arritmia'] = int(df.loc[x]['Dx'])
        # Inserir coluna de leads
        aux['leads'] = leads
        #Inserir coluna de fs
        aux['fs'] = df.loc[x]['fs']
        # Inserir a coluna com nome do arquivo
        aux['arquivo'] = df.loc[x]['arquivos']
        records = records.append(aux)
        
    return records
