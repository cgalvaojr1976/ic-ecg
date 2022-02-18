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
from scipy import signal as sig
import matplotlib.pyplot as plt

record, fields = wfdb.rdsamp("/home/matheus/Documentos/Facul/IC/ECG_classification/ptb-diagnostic-ecg-database-1.0.0/todos/s0004_re", channels=[1])

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
    yh = sig.sosfilt(sos_l, yl)
    yd = sig.sosfilt(sos_d, yh)
    
    # Quadrado do filtro
    yp = np.power(yd,2)

    # Integração
    N_average = int(fs*0.15)
    y_a = np.convolve(yp.flatten(),np.ones(N_average), 'same') / N_average    
    
    threshold = y_a.mean() - y_a.std()

    #distance between peaks
    maximumBPM = 200
    distance = fs/(maximumBPM/60)

    peaks = sig.find_peaks(y_a,distance=distance,height=threshold)

    return peaks


def batimentos(sinal, fields):
    if fields["comments"][4] == "Reason for admission: Myocardial infarction": #caso haja arritmia
        picos = peaks(sinal)[0]
        matriz = []
        for posicao in picos:
            lista = []
            #Descartar primeiro e ultimo sinal
            if posicao > 250 and (posicao < (len(sinal) - 400)):
                for x in range(651):
                    lista.append(float(sinal[posicao-250+x]))
                lista.append(1) # Add na ultima coluna o tipo de batimento 
            matriz.append(lista) 

    elif fields["comments"][4] == "Reason for admission: Healthy control":
        picos = peaks(sinal)[0]
        matriz = []
        for posicao in picos:
            lista = []
            # Descartar o primeiro pico se ele for antes do instante 250 e
            # Descartar o último pico se ele estiver depois dos 400 últimos instantes
            if posicao > 250 and (posicao < (len(sinal) - 400)):
                for x in range(651):
                    lista.append(float(sinal[posicao-250+x]))
                lista.append(0) # Add na ultima coluna o tipo de batimento

            matriz.append(lista)
    else:
        return None

    return np.array(matriz)

# beats = batimentos(record)
# print(beats4)

