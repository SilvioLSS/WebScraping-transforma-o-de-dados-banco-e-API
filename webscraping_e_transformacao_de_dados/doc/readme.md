# 🏥 Web Scraping – ANS (Gov.br)

Projeto desenvolvido para teste técnico em vaga de estágio.
O objetivo é acessar a página oficial da ANS no Gov.br, baixar os dois anexos do Rol de Procedimentos, extrair dados do *Anexo I* e gerar:

- ZIP com todos os PDFs baixados  
- CSV processado e limpo  
- ZIP separado contendo somente o CSV  
- Exclusão dos arquivos originais após compactação  

***

## 📌 Tecnologias Utilizadas

- **Python 3.10+**  
- Requests  
- BeautifulSoup4  
- pdfplumber  
- Pandas  
- Zipfile  

***

## 📁 Estrutura do Projeto

```
src/
├── controller/
│   └── scraping_controller.py
├── model/
│   ├── scraper_model.py
│   ├── downloader_model.py
│   ├── pdf_extractor_model.py
│   └── zipper_model.py
├── view/
│   └── console_view.py
└── main.py
statics/
└── resultados/
venv/
```

***

## 🚀 Como Executar

### 1. Instalar dependências

```bash
pip install -r requirements.txt
```

### 2. Rodar o scraper

```bash
python src/main.py
```

### 3. Saída esperada

Após a execução, será criada uma pasta com a data atual:  
`statics/resultados/YYYY-MM-DD/`

Dentro dela estarão:  
- O ZIP dos PDFs  
- O ZIP do CSV processado  

***

📄 **Observações Importantes:**  
O projeto segue uma arquitetura MVC simplificada.  
Código modular, seguindo boas práticas de organização.  
Não depende de versões antigas de Python.  
Fácil de manter, testar e expandir.  

***

👨‍💻 **Autor**  

Silvio Luiz Silva Santos  

***
