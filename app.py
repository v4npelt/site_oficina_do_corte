from flask import Flask, render_template, request, url_for, redirect 
from translate import Translator
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class Cad(db.Model):
    #__tablename__ = 'cadastro'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100)) 
    
    def __init__(self, email):
        self.email = email

db.create_all()

@app.route("/")

@app.route("/home")
def home():
    return render_template("index.html")


@app.route("/result", methods = ["POST", "GET"])
def result():
    feedback="E-mail cadastrado com sucesso"
    if request.method == "POST":
        data = request.form['email']
        email = Cad(data)
        print(email)
        db.session.add(email) 
        db.session.commit()
  
    return render_template("index.html", feedback=feedback)

@app.route("/lista", methods = ['GET', 'POST'])
def lista():
    cad = Cad.query.all()
    print(cad) 
    return render_template('lista.html', cad=cad)

@app.route('/delete/<id>/', methods = ["GET", "POST"])
def delete(id):
    data = Cad.query.get(id)
    db.session.delete(data)
    db.session.commit()
    return redirect(url_for('lista'))

@app.route("/sort", methods = ["GET", "POST"])
def sort():
    pass

       
if __name__ == '__main__':
    app.run(debug= True, port=5050)
