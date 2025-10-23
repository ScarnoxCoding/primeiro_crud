import csv
import os
from flask import Flask, render_template, request, redirect, url_for

# Inicializa a aplicação Flask
app = Flask(__name__)

# Define o caminho do nosso arquivo CSV
ARQUIVO_CSV = 'database.csv'

# Função para ler os dados do arquivo CSV
def ler_dados_csv():
    """Lê todos os dados do arquivo CSV e retorna uma lista de dicionários."""
    if not os.path.exists(ARQUIVO_CSV):
        return []
    with open(ARQUIVO_CSV, mode='r', newline='', encoding='utf-8') as arquivo:
        # DictReader trata cada linha como um dicionário
        leitor_csv = csv.DictReader(arquivo)
        return list(leitor_csv)

# Função para escrever dados no arquivo CSV
def escrever_dados_csv(dados):
    """Escreve uma lista de dicionários no arquivo CSV."""
    # 'fieldnames' são os cabeçalhos das colunas
    fieldnames = ['id', 'nome', 'email']
    with open(ARQUIVO_CSV, mode='w', newline='', encoding='utf-8') as arquivo:
        # DictWriter escreve dicionários em linhas de CSV
        escritor_csv = csv.DictWriter(arquivo, fieldnames=fieldnames)
        escritor_csv.writeheader()  # Escreve o cabeçalho
        escritor_csv.writerows(dados) # Escreve todas as linhas de dados

# --- ROTAS DA APLICAÇÃO (CRUD) ---

# Rota para LER (Read) todos os contatos - a página inicial
@app.route('/')
def index():
    """Mostra a lista de contatos."""
    dados = ler_dados_csv()
    return render_template('index.html', dados=dados)

# Rota para CRIAR (Create) um novo contato
@app.route('/adicionar', methods=['GET', 'POST'])
def adicionar():
    """Adiciona um novo contato."""
    if request.method == 'POST':
        # Gera um ID único simples (usando timestamp para simplicidade)
        import time
        novo_id = str(int(time.time()))

        novo_contato = {
            'id': novo_id,
            'nome': request.form['nome'],
            'email': request.form['email']
        }

        dados = ler_dados_csv()
        dados.append(novo_contato)
        escrever_dados_csv(dados)

        # Redireciona de volta para a página inicial
        return redirect(url_for('index'))

    # Se for GET, apenas mostra o formulário de adição
    return render_template('adicionar.html')

# Rota para ATUALIZAR (Update) um contato existente
@app.route('/editar/<id>', methods=['GET', 'POST'])
def editar(id):
    """Edita um contato existente."""
    dados = ler_dados_csv()
    contato_a_editar = None
    for contato in dados:
        if contato['id'] == id:
            contato_a_editar = contato
            break

    if contato_a_editar is None:
        # Contato não encontrado, poderia mostrar uma página de erro
        return "Contato não encontrado!", 404

    if request.method == 'POST':
        # Atualiza os dados do contato no dicionário
        contato_a_editar['nome'] = request.form['nome']
        contato_a_editar['email'] = request.form['email']
        escrever_dados_csv(dados) # Reescreve o arquivo inteiro com os dados atualizados
        return redirect(url_for('index'))

    # Se for GET, mostra o formulário de edição com os dados atuais
    return render_template('editar.html', contato=contato_a_editar)


# Rota para APAGAR (Delete) um contato
@app.route('/apagar/<id>')
def apagar(id):
    """Apaga um contato."""
    dados = ler_dados_csv()
    # Cria uma nova lista sem o contato que queremos apagar
    dados_filtrados = [contato for contato in dados if contato['id'] != id]
    escrever_dados_csv(dados_filtrados)
    return redirect(url_for('index'))


# Roda a aplicação
if __name__ == '__main__':
    app.run(debug=True) # debug=True recarrega o servidor automaticamente após mudanças
