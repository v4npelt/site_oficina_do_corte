from flask import Flask, render_template, request, url_for, redirect 
from translate import Translator
from flask_sqlalchemy import SQLAlchemy
import smtplib
from email.message import EmailMessage



app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Cad(db.Model):
    __tablename__ = 'cadastro'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100)) 
    
    def __init__(self, email):
        self.email = email

with app.app_context():
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



@app.route("/send_email", methods = ["GET", "POST"])
def send_email():

    if request.method == 'POST':
        email_client = request.form['email']
        name = request.form['name']
        msg_client = request.form['msg']

        EMAIL_ADRESS = 't35t3con74@gmail.com'
        EMAIL_PASSWORD = '35qu3c1123'

        msg = EmailMessage()
        msg['Subject'] = email_client
        msg['From'] = name
        msg['To'] = EMAIL_ADRESS
        msg.set_content(msg_client)
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)



@app.route('/delete/<id>/', methods = ["GET", "POST"])
def delete(id):  
    data = Cad.query.get(id)
    db.session.delete(data)
    db.session.commit()
    return redirect(url_for('lista'))
       
#if __name__ == '__main__':
    #app.run(debug= True, port=5050)
    #from waitress import serve
    #serve(app, host="0.0.0.0", port="8080")

