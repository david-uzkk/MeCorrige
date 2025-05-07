from flask import Flask, render_template, request
from openai import OpenAI
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Configurar a API OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Inicializar a aplicação Flask
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/aprimorar', methods=['POST'])
def aprimorar_mensagem():
    # Obter dados do formulário
    mensagem_original = request.form['mensagem']
    contexto = request.form.get('contexto', 'Automático')
    tom = request.form.get('tom', 'Automático')
    
    try:
        # Criar prompt para a API da OpenAI
        if contexto == "Automático" and tom == "Automático":
            prompt = f"""
            Por favor, apimore a seguinte mensagem para torná-la mais profissional,
            clara e adequada. Corrija erros gramaticais, melhore a estrutura e o tom.
            
            Mensagem original: "{mensagem_original}"
            """
        else:
            prompt = f"""
            Por favor, apimore a seguinte mensagem para um contexto profissional.
            
            Mensagem original: "{mensagem_original}"
            
            Contexto da mensagem: {contexto}
            
            Tom desejado: {tom}
            
            Forneça uma versão aprimorada que seja clara, profissional e adequada ao contexto.
            Corrija erros gramaticais, melhore a estrutura e o tom.
            """
        
        # Fazer chamada para a API da OpenAI
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Você é um especialista em comunicação profissional. Sua tarefa é melhorar mensagens para torná-las mais claras, profissionais e adequadas ao contexto, corrigindo gramática e ajustando o tom conforme necessário."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=800
        )
        
        # Extrair a resposta gerada
        mensagem_aprimorada = response.choices[0].message.content
        
        return render_template('result.html', 
                              mensagem_original=mensagem_original,
                              mensagem_aprimorada=mensagem_aprimorada,
                              contexto=contexto,
                              tom=tom)
    
    except Exception as e:
        return render_template('result.html', 
                              mensagem_original=mensagem_original,
                              mensagem_aprimorada=f"Erro ao processar a solicitação: {str(e)}",
                              contexto=contexto,
                              tom=tom)

if __name__ == '__main__':
    app.run(debug=True)