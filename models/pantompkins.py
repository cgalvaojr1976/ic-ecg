'''
Código representado no notebook PanTompkins

O algoritmo de Pan & Tompkins passa por 6 diferentes fazes
ele foi feito para representação em tempo real, portanto
nesse código só foi feito até a quinta parte.
Primeiramente um filtro passa baixa é utilizado seguido de um passa alta.
Depois deriva o sinal e o eleva ao quadrado. Por fim faz a integração em um
determinado intervalo.
Após todos os passos 
'''

import wfdb
import numpy as np
# from scipy import signal as sig
# import matplotlib.pyplot as plt

# record, fields = wfdb.rdsamp("database_part/s0004_re", channels=[0])

def passa_baixa(sinal):
    lowpass = np.copy(sinal)
    for i in range(12,len(lowpass)-1):
        lowpass[i] = (2*lowpass[i-1]) - (lowpass[i-2]) + (sinal[i] - (2*sinal[i-6]) + sinal[i-12])
    return lowpass

def passa_alta(sinal):
    hightpass = np.copy(sinal)
    for i in range(32,len(hightpass)-1):
        hightpass[i] = hightpass[i-1] - (sinal[i]/32) + sinal[i-16] - sinal[i-17] + (sinal[i-32]/32)
    return hightpass

def diferencial(sinal):
    derivative = np.copy(sinal)
    for i in range(len(derivative)-1):
        derivative[i] = (1/8)*(2*sinal[i] + sinal[i-1] - sinal[i-3] - 2*sinal[i-4])
    return derivative

def integration(n, sinal):
    integra = np.copy(sinal)
    for i in range(len(integra)):
        # Fazer somatorio primeiro
        somatorio = 0
        for j in range(n):
            somatorio = somatorio + sinal[i-(n-j)] 
        integra[i] = 1/n * somatorio
    return integra

def pan_peak(sinal):
    '''Se passar de um determinado limiar
    detecta uma subida e salva esse ponto
    a hora que passa abaixo do limiar salva o ponto de descida.
    O pico será a mediana entre os sinais.
    Retorna os momento dos picos.
    '''
    limiar = 0.8
    digital_b = 0 # Verifica o limiar no momento anterior
    digital_a = 0 # Verifica o limiar no momento atual
    subida = [] # posicai de subida
    descida = [] # posicao de descida
    pos = [] # posicao dos picos
    sig = passa_baixa(sinal)
    sig = passa_alta(sig)
    sig = diferencial(sig)
    sig = np.power(sig,2)
    sig = integration(40, sig)

    for x in range(len(sig)):
        #verificacao de limiar
        if sig[x] > limiar:
            digital_a = 1
        else:
            digital_a = 0
        #verificacao de subida
        if digital_a == 1 and digital_b == 0:
            subida.append(x)
        #verificacao de descida
        if digital_a == 0 and digital_b == 1:
            descida.append(x)
            
        digital_b = digital_a
        
    for x in range(len(descida)):
        pos.append(subida[x] + ((descida[x] - subida[x]) // 2))
    
    return pos

#picos = pan_peak(record)

def batimentos(sinal, fields):
    if fields["comments"][4] == "Reason for admission: Myocardial infarction": #caso haja arritmia
        picos = pan_peak(sinal)
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
        picos = pan_peak(sinal)
        matriz = []
        for posicao in picos:
            lista = []
            #Descartar primeiro e ultimo sinal
            if posicao > 250 and (posicao < (len(sinal) - 400)):
                for x in range(651):
                    lista.append(float(sinal[posicao-250+x]))
                lista.append(0) # Add na ultima coluna o tipo de batimento
            matriz.append(lista)
    else:
        return None

    return np.array(matriz)

# beats = batimentos(record)
# print(beats[4])
