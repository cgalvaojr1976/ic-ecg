'''Esse código tem a finalidade de criar uma tabela com os batimentos e
suas labels.

TODO: 
    use input and output directories as arguments
    fix sampling rate

    
'''

import pandas as pd
#import numpy as np
#import matplotlib.pyplot as plt
import wfdb

diretorio = '../all_data/'

# Lista com os códigos que precisamos
codigo = [164947007]
#codigo=[426783006]
# Lista dos leads
leads = [2]

def records(diretorio, codigo, leads, n_Files, resample=False, fs=500, denoise=0):
    '''
    resample - boolean: resample or not
    fs - int: default sampling rate for resampling
    denoise - int: 0-nothing
                   1-Butterworth
                   2-DWT
    '''
    # Criar tabela que contenha os Datasets e os Arquivos com os códigos
    data_frame = pd.read_csv('../datasets/Total.csv')
    # Cria tabela com apenas os códigos necessários
    df = pd.DataFrame(columns= ['arquivos', 'base', 'Dx'])

    for x in range(len(codigo)):
        df = df.append(data_frame.loc[data_frame['Dx'] == codigo[x]])
    
    df = df.sample(frac=1).reset_index(drop=True)
    #Cria a tabela dos records
    records = pd.DataFrame()

    # Leitura dos records
    for x in range(min(len(df),n_Files)):

        destino = diretorio + df.loc[x]['base'] + '/' + df.loc[x]['arquivos']
         
        record, fields = wfdb.rdsamp(destino, channels = leads, sampto= int(df.loc[x]['fs']*10))
        #if df.loc[x]['fs'] != 500.0:
            #resample if necessary
        # clean if necessary
            
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

    # Gravar Tabela
    records.to_csv('../records/records1'+str(codigo)+str(denoise)+'.csv')
    print(str(x+1) + ' files used')

records(diretorio,codigo,leads,n_Files=500)