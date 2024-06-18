from PIL import Image
from pathlib import Path

def resize_img(file_path, largura, altura):
    with open(file_path, 'r') as file:
        rows = file.readlines()
    
    for row in rows:
        img_path = row.split()[0].replace('\\', '/')
        abs_img_path = Path(img_path)
    
        try:
            with Image.open(abs_img_path) as img:
                img_resized = img.resize((largura, altura))
                new_path = abs_img_path.parent / f'resized_{abs_img_path.name}'
                img_resized.save(new_path)
        except FileNotFoundError:
            print(f'Arquivo não encontrado: {abs_img_path}')
        except Exception as e:
            print(f'Erro ao processar {abs_img_path}: {e}')

largura = 320
altura = 180
resize_img('positives.txt', largura=largura, altura=altura)
