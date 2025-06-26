from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    message = db.Column(db.String(10000), nullable=False)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        nachricht = request.form.get('Nachricht')
        if nachricht:
            neue_nachricht = message(name="User", message=nachricht)
            db.session.add(neue_nachricht)
            db.session.commit()
    
    alle_nachrichten = message.query.order_by(message.id).all()
    return render_template('index.html', nachrichten = alle_nachrichten)

@app.route('/clear')
def clear():
    db.session.query(message).delete()
    db.session.commit()
    return 'Alle Nachrichten wurden gelöscht.'

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)