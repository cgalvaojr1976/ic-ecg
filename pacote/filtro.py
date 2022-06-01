import pywt
from scipy import signal

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

    
    elif db_family == 6:
        coeff = pywt.wavedec(sig, 'db6', level=2) # Gerar coeficientes dos sinais
        cA2, cD2, cD1 = coeff # coeficientes do sinal
        cD1 = 0*cD1 # zerar altas frequências
        cD2 = 0*cD2 # zerar altas frequenceias
        return pywt.waverec([cA2,cD2,cD1], 'db6') # recosnstruir sinal