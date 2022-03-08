'''
O algoritmo de Pan & Tompkins passa por 6 diferentes fases
ele foi feito para representação em tempo real, portanto
nesse código só foi feito até a quinta parte.
Primeiramente um filtro passa baixa é utilizado seguido de um passa alta.
Depois deriva o sinal e o eleva ao quadrado. Por fim faz a integração em um
determinado intervalo.
Após todos os passos 
'''

import wfdb
import numpy as np
import pandas as pd
from scipy import signal as sig
import matplotlib.pyplot as plt


def peaks(signal, frequencia):
    fs = frequencia
    
    # vetores dos filtros
    low_b = np.zeros(13)
    low_b[0] = 1
    low_b[6] = -2
    low_b[12] = 1
    low_a = np.array([1,-2,1])
    
    # Passa baixa
    sos_l = sig.tf2sos(b=low_b,a=low_a)
    
    high_b = np.zeros(33)
    high_b[0] = -1/32
    high_b[16] = 1
    high_b[17] = -1
    high_b[32] = 1/32 
    high_a = np.array([1,-1])
    
    # Passa alta
    sos_h = sig.tf2sos(b=high_b,a=high_a)
    
    deriv_b = np.array([2,3,9,-1,-2])
    deriv_b = deriv_b/8
    
    deriv_a = 1
    
    # Derivada
    sos_d = sig.tf2sos(b=deriv_b,a=deriv_a)
    
    # Aplica filtro
    yl = sig.sosfilt(sos_l,signal)
    yh = sig.sosfilt(sos_h, yl)
    yd = sig.sosfilt(sos_d, yh)
    
    # Quadrado do filtro
    yp = np.power(yd,2)

    # Integração
    N_average = int(fs*0.15)
    y_a = np.convolve(yp.flatten(),np.ones(N_average), 'same') / N_average    
    
    threshold = y_a.mean() + y_a.std()

    #distance between peaks
    maximumBPM = 200
    distance = fs/(maximumBPM/60)

    peaks = sig.find_peaks(y_a,distance=distance,height=threshold)
    # O pico fica deslocado 30 capturas a frente

    return peaks


def batimentos(sinal, codigo, frequencia, lead):
    picos = peaks(sinal, frequencia)
    df = pd.DataFrame()

    for posicao in picos[0]:
        #Descartar batimentos incompletos
        if posicao > 250 and (posicao < (len(sinal) - 400)):
            batimento = []

            for x in range(651):
                batimento.append(float(sinal[posicao-250+x]))

            batimento.append(codigo) # Add na ultima coluna o tipo de batimento
            batimento.append(lead) # Add na ultima coluna o tipo de batimento
            batimento_s = pd.Series(batimento)
            df = df.append(batimento_s, ignore_index=True)

    return df


# beats = batimentos(record)
# print(beats4)

