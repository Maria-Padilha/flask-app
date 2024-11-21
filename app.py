from flask import Flask, render_template, request, redirect, url_for, send_file
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import os
import io
import openpyxl


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///events.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modelo de Evento
class Evento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    data = db.Column(db.String(50), nullable=False)
    local = db.Column(db.String(200), nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    organizador = db.Column(db.String(100), nullable=False)
    contato = db.Column(db.String(50), nullable=False)
    observacoes = db.Column(db.Text, nullable=True)


# Tela Principal
@app.route('/')
def index():
    return render_template('index.html')


# Tela de Cadastro
@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        evento = Evento(
            nome=request.form['nome'],
            data=request.form['data'],
            local=request.form['local'],
            descricao=request.form['descricao'],
            organizador=request.form['organizador'],
            contato=request.form['contato'],
            observacoes=request.form['observacoes']
        )
        db.session.add(evento)
        db.session.commit()
        return redirect(url_for('exibir'))

    return render_template('cadastro.html')


# tela de exibir todos os eventos
@app.route('/exibir')
def exibir():
    eventos = Evento.query.all()
    return render_template('exibir.html', eventos=eventos)


# Tela de Pesquisa
@app.route('/pesquisa', methods=['GET', 'POST'])
def pesquisa():
    eventos = []
    if request.method == 'POST':
        termo = request.form['termo']
        eventos = Evento.query.filter(Evento.nome.contains(termo)).all()

    return render_template('pesquisa.html', eventos=eventos)


# Tela de Edição
@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    evento = Evento.query.get_or_404(id)

    if request.method == 'POST':
        evento.nome = request.form['nome']
        evento.data = request.form['data']
        evento.local = request.form['local']
        evento.descricao = request.form['descricao']
        evento.organizador = request.form['organizador']
        evento.contato = request.form['contato']
        evento.observacoes = request.form['observacoes']
        db.session.commit()
        return redirect(url_for('exibir'))

    return render_template('editar.html', evento=evento)


# Excluir Evento
@app.route('/deletar/<int:id>')
def deletar(id):
    evento = Evento.query.get_or_404(id)
    db.session.delete(evento)
    db.session.commit()
    return redirect(url_for('exibir'))


# Tela de Upload e Carga de Dados
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file.filename.endswith('.csv'):
            df = pd.read_csv(file)
        elif file.filename.endswith('.json'):
            df = pd.read_json(file)
        elif file.filename.endswith(('.xls', '.xlsx')):
            df = pd.read_excel(file)
        else:
            return render_template('upload.html', mensagem="Formato de arquivo inválido.")

        for _, row in df.iterrows():
            evento = Evento(
                nome=row['nome'],
                data=row['data'],
                local=row['local'],
                descricao=row.get('descricao', ''),
                organizador=row['organizador'],
                contato=row['contato'],
                observacoes=row.get('observacoes', '')
            )
            db.session.add(evento)
        db.session.commit()
        return redirect(url_for('exibir'))

    return render_template('upload.html')


# Tela de Exportação
@app.route('/exportar', methods=['GET'])
def exportar():
    eventos = Evento.query.all()
    data = [{
        'nome': e.nome, 'data': e.data, 'local': e.local, 'descricao': e.descricao,
        'organizador': e.organizador, 'contato': e.contato, 'observacoes': e.observacoes
    } for e in eventos]

    df = pd.DataFrame(data)
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Eventos')

    output.seek(0)
    return send_file(output, download_name='eventos.xlsx', as_attachment=True)


if __name__ == '__main__':
    # Certifique-se de que o banco de dados e as tabelas sejam criados antes de iniciar o servidor
    if not os.path.exists('events.db'):
        with app.app_context():
            db.create_all()

    # Inicia o servidor Flask
    cert_path = 'flask.crt'
    key_path = 'flask.key'

    if os.path.exists(cert_path) and os.path.exists(key_path):
        app.run(host='0.0.0.0', port=443, ssl_context=(cert_path, key_path))
    else:
        print("Certificados SSL não encontrados. Execute com HTTP para testes.")
        app.run(host='0.0.0.0', port=5000, debug=True)
