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

destino = "/home/matheus/Documentos/Facul/IC/ECG_classification/ic-ecg/models/database_part2"
# import numpy as np
# import matplotlib.pyplot as plt

# Percorrer todo o diretorio de /database_part
with open("batimentos.csv", "w", newline='') as f:
    writer = csv.writer(f)

# Podia criar uma funcao aqui e passar no writer
    for root, dirs, files in os.walk("models/database_part", topdown=False):
        for name in files:
            temp = name.split('.')
            if len(temp)==2:
                if name.split('.')[1] == 'hea':
                    writer.writerow([temp[0]])
                    record, fields = wfdb.rdsamp(os.path.join(root, temp[0]), channels=[0])
                    # Gravar os batimentos de um sinal
                    beats = pantompkins.batimentos(record, fields)
                    if beats is not None:
                        for beat in beats:
                            writer.writerow(beat)
                    shutil.move(os.path.join(root, name), destino)
