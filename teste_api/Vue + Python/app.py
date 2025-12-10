from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
from difflib import SequenceMatcher
import unicodedata
import os
import json
import math

app = Flask(__name__)
CORS(app)

def limpar_nan(obj):
    if isinstance(obj, float) and math.isnan(obj):
        return None
    elif isinstance(obj, dict):
        return {k: limpar_nan(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [limpar_nan(item) for item in obj]
    return obj

def normalizar(texto):
    return ''.join(c for c in unicodedata.normalize('NFD', str(texto))
                   if unicodedata.category(c) != 'Mn').lower()

try:
    df_operadoras = pd.read_csv('operadoras.csv', sep=';', encoding='utf-8')
    df_operadoras = df_operadoras.where(pd.notnull(df_operadoras), None)
    print(f"✓ CSV carregado com sucesso! {len(df_operadoras)} registros encontrados")
    print(f"✓ Colunas: {list(df_operadoras.columns)}")
    lista_cadastros = df_operadoras.to_dict(orient='records')
    
    for cadastro in lista_cadastros:
        cadastro['nome_fantasia_normalizado'] = normalizar(cadastro.get('Nome_Fantasia', ''))
    print(f"✓ Dados normalizados com sucesso!")
except FileNotFoundError:
    print("✗ ERRO: Arquivo 'operadoras.csv' não encontrado!")
    print(f"✗ Procurando em: {os.getcwd()}")
    lista_cadastros = []
except Exception as e:
    print(f"✗ ERRO ao carregar CSV: {e}")
    lista_cadastros = []

def similaridade(a, b):
    return SequenceMatcher(None, a, b).ratio()

@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Busca de Operadoras</title>
    <script src="https://unpkg.com/vue@3/dist/vue.global.js"></script>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        #app {
            max-width: 900px;
            margin: 0 auto;
            padding: 40px 20px;
        }
        h1 {
            color: white;
            text-align: center;
            margin-bottom: 30px;
            font-size: 2.5em;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        }
        .search-box {
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            margin-bottom: 30px;
        }
        .search-container {
            display: flex;
            gap: 10px;
        }
        input {
            flex: 1;
            padding: 15px 20px;
            font-size: 16px;
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            outline: none;
            transition: all 0.3s;
        }
        input:focus {
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }
        button {
            padding: 15px 30px;
            font-size: 16px;
            font-weight: 600;
            color: white;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border: none;
            border-radius: 10px;
            cursor: pointer;
            transition: all 0.3s;
        }
        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }
        button:active {
            transform: translateY(0);
        }
        .results {
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            overflow: hidden;
        }
        .result-item {
            padding: 20px;
            border-bottom: 1px solid #f0f0f0;
            transition: background 0.2s;
        }
        .result-item:hover {
            background: #f8f9ff;
        }
        .result-item:last-child {
            border-bottom: none;
        }
        .result-name {
            font-size: 18px;
            font-weight: 600;
            color: #333;
            margin-bottom: 8px;
        }
        .result-info {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 10px;
            margin-top: 10px;
        }
        .result-field {
            font-size: 14px;
            color: #666;
        }
        .result-label {
            font-weight: 600;
            color: #667eea;
        }
        .no-results {
            text-align: center;
            padding: 40px;
            color: #999;
            font-size: 16px;
        }
        .loading {
            text-align: center;
            padding: 40px;
            color: #667eea;
            font-size: 16px;
        }
        .error {
            background: #fee;
            color: #c33;
            padding: 15px;
            border-radius: 10px;
            margin-top: 20px;
        }
    </style>
    </head>
    <body>
    <div id="app">
        <h1>🔍 Busca de Operadoras</h1>
        
        <div class="search-box">
            <div class="search-container">
                <input 
                    v-model="termo" 
                    placeholder="Digite o nome da operadora..." 
                    @keyup.enter="buscar"
                    :disabled="loading"
                >
                <button @click="buscar" :disabled="loading">
                    {{ loading ? 'Buscando...' : 'Buscar' }}
                </button>
            </div>
        </div>

        <div v-if="erro" class="error">
            {{ erro }}
        </div>

        <div v-if="loading" class="results">
            <div class="loading">Carregando resultados...</div>
        </div>

        <div v-else-if="resultados.length > 0" class="results">
            <div v-for="(operadora, index) in resultados" :key="index" class="result-item">
                <div class="result-name">{{ operadora.Nome_Fantasia }}</div>
                <div class="result-info">
                    <div class="result-field" v-if="operadora.Razao_Social">
                        <span class="result-label">Razão Social:</span> {{ operadora.Razao_Social }}
                    </div>
                    <div class="result-field" v-if="operadora.CNPJ">
                        <span class="result-label">CNPJ:</span> {{ operadora.CNPJ }}
                    </div>
                    <div class="result-field" v-if="operadora.Registro_ANS">
                        <span class="result-label">Registro ANS:</span> {{ operadora.Registro_ANS }}
                    </div>
                    <div class="result-field" v-if="operadora.Modalidade">
                        <span class="result-label">Modalidade:</span> {{ operadora.Modalidade }}
                    </div>
                    <div class="result-field" v-if="operadora.UF">
                        <span class="result-label">UF:</span> {{ operadora.UF }}
                    </div>
                    <div class="result-field" v-if="operadora.Municipio">
                        <span class="result-label">Município:</span> {{ operadora.Municipio }}
                    </div>
                </div>
            </div>
        </div>

        <div v-else-if="buscaRealizada" class="results">
            <div class="no-results">Nenhum resultado encontrado para "{{ termo }}"</div>
        </div>
    </div>

    <script>
    const { createApp } = Vue;

    createApp({
        data() {
            return {
                termo: '',
                resultados: [],
                loading: false,
                erro: null,
                buscaRealizada: false
            };
        },
        methods: {
            async buscar() {
                if (!this.termo.trim()) {
                    this.erro = 'Por favor, digite um termo de busca';
                    return;
                }
                
                this.loading = true;
                this.erro = null;
                this.buscaRealizada = false;
                
                try {
                    const res = await fetch(`/buscar?q=${encodeURIComponent(this.termo)}`);
                    
                    if (!res.ok) {
                        throw new Error(`Erro HTTP: ${res.status}`);
                    }
                    
                    const data = await res.json();
                    this.resultados = data;
                    this.buscaRealizada = true;
                } catch (err) {
                    console.error('Erro detalhado:', err);
                    this.erro = `Erro ao buscar operadoras: ${err.message}`;
                    this.resultados = [];
                } finally {
                    this.loading = false;
                }
            }
        }
    }).mount('#app');
    </script>
    </body>
    </html>
    '''

@app.route('/buscar', methods=['GET'])
def buscar_operadoras():
    try:
        termo = request.args.get('q', '')
        if not termo:
            return jsonify({"erro": "Parâmetro 'q' é obrigatório"}), 400

        if not lista_cadastros:
            return jsonify({"erro": "Nenhum dado carregado. Verifique o arquivo CSV."}), 500

        termo_normalizado = normalizar(termo)

        resultados = []
        for cadastro in lista_cadastros:
            score = similaridade(termo_normalizado, cadastro['nome_fantasia_normalizado'])
            if score > 0:
                resultados.append((score, cadastro))

        resultados.sort(reverse=True, key=lambda x: x[0])

        resultados_json = []
        for score, cadastro in resultados[:10]:
            cad_copy = cadastro.copy()
            del cad_copy['nome_fantasia_normalizado']
            # Limpa valores NaN antes de enviar
            cad_limpo = limpar_nan(cad_copy)
            resultados_json.append(cad_limpo)

        return jsonify(resultados_json)
    
    except Exception as e:
        print(f"Erro na rota /buscar: {e}")
        return jsonify({"erro": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)