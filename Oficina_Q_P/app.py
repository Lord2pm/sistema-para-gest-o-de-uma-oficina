from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///veiculos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Veiculos(db.Model):
    id = db.Column('id_veiculo', db.Integer, primary_key=True)
    marca = db.Column(db.String(100))
    modelo = db.Column(db.String(100))
    cor = db.Column(db.String(100))
    quilometragem = db.Column(db.Integer)
    nome = db.Column(db.String(100))
    morada = db.Column(db.String(100))
    numero_bi = db.Column(db.String(100))
    numero_tel = db.Column(db.String(100))


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/home')
def home():
    return redirect(url_for('index'))


@app.route('/servicos_agendados')
def servicos_agendados():
    lista_veiculos = Veiculos.query.all()
    return render_template('agendados.html', lista_veiculos=lista_veiculos)


@app.route('/agendar', methods=['GET', 'POST'])
def agendar():
    if request.method == 'POST':
        # Dados da viatura
        marca = request.form.get('marca')
        modelo = request.form.get('modelo')
        cor = request.form.get('cor')
        quilometragem = request.form.get('quilometragem')

        # Dados do condutor
        nome = request.form.get('nome')
        morada = request.form.get('morada')
        numero_bi = request.form.get('numero-bi')
        numero_tel = request.form.get('numero-tel')

        if marca and modelo and cor and quilometragem and nome and morada and numero_bi and numero_tel:
            veiculo = Veiculos(marca=marca, modelo=modelo, cor=cor,
                               quilometragem=int(quilometragem), nome=nome, morada=morada, numero_bi=numero_bi, numero_tel=numero_tel)
            db.session.add(veiculo)
            db.session.commit()
            return redirect(url_for('servicos_agendados'))
        return render_template('cadastrar.html')
    else:
        return render_template('cadastrar.html')


@app.route('/delete/<int:veiculo_id>')
def delete(veiculo_id):
    veiculo = Veiculos.query.filter_by(id=veiculo_id).first()
    db.session.delete(veiculo)
    db.session.commit()
    return redirect(url_for('servicos_agendados'))


if __name__ == '__main__':
    app.run(debug=True)
