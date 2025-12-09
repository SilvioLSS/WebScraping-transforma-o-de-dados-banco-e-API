# models/pdf_extractor_model.py
import pdfplumber
import pandas as pd
import os

class PDFExtractorModel:
    
    def extrair_tabelas_do_pdf(self, caminho_pdf, pagina_inicio=1, pagina_fim=None):
        if not os.path.exists(caminho_pdf):
            raise FileNotFoundError(f"PDF não encontrado: {caminho_pdf}")
        
        print(f"📄 Extraindo tabelas de: {os.path.basename(caminho_pdf)}")
        
        todas_tabelas = []
        
        try:
            with pdfplumber.open(caminho_pdf) as pdf:
                total_paginas = len(pdf.pages)

                if pagina_fim is None or pagina_fim > total_paginas:
                    pagina_fim = total_paginas
                
                print(f"   Páginas a processar: {pagina_inicio} a {pagina_fim} (de {total_paginas})")

                for i in range(pagina_inicio - 1, pagina_fim):
                    pagina = pdf.pages[i]
                    numero_pagina = i + 1
                    tabelas_pagina = pagina.extract_tables()
                    
                    if tabelas_pagina:
                        print(f"   📑 Página {numero_pagina}: {len(tabelas_pagina)} tabela(s)")
                        
                        for j, tabela in enumerate(tabelas_pagina):
                            df = pd.DataFrame(tabela)                            
                            df.attrs['pagina'] = numero_pagina
                            df.attrs['tabela_numero'] = j + 1
                            df.attrs['arquivo'] = os.path.basename(caminho_pdf)
                            
                            todas_tabelas.append(df)
                    else:
                        print(f"   ⚠️  Página {numero_pagina}: Nenhuma tabela encontrada")
            
            print(f"✅ Total de tabelas extraídas: {len(todas_tabelas)}")
            return todas_tabelas
            
        except Exception as e:
            print(f"❌ Erro ao extrair tabelas: {e}")
    
    def identificar_colunas_rol(self, df):
        print("🧹 Limpando e identificando colunas...")

        df_limpo = df.copy()
        df_limpo = df_limpo.dropna(axis=1, how='all')
        df_limpo = df_limpo.dropna(axis=0, how='all')
        primeira_linha = df_limpo.iloc[0] if len(df_limpo) > 0 else pd.Series()

        textos_cabecalho = ['PROCEDIMENTO', 'RN (alteração)', 'VIGÊNCIA', 'SEG. ODONTOLÓGICA', 'SEG. AMBIENTAL', 'HCO', 'HSO', 'REF', 'PAC', 'DUT', 'SUBGRUPO' 'GRUPO', 'CAPÍTULO']
        primeira_linha_str = primeira_linha.astype(str).str.upper().tolist()
        
        if any(any(texto in str(cell) for texto in textos_cabecalho) for cell in primeira_linha_str):
            print("   Usando primeira linha como cabeçalho...")
            df_limpo.columns = df_limpo.iloc[0]
            df_limpo = df_limpo[1:].reset_index(drop=True)

        df_limpo.columns = df_limpo.columns.str.strip()
        
        print(f"   Colunas finais: {list(df_limpo.columns)}")
        return df_limpo
    
    def substituir_siglas(self, df):

        print("🔠 Substituindo siglas...")
        
        df_substituido = df.copy()

        substituicoes = {
            'OD': 'Seg. Odontológica',
            'AMB': 'Seg. Ambulatorial', 
        }

        for col in df_substituido.columns:
            if df_substituido[col].dtype == 'object':
                df_substituido[col] = df_substituido[col].astype(str).str.strip()
                
                for sigla, substituicao in substituicoes.items():
                    df_substituido[col] = df_substituido[col].replace(sigla, substituicao)
        
        return df_substituido
        
    def salvar_para_csv(self, df, caminho_csv):
        try:
            print(f"💾 Salvando CSV: {caminho_csv}")

            BASE_DIR = os.path.dirname(os.path.abspath(__file__))
            caminho_csv = os.path.join(BASE_DIR, "..", "..", caminho_csv)
            caminho_csv = os.path.normpath(caminho_csv)

            pasta = os.path.dirname(caminho_csv)
            if not os.path.exists(pasta):
                os.makedirs(pasta, exist_ok=True)

            df.to_csv(caminho_csv, index=False, encoding='utf-8', sep=';')

            tamanho = os.path.getsize(caminho_csv)

            print("✅ CSV salvo com sucesso")
            print(f"   📊 Linhas: {len(df)}")
            print(f"   📈 Colunas: {len(df.columns)}")
            print(f"   💾 Tamanho: {tamanho} bytes ({tamanho/1024:.1f} KB)")

            return {
                'sucesso': True,
                'caminho': caminho_csv,
                'tamanho_bytes': tamanho,
                'tamanho_kb': round(tamanho / 1024, 1),
                'linhas': len(df),
                'colunas': len(df.columns)
            }

        except Exception as e:
            print(f"❌ Erro ao salvar CSV: {e}")
            return {
                'sucesso': False,
                'erro': str(e)
            }

