import os
from flask import Flask, jsonify

app = Flask(__name__)

# Configurações do app vindas de variáveis de ambiente (prática recomendada de segurança da AWS)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'chave-secreta-padrao-desenvolvimento')
app.config['ENV'] = os.getenv('FLASK_ENV', 'production')


@app.route('/')
def home():
    """Rota principal de teste da aplicação."""
    return jsonify({
        "message": "Aplicação Flask rodando com sucesso na AWS!",
        "status": "online"
    }), 200


@app.route('/health')
def health_check():
    """
    Endpoint de Health Check para Application Load Balancers (ALB) da AWS,
    Elastic Beanstalk, App Runner ou ECS monitoring.
    """
    return jsonify({"status": "healthy"}), 200


if __name__ == '__main__':
    # Obtém a porta injetada pela AWS (Elastic Beanstalk/App Runner) ou usa 8080/5000 por padrão
    port = int(os.getenv('PORT', 5000))
    # Em produção na AWS, nunca use debug=True e configure host='0.0.0.0'
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() in ['true', '1']
    
    app.run(host='0.0.0.0', port=port, debug=debug_mode)
