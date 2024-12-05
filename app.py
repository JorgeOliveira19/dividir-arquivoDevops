import os
from flask import Flask, request, render_template, send_from_directory, jsonify
import pandas as pd

app = Flask(__name__)

# Caminho do arquivo para armazenar o contador
contador_arquivo = 'contador.txt'

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')


# Função para ler o contador do arquivo
def ler_contador():
    if not os.path.exists(contador_arquivo):
        return 0  # Inicia o contador em 0 se o arquivo não existir
    with open(contador_arquivo, 'r') as f:
        return int(f.read())

# Função para escrever o contador no arquivo
def atualizar_contador(valor):
    with open(contador_arquivo, 'w') as f:
        f.write(str(valor))

# Carrega o contador do arquivo ao iniciar a aplicação
contador_uso = ler_contador()

## ---------------------------------------------------------------------------

# Caminho do arquivo para armazenar o contador
contador_arquivo2 = 'qtdArquivosGerados.txt'

# Função para ler o contador do arquivo
def ler_contador2():
    if not os.path.exists(contador_arquivo2):
        return 0  # Inicia o contador em 0 se o arquivo não existir
    with open(contador_arquivo2, 'r') as f:
        return int(f.read())

# Função para escrever o contador no arquivo
def atualizar_contador2(valor):
    with open(contador_arquivo2, 'w') as f:
        f.write(str(valor))

# Carrega o contador do arquivo ao iniciar a aplicação
contador_uso2 = ler_contador2()
## ---------------------------------------------------------------------------

# Pasta onde os arquivos CSV divididos serão armazenados
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Função para dividir o CSV
def dividir_csv(input_file, tamanho_lote):
    try:
        # Lê o arquivo CSV
        df = pd.read_csv(input_file, delimiter=';')
        num_partes = len(df) // tamanho_lote + (1 if len(df) % tamanho_lote != 0 else 0)

        arquivos_gerados = []

        # Dividir o arquivo CSV em partes
        for i in range(num_partes):
            inicio = i * tamanho_lote
            fim = min((i + 1) * tamanho_lote, len(df))
            df_part = df.iloc[inicio:fim].reset_index(drop=True)
            output_file = os.path.join(app.config['UPLOAD_FOLDER'], f'Arquivo: {i + 1}.csv')
            df_part.to_csv(output_file, sep=';', index=False)
            arquivos_gerados.append(f'Arquivo: {i + 1}.csv')

        return arquivos_gerados
    except Exception as e:
        print(f"Erro ao dividir o CSV: {e}")
        raise

# Rota para o favicon
@app.route('/favicon.ico')
def favicon():
    return send_from_directory('static', 'favicon.ico')

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Obtém o arquivo CSV
        file = request.files['file']
        if file.filename == '':
            return 'Nenhum arquivo foi enviado.', 400

        # Salva o arquivo CSV na pasta 'uploads'
        input_file = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(input_file)
        print(f"Arquivo salvo como: {input_file}")

        # Obtém o tamanho do lote
        tamanho_lote = int(request.form['tamanho_lote'])

        # Chama a função para dividir o CSV
        arquivos_gerados = dividir_csv(input_file, tamanho_lote)

        # Gera links para download dos arquivos gerados
        links_download = [f"/download/{arquivo}" for arquivo in arquivos_gerados]

        global contador_uso
    if request.method == 'POST':
        # Incrementa o contador e atualiza o arquivo
        contador_uso += 1
        atualizar_contador(contador_uso)

        global contador_uso2
    if request.method == 'POST':
        # Incrementa o contador e atualiza o arquivo
        contador_uso2 += 1
        atualizar_contador2(contador_uso2)

        # Outras operações, como manipulação do arquivo CSV...

        # Retorna os links para download
        return jsonify(links_download)

    return render_template('index.html', contador=contador_uso, contador2=contador_uso2)



@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    # Certifica-se de que a pasta 'uploads' é criada ao iniciar a aplicação
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
        print(f"Pasta '{app.config['UPLOAD_FOLDER']}' criada.")
    app.run(debug=True)
