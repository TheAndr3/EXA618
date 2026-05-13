from flask import Flask, request, redirect, url_for, render_template, session, make_response

app = Flask(__name__)
app.secret_key = 'eita'


@app.route("/nome/<nome>")
def salvar_nome(nome):
    session['nome'] = nome
    resposta = make_response(redirect(url_for('home')))
    resposta.set_cookie('nome', nome)
    return resposta

@app.route("/")
def home():
    nome = session.get('nome') or request.cookies.get('nome')
    visitas = int(request.cookies.get('visitas', 0)) + 1
    
    if nome:
        saudacao = f"{nome}"
    else:
        saudacao = "VISITANTE"
    resposta = make_response(render_template('index.html', saudacao=saudacao, visitas=visitas))
    resposta.set_cookie('visitas', str(visitas))
    return resposta

@app.route("/login", methods=['POST'])
def login_post():
    usuario = request.form.get('usuario')
    senha = request.form.get('senha')

    if usuario == 'admin' and senha == '123':
        session['usuario'] = usuario
        return redirect(url_for('perfil'))
    return render_template('login.html', erro = 'Usuário ou senha incorretos')
    
@app.route("/login", methods=['GET'])
def login_get():
    return render_template('login.html')

@app.route("/perfil")
def perfil():
    if 'usuario' in session:
        usuario = session['usuario']
        nome = session.get('nome') or request.cookies.get('nome', 'VISITANTE')
        return render_template('perfil.html', usuario=usuario, nome=nome)
    return redirect(url_for('login_get'))

@app.route("/logout") 
def logout():
    session.pop('usuario', None)
    session.pop('nome', None)
    return redirect(url_for('login_get'))


if __name__ == '__main__':
    app.run(debug=True)

