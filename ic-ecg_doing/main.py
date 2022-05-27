import batimentos

codigo = [164947007]
leads = [2]
diretorio = '../data/'
n_files = 500

for x in range(4):
    batimentos.records(diretorio,codigo,leads,n_files,x)

