from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///nachrichten.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    message = db.Column(db.String(10000), nullable=False)

with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        nachricht = request.form.get('Nachricht')
        if nachricht:
            # Optional: Nachricht nur speichern, wenn sie nicht schon existiert
            vorhandene = Message.query.filter_by(message=nachricht, name="User").first()
            if not vorhandene:
                neue_nachricht = Message(name="User", message=nachricht)
                db.session.add(neue_nachricht)
                db.session.commit()
        return redirect(url_for('home'))  # <- Korrektes Redirect

    alle_nachrichten = Message.query.order_by(Message.id).all()
    return render_template('index.html', nachrichten=alle_nachrichten)

@app.route('/clear')
def clear():
    db.session.query(Message).delete()
    db.session.commit()
    return 'Alle Nachrichten wurden gelöscht.'

if __name__ == "__main__":
    app.run(debug=True)
