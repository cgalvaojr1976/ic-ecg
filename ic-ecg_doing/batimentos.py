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
import pywt
from scipy import signal

diretorio = '../data/'

# Lista com os códigos que precisamos
codigo = [164947007]
#codigo=[426783006]
# Lista dos leads
leads = [2]

def denoise_fir(sig, fs, cuthigh, cutlow):
    sos = signal.butter(10, [cutlow, cuthigh], 'bandpass', fs=fs, output='sos', analog= False) # Criar filtro
    return signal.sosfilt(sos, sig) # Convoluir filtro

def denoise_wavelet(db_family, sig):

    if db_family == 2:
        coeff = pywt.wavedec(sig, 'db2', level=2) # Gerar coeficientes dos sinais
        cA2, cD2, cD1 = coeff # coeficientes do sinal
        cD1 = 0*cD1 # zerar altas frequências
        cD2 = 0*cD2 # zerar altas frequenceias
        return pywt.waverec([cA2,cD2,cD1], 'db2') # recosnstruir sinal
    
    elif db_family == 3:
        coeff = pywt.wavedec(sig, 'db6', level=2) # Gerar coeficientes dos sinais
        cA2, cD2, cD1 = coeff # coeficientes do sinal
        cD1 = 0*cD1 # zerar altas frequências
        cD2 = 0*cD2 # zerar altas frequenceias
        return pywt.waverec([cA2,cD2,cD1], 'db6') # recosnstruir sinal
    
def records(diretorio, codigo, leads, n_Files, denoise=0):
    '''
    argumentos denoise
    0 -> sem
    1 -> fir
    2 -> db2
    3 -> db6
    '''

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
        
        if denoise == 1:
            record = denoise_fir(record, 500, 0.5, 50)

        elif denoise == 2:
            record = denoise_wavelet(denoise, record)

        elif denoise == 3:
            record = denoise_wavelet(denoise, record)

            
        # Colocar o record em uma data_frame Junto com seu código
        aux = pd.DataFrame(record.transpose())
        # Inserir a linha com o nome da arritmia
        aux['arritmia'] = int(df.loc[x]['Dx'])
        # Inserir coluna de leads
        print(leads)
        aux['leads'] = leads[0]
        #Inserir coluna de fs
        aux['fs'] = df.loc[x]['fs']
        # Inserir a coluna com nome do arquivo
        aux['arquivo'] = df.loc[x]['arquivos']
        records = records.append(aux)

    # Gravar Tabela
    if denoise == 0:
        records.to_csv('signal'+str(codigo)+'no_filter.csv')
        print(str(x+1) + ' files used')
    elif denoise == 1:
        records.to_csv('signal'+str(codigo)+'fir_filter.csv')
        print(str(x+1) + ' files used')
    elif denoise == 2:
        records.to_csv('signal'+str(codigo)+'db2_filter.csv')
        print(str(x+1) + ' files used')
    elif denoise == 3:
        records.to_csv('signal'+str(codigo)+'db6_filter.csv')
        print(str(x+1) + ' files used')
