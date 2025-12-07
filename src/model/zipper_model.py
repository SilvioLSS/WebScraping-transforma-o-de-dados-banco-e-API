import zipfile
import os

class ZipperModel:
    
    @staticmethod
    def criar_zip(pasta_origem, nome_zip=None):
        try:
            if not os.path.exists(pasta_origem):
                return {'sucesso': False, 'erro': f'Pasta não existe: {pasta_origem}'}
            
            if not nome_zip:
                nome_pasta = os.path.basename(pasta_origem)
                nome_zip = f"{nome_pasta}_anexos.zip"
            
            caminho_zip = os.path.join(pasta_origem, nome_zip)
            
            print(f"[ZIP MODEL] Criando: {caminho_zip}")
            
            arquivos_pdf = []
            for item in os.listdir(pasta_origem):
                item_path = os.path.join(pasta_origem, item)
                
                if os.path.isfile(item_path) and item.lower().endswith('.pdf'):
                    arquivos_pdf.append(item_path)
            
            if not arquivos_pdf:
                return {'sucesso': False, 'erro': 'Nenhum PDF encontrado'}
            
            with zipfile.ZipFile(caminho_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for arquivo in arquivos_pdf:
                    nome_no_zip = os.path.basename(arquivo)
                    zipf.write(arquivo, nome_no_zip)
                    print(f"[ZIP MODEL] + {nome_no_zip}")
            
            tamanho = os.path.getsize(caminho_zip)
            return {
                'sucesso': True,
                'caminho_zip': caminho_zip,
                'tamanho_bytes': tamanho,
                'tamanho_mb': round(tamanho / (1024 * 1024), 2),
                'quantidade_arquivos': len(arquivos_pdf),
                'arquivos': [os.path.basename(a) for a in arquivos_pdf]
            }
            
        except Exception as e:
            return {'sucesso': False, 'erro': str(e)}
    