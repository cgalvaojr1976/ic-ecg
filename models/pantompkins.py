import wfdb
import numpy as np

record, fields = wfdb.rdsamp("database_part/s0004_re", channels=[0])

def pass_baixa(sinal):
    lowpass = np.zeros(len(sinal)+1)
    for i in range(12, len(lowpass)-2):
        lowpass[i] = 2*lowpass[i+1] - lowpass[i-2] + (1/32*(sinal[i] - 2*sinal[i-6] + sinal[i-12]))
    return lowpass 

teste = pass_baixa(record)

print(teste)