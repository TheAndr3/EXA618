#!/usr/bin/env python3
import os
import sys
from urllib.parse import parse_qs
from datetime import datetime

FILE_NAME = "posts.txt"

# Lê os dados enviados via formulário
content_length = int(os.environ.get("CONTENT_LENGTH", 0))
if content_length > 0:
    body = sys.stdin.buffer.read(content_length).decode('utf-8')
    params = parse_qs(body)
    
    autor = params.get("autor", ["Anônimo"])[0]
    mensagem = params.get("mensagem", [""])[0]
    data = datetime.now().strftime("%d/%m/%Y %H:%M")

    # Salva no arquivo de texto
    if mensagem:
        with open(FILE_NAME, "a", encoding="utf-8") as f:
            f.write(f"{autor}|{mensagem}|{data}\n")

# Exibe a tela de confirmação após salvar
print("Content-Type: text/html; charset=utf-8")
print()
print("""
<html>
<head>
    <title>Sucesso!</title>
    <style>
        body { font-family: sans-serif; text-align: center; margin-top: 50px; }
        button { padding: 10px 15px; margin: 10px; cursor: pointer; }
    </style>
</head>
<body>
    <h2>Postagem salva com sucesso!</h2>
    <a href="/cgi-bin/list_posts.py"><button>Ver todas as Postagens</button></a>
    <a href="/index.html"><button>Fazer nova postagem</button></a>
</body>
</html>
""")