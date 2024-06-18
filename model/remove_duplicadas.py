import os
from PIL import Image
import imagehash


def remove_duplicate_images(dir):
    hashes = {}
    files_to_remove = []

    for filename in os.listdir(dir):
        if filename.endswith('.jpg'):
            filepath = os.path.join(dir, filename)
            try:
                with Image.open(filepath) as img:
                    hash = imagehash.average_hash(img)
                
                if hash in hashes:
                    files_to_remove.append(filepath)
                else:
                    hashes[hash] = filename
            except OSError as e:
                print(f'erro ao processar imagem {filename}: {e}')
    
    for file in files_to_remove:
        os.remove(file)
        print(f'imagem removida: {file}')
    
    print('duplicadas removidas com sucesso')


remove_duplicate_images('negatives')