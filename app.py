cd ~/Coolkie
cp app.py app.py.bak
cat > app.py << 'EOF'
import os
from flask import Flask, send_from_directory, abort, jsonify
from dotenv import load_dotenv
import pymysql


load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
DB_PORT = int(os.getenv("DB_PORT", 3306))

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__, static_folder=None)


def get_db_connection():
    connection = pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        port=DB_PORT,
        cursorclass=pymysql.cursors.DictCursor
    )
    return connection

PAGES = {"index.html", "cliente.html", "sabores.html"}


@app.route("/")
def home():
    return send_from_directory(BASE_DIR, "index.html")


@app.route("/<path:page>.html")
def pages(page):
    filename = f"{page}.html"
    if filename not in PAGES:
        abort(404)
    return send_from_directory(BASE_DIR, filename)


@app.route("/css/<path:filename>")
def css(filename):
    return send_from_directory(os.path.join(BASE_DIR, "css"), filename)


@app.route("/image/<path:filename>")
def image(filename):
    return send_from_directory(os.path.join(BASE_DIR, "image"), filename)

@app.route("/salvar-cliente", methods=["POST"])
def salvar_cliente():
    # Recolhe os dados enviados pelo formulário HTML (através do atributo 'name' dos inputs)
    nome = request.form.get("nome")
    email = request.form.get("email")

    try:
        # Abre a conexão com o banco RDS na AWS
        conn = get_db_connection()
        with conn.cursor() as cursor:
            # Insere os dados na tabela do banco (certifique-se de que a tabela 'clientes' existe)
            sql = "INSERT INTO clientes (nome, email) VALUES (%s, %s)"
            cursor.execute(sql, (nome, email))
            conn.commit() # Salva as alterações no banco
        conn.close()
        
        return "Informações guardadas com sucesso no banco da AWS! 🎉"
    
    except Exception as e:
        return f"Erro ao salvar no banco: {str(e)}"


@app.route("/health")
def health():
    # Opcional: testando se a API consegue falar com o banco RDS na AWS
    db_status = "connected"
    try:
        conn = get_db_connection()
        conn.close()
    except Exception as e:
        db_status = f"error: {str(e)}"

    return jsonify({"status": "healthy", "database": db_status}), 200


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)