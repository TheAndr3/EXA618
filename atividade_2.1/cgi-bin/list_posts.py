#!/usr/bin/env python3
import os

FILE_NAME = "posts.txt"

# Cabeçalho OBRIGATÓRIO
print("Content-Type: text/html; charset=utf-8")
print()

# Início do HTML
print("""
<html>
<head>
    <title>Postagens do Blog</title>
    <style>
        body { font-family: sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; }
        .post { border: 1px solid #ccc; padding: 10px; margin-bottom: 10px; border-radius: 5px; }
        .autor { font-weight: bold; color: #2c3e50; }
        .data { font-size: 0.8em; color: #7f8c8d; }
    </style>
</head>
<body>
    <h1>Postagens do Blog</h1>
    <a href="/index.html"><button>Voltar para o Início</button></a>
    <hr>
""")

# Lê o arquivo e imprime as mensagens na tela
if os.path.exists(FILE_NAME):
    with open(FILE_NAME, "r", encoding="utf-8") as f:
        posts = f.readlines()
    
    posts.reverse() # Mais recentes primeiro

    for post in posts:
        parts = post.strip().split("|")
        if len(parts) == 3:
            autor, msg, data = parts
            print(f"""
            <div class="post">
                <span class="autor">{autor}</span> em <span class="data">{data}</span>
                <p>{msg}</p>
            </div>
            """)
else:
    print("<p>Nenhuma postagem ainda.</p>")

print("</body></html>")