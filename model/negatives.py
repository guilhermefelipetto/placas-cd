import os

diretorio = 'negatives'
output_file = 'negatives.txt'

with open(output_file, 'w') as f:
    for arquivo in os.listdir(diretorio):
        if arquivo.lower().endswith('.jpg'):
            caminho_completo = os.path.join(diretorio, arquivo)
            f.write(caminho_completo + f'\n')
