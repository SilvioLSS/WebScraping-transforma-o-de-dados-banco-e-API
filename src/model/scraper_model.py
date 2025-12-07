import requests
from bs4 import BeautifulSoup

class ScraperModel:
    def __init__(self):
        self.url = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos"

    def buscar_anexos(self):

        anexos_encontrados = []

        pagina_gov = requests.get(self.url, timeout=10)
        pagina_gov.raise_for_status()

        html_pagina_gov = BeautifulSoup(pagina_gov.text, 'html.parser')

        links_pagina_gov = html_pagina_gov.find_all('a')

        for a in links_pagina_gov:
            texto = a.get_text(strip=True)
            href = a.get('href', '')

            if 'Anexo II' in texto and href.lower().endswith('.pdf'):
                anexos_encontrados.append({
                    'nome': 'Anexo II',
                    'url': href
                })

            if 'Anexo I' in texto and not 'Anexo II' in texto and href.lower().endswith('.pdf'):
                anexos_encontrados.append({
                    'nome': 'Anexo I',
                    'url': href
                })

        return anexos_encontrados
            

        