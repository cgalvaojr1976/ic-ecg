# ic-ecg
ECG anomaly detection
This repository contains several models and strategies employed in ECG/EKG anomaly detection, including support procedures (e.g Pan-Tompkins algorithm)

batimentos.py -->  apply_pant.ipynb --> concatenar.ipynb

## notebooks
### apply_pant.ipynb
Using a csv file created from batimentos.py, extract the beatings to another csv file
Each line contains the beatings and (last column ?)


### concatenar.ipynb
Notebook used to concatenate files created in "apply_pant" notebook.

### exploratory-v2.ipynb and exploratory.ipynb
Notebooks to explore the data

### leitura_notebook.ipynb
????
### PanTompkins.ipynb
????

## Pacote
### batimentos.py
Saves 'records1.csv' with all recordings with specified leads and codes (Dx)
Each line has:
- lead
- respective data
- Dx
- filename

### leitura.py
Saves a csv file (dataset name) with filenames and info data
Used to populate Total.csv file

### pantompkins.py
auxiliary functions to extract beatings from data


## Read Data
### ler_arquivo_wfdb
Using wdbf library

## Support
### Pan-Tompkins-algorithm.ipynb
Notebook showing Pan-tompkins based peak detection

### Pan-Tompkins-algorithm_general_filter.ipynb
Notebook showing Pan-tompkins based peak detection, but using custom low-pass and high-pass filters designed by the authors 

### make_sample.py
????????