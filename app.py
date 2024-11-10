from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import openai


app = Flask(__name__)
CORS(app)
genai.configure(api_key='AIzaSyDgaiDqmjd4aScETKWkChUjz8XsL7AlFKU')

cadastros = []

def responder_pergunta_de_idioma(pergunta):
    try:
        model = genai.GenerativeModel('gemini-1.0-pro')
        prompt = f"Uma criança perguntou: '{pergunta}'. Como eu posso responder a essa pergunta de forma simples e divertida para ajudar no aprendizado de idiomas com apenas uma respota?"

        response = model.generate_content(prompt)
        print(f"Resposta completa da API: {response}")

        if response and hasattr(response, 'candidates') and len(response.candidates) > 0:
            content = response.candidates[0].content
            resposta = content.parts[0].text if content.parts else "Não encontrei uma resposta para essa pergunta."

            resposta_formatada = (f"<strong>Resposta:</strong> {resposta}<br>"
                                  "Lembre-se de praticar e se divertir enquanto aprende!")
        else:
            resposta_formatada = "Não encontrei uma resposta para essa pergunta."

        return resposta_formatada
    except Exception as e:
        return f"Erro ao buscar a resposta: {str(e)}"

# Rota de cadastro
@app.route('/cadastro', methods=['POST'])
def cadastro():
    data = request.get_json()
    nome = data.get('nome')
    email = data.get('email')
    senha = data.get('senha')

    # Verificar se todos os dados foram enviados
    if not nome or not email or not senha:
        return jsonify({"error": "Todos os campos são obrigatórios"}), 400

    # Adicionar o cadastro à lista
    cadastros.append({
        "nome": nome,
        "email": email,
        "senha": senha
    })
    return jsonify({"message": "Cadastro realizado com sucesso!"}), 201

# Rota de login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    senha = data.get('senha')

    # Verificar se o email e senha estão corretos
    for cadastro in cadastros:
        if cadastro["email"] == email and cadastro["senha"] == senha:
            return jsonify({"message": "Login realizado com sucesso!"}), 200

    return jsonify({"error": "Email ou senha incorretos"}), 401

@app.route('/chat', methods=['POST'])
def api_chat():
    data = request.get_json()

    if 'pergunta' not in data:
        return jsonify({"erro": "Campo 'pergunta' não encontrado na requisição."}), 400

    pergunta = data['pergunta']

    if len(pergunta) < 3:
        return jsonify({"erro": "Por favor, faça uma pergunta mais específica."}), 400

    resposta = responder_pergunta_de_idioma(pergunta)

    return jsonify({"resposta": resposta})


if __name__ == '__main__':
    app.run(debug=True)
