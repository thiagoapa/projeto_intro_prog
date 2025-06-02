import google.generativeai as genai
from google.api_core.exceptions import DeadlineExceeded

# Configura la API con tu clave
genai.configure(api_key="AIzaSyAGDtq21JCS4kMhw9qmGXSBwIwSF3v854Q")  # Reemplaza YOUR_API_KEY con tu clave real

# Inicializa el modelo
model = genai.GenerativeModel('models/gemini-1.5-flash')

# Función para obtener la respuesta del modelo Gemini
def get_gemini_response(question):
    try:
        response = model.generate_content(question)
        return response.text
    except DeadlineExceeded:
        return "Erro: A solicitação excedeu o tempo limite. Tente novamente mais tarde."
    except Exception as e:
        return f"Ocorreu um erro: {e}"