import google.generativeai as genai
from google.api_core.exceptions import DeadlineExceeded

# Configure with your API key (de preferência use variáveis de ambiente)
genai.configure(api_key="AIzaSyDGMo4_tD8FyIX-nRGU_INsRBAQMCne9tY")

# List available models
for m in genai.list_models():
    if "generateContent" in m.supported_generation_methods:
        print(m.name)

# Inicializa o modelo
model = genai.GenerativeModel('models/gemini-1.5-flash')

# Tenta gerar conteúdo com tratamento de timeout
try:
    response = model.generate_content("Qual o significado de ser normal?")
    print(response.text)
except DeadlineExceeded:
    print("Erro: A solicitação excedeu o tempo limite. Tente novamente mais tarde.")
except Exception as e:
    print(f"Ocorreu um erro: {e}")


