from flask import Flask, render_template, request, redirect, url_for, flash
from gemini import get_gemini_response # Certifique-se que 'gemini.py' está no mesmo diretório ou acessível
import os # Importa o módulo os para verificar a existência do arquivo

app = Flask(__name__)
# Necessário para que as mensagens flash funcionem
# Em um ambiente de produção, esta chave deve ser uma string longa e aleatória
app.secret_key = 'sua_chave_secreta_aqui' # <-- MUDE ISTO PARA UMA CHAVE MAIS SEGURA EM PROD!

# Página inicial
@app.route('/')
def home():
    return render_template("index.html")

# Página da Equipe
@app.route('/equipe')
def equipe():
    return render_template('equipe.html')

# Página de Educação
@app.route('/educational')
def educational():
    return render_template("educational.html")

# Página de Perguntas e Respostas
@app.route('/qa', methods=['GET', 'POST'])
def qa():
    answer = None
    if request.method == 'POST':
        question = request.form['question']
        answer = get_gemini_response(question)
    return render_template("qa.html", answer=answer)

# --- Funções de manipulação do arquivo de texto ---

# Define o nome do arquivo onde os termos do dicionário serão armazenados
ARQUIVO_DICIONARIO = 'termos.txt'

def ler_termos():
    """Lê todos os termos e definições do arquivo e retorna um dicionário."""
    termos = {}
    # Verifica se o arquivo existe antes de tentar lê-lo
    if not os.path.exists(ARQUIVO_DICIONARIO):
        # Se o arquivo não existe, retorna um dicionário vazio
        return termos

    with open(ARQUIVO_DICIONARIO, 'r', encoding='utf-8') as f:
        for linha in f:
            linha = linha.strip() # Remove espaços em branco e quebras de linha
            if "::" in linha: # Garante que a linha contém o separador
                termo, definicao = linha.split('::', 1) # Divide a linha no primeiro "::"
                termos[termo.strip()] = definicao.strip() # Adiciona ao dicionário
    return termos

def adicionar_termo(termo, definicao):
    """Adiciona um novo termo e definição ao arquivo."""
    termos = ler_termos()
    if termo in termos:
        # Se o termo já existe, não adiciona e retorna False
        return False

    with open(ARQUIVO_DICIONARIO, 'a', encoding='utf-8') as f:
        f.write(f"{termo}::{definicao}\n") # Escreve o novo termo no final do arquivo
    return True

def alterar_termo(termo_existente, nova_definicao):
    """Altera a definição de um termo existente."""
    termos = ler_termos()
    if termo_existente not in termos:
        # Se o termo não for encontrado, retorna False
        return False

    termos[termo_existente] = nova_definicao # Atualiza a definição no dicionário
    _salvar_termos_no_arquivo(termos) # Salva o dicionário atualizado no arquivo
    return True

def deletar_termo(termo_a_deletar):
    """Deleta um termo e sua definição do arquivo."""
    termos = ler_termos()
    if termo_a_deletar not in termos:
        # Se o termo não for encontrado, retorna False
        return False

    del termos[termo_a_deletar] # Remove o termo do dicionário
    _salvar_termos_no_arquivo(termos) # Salva o dicionário sem o termo deletado
    return True

def _salvar_termos_no_arquivo(termos):
    """Função interna para sobrescrever o arquivo com todos os termos do dicionário."""
    with open(ARQUIVO_DICIONARIO, 'w', encoding='utf-8') as f:
        for termo, definicao in termos.items():
            f.write(f"{termo}::{definicao}\n")
# --- Fim das funções de manipulação do arquivo ---


# Rota para a página principal do dicionário (dictionary.html) - CORRIGIDA!
@app.route('/dictionary') # Rota para acessar o dicionário
def dictionary(): # Nome do endpoint para usar no url_for()
    termos = ler_termos()
    # Ordena os termos alfabeticamente para uma exibição organizada
    termos_ordenados = sorted(termos.items())
    return render_template('dictionary.html', termos=termos_ordenados)

# Rota para Adicionar Termo (add_term.html)
@app.route('/adicionar', methods=['GET', 'POST'])
def adicionar():
    if request.method == 'POST':
        termo = request.form['termo'].strip()
        definicao = request.form['definicao'].strip()
        if termo and definicao: # Garante que os campos não estão vazios
            if adicionar_termo(termo, definicao):
                flash(f"Termo '{termo}' adicionado com sucesso!", 'success')
                return redirect(url_for('dictionary')) # Redireciona para a página principal do dicionário
            else:
                flash(f"Erro: O termo '{termo}' já existe.", 'danger')
        else:
            flash("Por favor, preencha o termo e a definição.", 'warning')
    return render_template('add_term.html')

# Rota para Alterar Termo (edit_term.html)
@app.route('/alterar', methods=['GET', 'POST'])
def alterar():
    termos_existentes = ler_termos() # Pega os termos existentes para mostrar na lista suspensa
    if request.method == 'POST':
        termo_selecionado = request.form['termo_selecionado'].strip()
        nova_definicao = request.form['nova_definicao'].strip()
        if termo_selecionado and nova_definicao:
            if alterar_termo(termo_selecionado, nova_definicao):
                flash(f"Definição do termo '{termo_selecionado}' alterada com sucesso!", 'success')
                return redirect(url_for('dictionary')) # Redireciona para a página principal do dicionário
            else:
                flash(f"Erro: Termo '{termo_selecionado}' não encontrado.", 'danger')
        else:
            flash("Por favor, selecione um termo e preencha a nova definição.", 'warning')
    return render_template('edit_term.html', termos=termos_existentes)

# Rota para Deletar Termo (delete_term.html)
@app.route('/deletar', methods=['GET', 'POST'])
def deletar():
    termos_existentes = ler_termos() # Pega os termos existentes para mostrar na lista suspensa
    if request.method == 'POST':
        termo_a_deletar = request.form['termo_a_deletar'].strip()
        if termo_a_deletar:
            if deletar_termo(termo_a_deletar):
                flash(f"Termo '{termo_a_deletar}' deletado com sucesso!", 'success')
                return redirect(url_for('dictionary')) # Redireciona para a página principal do dicionário
            else:
                flash(f"Erro: Termo '{termo_a_deletar}' não encontrado.", 'danger')
        else:
            flash("Por favor, selecione um termo para deletar.", 'warning')
    return render_template('delete_term.html', termos=termos_existentes)

if __name__ == '__main__':
    app.run(debug=True)