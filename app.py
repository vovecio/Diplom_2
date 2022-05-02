from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123@localhost/diplom'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    surname = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    gpa = db.Column(db.Integer, nullable=False)
    sex = db.Column(db.String(100), nullable=False)
    expert_review = db.Column(db.String(200), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Question %r>' % self.id


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == "POST":
        name = request.form['name']
        surname = request.form['surname']
        city = request.form['city']
        sex = request.form['sex']

        question = Question(name=name, surname=surname, city=city, sex=sex)

        try:
            db.session.add(question)
            db.session.commit()
            return redirect('/about')

        except:
            return "Ошибка"

    else:
        return render_template("index.html")


@app.route('/about')
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True)

