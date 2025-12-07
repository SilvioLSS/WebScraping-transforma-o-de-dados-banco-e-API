import os 
from datetime import datetime 

class ScrapingController:
        def __init__(self):
            from model.scraper_model import ScraperModel
            from model.downloader_model import DonwloaderModel
            from model.zipper_model import ZipperModel

            self.scraper = ScraperModel()
            self.downloader = DonwloaderModel()
            self.zipper_model = ZipperModel() 
            

        def criar_pasta_pdfs(self):
            hoje = datetime.now().strftime("%Y-%m-%d")
            pasta = os.path.join("statics/pdfs", hoje)
            os.makedirs(pasta, exist_ok=True)
            return pasta

        def executar(self):
            try:
                anexos = self.scraper.buscar_anexos()

                if not anexos:
                    return {
                        'sucesso': False,
                        'mensagem': 'Nenhum anexo encontrado',
                        'arquivos': []
                    }
            
                pasta_pdfs = self.criar_pasta_pdfs()
                resultados = []

                for anexo in anexos:
                    nome_arquivo = anexo['nome'].replace(' ', '_').lower() + '.pdf'
                    caminho_completo = os.path.join(pasta_pdfs, nome_arquivo)

                    baixou = self.downloader.donwload(anexo['url'], caminho_completo)

                    resultados.append({
                        'nome': anexo['nome'],
                        'url': anexo['url'],
                        'caminho': caminho_completo,
                        'sucesso': baixou
                    })

                sucessos = sum(1 for r in resultados if r['sucesso'])

                resultado_zip = None
                if sucessos > 0:
                    print("[CONTROLLER] Compactando arquivos...")
                    resultado_zip = self.zipper_model.criar_zip(pasta_pdfs)
            
                return{
                    'sucesso': True,
                    'mensagem': f'baixados {sucessos} de {len(anexos)} arquivos',
                    'arquivos': resultados,
                    'pasta': pasta_pdfs,
                    'zip': resultado_zip
                }
        
            except Exception as e:
                return {
                    'sucesso': False,
                    'mensagem': f'Erro: {e}',
                    'arquivos': [],
                    'zip': None
    }   
        