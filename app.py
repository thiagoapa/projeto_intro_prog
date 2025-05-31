# Importamos la clase Flask del paquete flask
from flask import Flask, render_template

# Creamos una instancia de la aplicación Flask
# El parámetro __name__ indica que este archivo es el punto principal de la app
app = Flask(__name__)

# Definimos una RUTA
# Esto significa: cuando alguien acceda a la URL raíz '/' ejecutará la función 'home'
@app.route('/')
def home():
    # Esta función devuelve una respuesta que el navegador mostrará
    return render_template("index.html")

# Este bloque asegura que el servidor solo se ejecuta si el script se corre directamente
# y no si es importado desde otro archivo
if __name__ == '__main__':
    # Levantamos el servidor Flask en modo debug
    # Esto permite que veamos los errores detalladamente y recargue automáticamente al cambiar código
    app.run(debug=True)
