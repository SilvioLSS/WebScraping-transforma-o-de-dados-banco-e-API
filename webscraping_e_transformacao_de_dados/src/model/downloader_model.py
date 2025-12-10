import requests
import os
import time

class DonwloaderModel:

    def donwload(self, url, caminho):

        if not url.startswith('http'):
            raise ValueError("URL inválida")
        
        pasta = os.path.dirname(caminho)
        if pasta:
            os.makedirs(pasta, exist_ok=True)

        download = requests.get(url, stream=True, timeout=30)
        download.raise_for_status()

        with open(caminho, 'wb') as arquivo:
            for parte in download.iter_content(chunk_size=8192):
                arquivo.write(parte)

        if os.path.getsize(caminho) > 0:
            print(f"[DOWNLOADER] Salvo: {caminho}")
            return True
        else:
            os.remove(caminho)
            print("[DOWNLOADER] Arquivo vazio")
        return False
        
