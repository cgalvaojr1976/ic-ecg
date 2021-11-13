import wfdb
import numpy as np
from scipy import signal as sig
import matplotlib.pyplot as plt

record, fields = wfdb.rdsamp("database_part/s0004_re", channels=[0])
tamanho = np.linspace(0, len(record), num = len(record))


def pass_baixa(sinal):
    lowpass = np.copy(sinal)
    for i in range(12, len(lowpass)-1):
        lowpass[i] = (2*lowpass[i-1]) - (lowpass[i-2]) + ((1/32)*(sinal[i] - 2*sinal[i-6] + sinal[i-12]))
    return lowpass 

teste = pass_baixa(record)


plt.figure(figsize=(10,5))
plt.xlabel(xlabel="Time(ms)")
plt.ylabel(ylabel="Amplitude")
plt.plot(tamanho[0:4000], teste[0:4000])
plt.show()
