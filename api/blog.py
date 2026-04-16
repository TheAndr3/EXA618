import os
import json
from datetime import datetime
from http.server import BaseHTTPRequestHandler
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

# Conexão com o Cluster do MongoDB
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client['blog_db']
collection = db['messages']

class handler(BaseHTTPRequestHandler):

    # Método para Listar as Mensagens (GET)
    def do_GET(self):
        try:
            # Busca todas as mensagens, tirando o ID interno do Mongo e ordenando pela data
            posts = list(collection.find({}, {"_id": 0}).sort("date", -1))
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json; charset=utf-8')
            self.end_headers()
            self.wfile.write(json.dumps(posts).encode('utf-8'))
        except Exception as e:
            self.send_error(500, f"Erro no banco: {str(e)}")

    # Método para Salvar Mensagem (POST/PUT)
    def do_POST(self):
        try:
            # Lê o corpo da requisição
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)

            # Verifica se a action é 'put' conforme o requisito
            if data.get("action") == "put":
                new_post = {
                    "author": data.get("author", "Anônimo"),
                    "message": data.get("message", ""),
                    "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                
                # Insere no MongoDB Atlas
                collection.insert_one(new_post)
                
                self.send_response(201)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = {"status": "success", "message": "put executed successfully"}
                self.wfile.write(json.dumps(response).encode())
            else:
                self.send_error(400, "Action incorreta. Use 'put'.")

        except Exception as e:
            self.send_error(500, f"Erro ao processar: {str(e)}")