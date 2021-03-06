'''
Codigo feito para pré processar os dados de ECG a fim de
alimentar uma rede neural.
A rede neural irá precisar de 651 amostras de sinal, sendo 250
antes do pico de PanTompkins e 400 após o pico.
Esse algoritmo irá receber os dados dos arquivos e criar o sample
em um .csv
'''

import wfdb
import os
import shutil
import pantompkins
import csv


destino = "/home/matheus/Documentos/Facul/IC/ECG_classification/ptb-diagnostic-ecg-database-1.0.0/todos/lidos"
# import numpy as np
# import matplotlib.pyplot as plt

# Percorrer todo o diretorio de /database_part
with open("batimentos.csv", "w", newline='') as f:
    writer = csv.writer(f)

# Podia criar uma funcao aqui e passar no writer
    for root, dirs, files in os.walk("todos", topdown=False):
        for name in files:
            temp = name.split('.')
            if len(temp)==2:
                if name.split('.')[1] == 'hea':
                    diretorio = os.path.join(root, temp[0])
                    # Gravar os batimentos de um sinal
                    try:
                    	record, fields = wfdb.rdsamp(diretorio, channels=[1])
                    	beats = pantompkins.batimentos(record, fields)
                    #Excessão caso não haver o arquivo para ler os dados.
                    except:
                    	beats = None
                    if beats is not None:
                        for beat in beats:
                            writer.writerow(beat)
                    shutil.move(os.path.join(root, name), destino)
