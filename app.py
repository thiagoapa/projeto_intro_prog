from flask import Flask, render_template, request, redirect, url_for
from gemini import get_gemini_response

app = Flask(__name__)

# Página inicial
@app.route('/')
def home():
    return render_template("index.html")

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

# Página principal do dicionário
@app.route('/dictionary')
def dictionary():
    return render_template("dictionary.html", terms=terms)

# Adicionar termo
@app.route('/add', methods=['GET', 'POST'])
def add_term():
    if request.method == 'POST':
        term = request.form['term']
        definition = request.form['definition']
        terms[term] = definition
        return redirect(url_for('dictionary'))
    return render_template("add_term.html")

# Editar termo
@app.route('/edit/<term>', methods=['GET', 'POST'])
def edit_term(term):
    if request.method == 'POST':
        new_term = request.form['term']
        definition = request.form['definition']
        # Remover termo antigo se foi renomeado
        if new_term != term:
            del terms[term]
        terms[new_term] = definition
        return redirect(url_for('dictionary'))
    return render_template("edit_term.html", term=term, definition=terms[term])

# Deletar termo
@app.route('/delete/<term>', methods=['POST'])
def delete_term(term):
    terms.pop(term, None)
    return redirect(url_for('dictionary'))

if __name__ == '__main__':
    app.run(debug=True)