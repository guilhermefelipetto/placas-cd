import os

def convert_annotations_to_positives(directories, output_file):
    with open(output_file, 'w') as out_file:
        for input_dir in directories:
            for filename in os.listdir(input_dir):
                if filename.endswith('.txt'):
                    image_name = filename.replace('.txt', '.jpg')
                    image_path = os.path.join(input_dir, image_name)
                    txt_path = os.path.join(input_dir, filename)
                    
                    with open(txt_path, 'r') as f:
                        lines = f.readlines()
                        corners_line = [line for line in lines if line.startswith('corners')][0]
                        corners = corners_line.split(': ')[1].strip()
                        corners = corners.split(' ')
                        x1, y1 = map(int, corners[0].split(','))
                        x2, y2 = map(int, corners[2].split(','))
                        
                        width = x2 - x1
                        height = y2 - y1
                        
                        out_file.write(f"{image_path} 1 {x1} {y1} {width} {height}\n")

# verifica isso aqui pra ve se tua ordem de diretorios ta certa
directories = [
    'dados/RodoSol-ALPR/images/cars-me',
    'dados/RodoSol-ALPR/images/cars-br',
    'dados/RodoSol-ALPR/images/motorcycles-me',
    'dados/RodoSol-ALPR/images/motorcycles-br'
]

"""
se seu caminho dos dados nao estiver assim vc vai colocar o caminho certo pra cada pasta,
e rodar o codigo, ele vai gerar um positives.txt, se gerou eh pq funcionou legal
"""

# dxa assim, confia
output_file = 'positives.txt'
convert_annotations_to_positives(directories, output_file)
