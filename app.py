from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

# Página de Educação
@app.route('/educational')
def educational():
    return render_template("educational.html")

# Página de Perguntas e Respostas
@app.route('/qa')
def qa():
    return render_template("qa.html")

# Página do Dicionário
@app.route('/dictionary')
def dictionary():
    return render_template("dictionary.html")

if __name__ == '__main__':
    app.run(debug=True)