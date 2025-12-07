import os 
from datetime import datetime 
import pandas as pd

class ScrapingController:
        def __init__(self):
            from model.scraper_model import ScraperModel
            from model.downloader_model import DonwloaderModel
            from model.zipper_model import ZipperModel
            from model.pdf_extractor_model import PDFExtractorModel 

            self.scraper = ScraperModel()
            self.downloader = DonwloaderModel()
            self.zipper_model = ZipperModel() 
            self.pdf_extractor = PDFExtractorModel()

        def processar_anexo_i(self, caminho_pdf):

            try:
                print(f"🔍 Processando: {os.path.basename(caminho_pdf)}")
                
                tabelas = self.pdf_extractor.extrair_tabelas_do_pdf(caminho_pdf)
                if not tabelas:
                    return {'sucesso': False, 'erro': 'Nenhuma tabela encontrada'}
                
                df_combinado = pd.concat(tabelas, ignore_index=True)
                
                df_limpo = self.pdf_extractor.identificar_colunas_rol(df_combinado)
                
                df_final = self.pdf_extractor.substituir_siglas(df_limpo)
                
                pasta = os.path.dirname(caminho_pdf)
                caminho_csv = os.path.join(pasta, "rol_procedimentos.csv")
                
                resultado_csv = self.pdf_extractor.salvar_para_csv(df_final, caminho_csv)
                if not resultado_csv['sucesso']:
                    return resultado_csv
                
                resultado_zip_csv = self.zipper_model.criar_zip_arquivo_unico(
                    caminho_csv, 
                    "rol_procedimentos.zip"
                )
                
                return {
                    'sucesso': True,
                    'mensagem': 'Anexo I processado com sucesso',
                    'tabela': {
                        'linhas': len(df_final),
                        'colunas': len(df_final.columns)
                    },
                    'csv': resultado_csv,
                    'zip_csv': resultado_zip_csv
                }
                
            except Exception as e:
                return {'sucesso': False, 'erro': str(e)}

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
                caminho_anexo_i = None

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

                    if anexo['nome'] == 'Anexo I' and baixou:
                        caminho_anexo_i = caminho_completo

                anexoI_processado = None
                if caminho_anexo_i and os.path.exists(caminho_anexo_i):
                    print("\n🔍 PROCESSANDO ANEXO I...")
                    anexoI_processado = self.processar_anexo_i(caminho_anexo_i)        

                sucessos = sum(1 for r in resultados if r['sucesso'])

                resultado_zip = None
                if sucessos > 0:
                    print("[CONTROLLER] Compactando arquivos...")
                    resultado_zip = self.zipper_model.criar_zip(pasta_pdfs)

                if resultado_zip and resultado_zip['sucesso']:
                    for arquivo in resultados:
                        if arquivo['sucesso']:
                            try:
                                os.remove(arquivo['caminho'])
                                print(f"🗑️  Excluído: {arquivo['nome']}")
                            except Exception as e:
                                print(f"⚠️  Não pude excluir {arquivo['nome']}: {e}") 
            
                return{
                    'sucesso': True,
                    'mensagem': f'baixados {sucessos} de {len(anexos)} arquivos',
                    'processamento_anexo_i': anexoI_processado,
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
        