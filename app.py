from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import requests


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://tkueqtax:2aRKblL6iOnx6h_QDXLdoEPmp0BskzxQ@heffalump.db.elephantsql.com/tkueqtax'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

my_dict = {
    'question1': { 'block': 1, 'negative': False, 'priority': 1.0 },
    'question2': { 'block': 1, 'negative': False, 'priority': 0.7 },
    'question3': { 'block': 1, 'negative': False, 'priority': 0.9 },
    'question4': { 'block': 1, 'negative': False, 'priority': 0.5 },
    'question5': { 'block': 1, 'negative': True, 'priority': 0.3 },
    'question6': { 'block': 2, 'negative': True, 'priority': 0.5 },
    'question7': { 'block': 2, 'negative': True, 'priority': 0.5 },
    'question8': { 'block': 2, 'negative': True, 'priority': 0.7 },
    'question9': { 'block': 2, 'negative': True, 'priority': 0.8 },
    'question10': { 'block': 2, 'negative': True, 'priority': 0.3 },
    'question11': { 'block': 3, 'negative': False, 'priority': 0.9 },
    'question12': { 'block': 3, 'negative': False, 'priority': 0.7 },
    'question13': { 'block': 3, 'negative': False, 'priority': 0.8 },
    'question14': { 'block': 3, 'negative': False, 'priority': 0.4 },
    'question15': { 'block': 3, 'negative': False, 'priority': 1.0 },
    'question16': { 'block': 4, 'negative': False, 'priority': 1.0 },
    'question17': { 'block': 4, 'negative': False, 'priority': 0.3 },
    'question18': { 'block': 4, 'negative': False, 'priority': 0.5 },
    'question19': { 'block': 4, 'negative': False, 'priority': 0.5 },
    'question20': { 'block': 4, 'negative': False, 'priority': 1.0 },
    'question21': { 'block': 5, 'negative': False, 'priority': 0.4 },
    'question22': { 'block': 5, 'negative': False, 'priority': 0.7 },
    'question23': { 'block': 5, 'negative': True, 'priority': 0.7 },
    'question24': { 'block': 5, 'negative': False, 'priority': 0.9 },
    'question25': { 'block': 5, 'negative': True, 'priority': 0.6 }
}


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    surname = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    sex = db.Column(db.String(100), nullable=False)
    average_rate = db.Column(db.Float, nullable=True)
    expert_review = db.Column(db.Text, nullable=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)


def __repr__(self):
    return '<Question %r>' % self.id


@app.route('/', methods=['POST', 'GET'])
def index():
    city_request = requests.get('https://api.hh.ru/areas').json()
    cities = []
    for region_data in city_request[0]['areas']:
        if len(region_data['areas']) == 0:
            cities.append(region_data['name'])
        else:
            for city_data in region_data['areas']:
                cities.append(city_data['name'])
    if request.method == "POST":
        name = request.form['name']
        surname = request.form['surname']
        city = request.form['city']
        sex = request.form['sex']
        if not name or not surname or not city or not sex:
            return render_template("index.html", error="Пожалуйста, заполните все поля")
        if city not in cities:
            return render_template("index.html", error="Пожалуйста, введите существующий город")
        question = Question(name=name, surname=surname, city=city, sex=sex)

        try:
            db.session.add(question)
            db.session.commit()
            return redirect(url_for('.quiz', id=question.id))

        except:
            return "Ошибка"

    else:
        return render_template("index.html")


@app.route('/result')
def result():
    return render_template("result.html")


@app.route('/about')
def about():
    return render_template("about.html")


def calculate_result(recieved_dict):
    total_score = 0
    for question_key, answer in recieved_dict.items():
        question_data = my_dict[question_key]
        if question_data['negative']:
            value = 6 - int(answer)
        else:
            value = int(answer)
        total_score += value * question_data['priority']
    return round(total_score, 2)


@app.route('/quiz', methods=['POST', 'GET'])
def quiz():
    user_id = request.args['id']
    if request.method == "POST":
        request_dict = dict(request.form)
        result = calculate_result(request_dict)
        expert_review = ""
        current_user = Question.query.get(user_id)
        if 0 < result <= 30:
            expert_review = f'Уважаемый {current_user.name}, к сожалению, вы не подходите на направление "Бизнес-информатика" '
        elif 30 < result <= 50:
            expert_review = f'Уважаемый {current_user.name}, вы молодец! У вас имеется предрасположенность к данному направлению, но советуем еще подумать над выбором'
        elif 50 < result:
            expert_review = f'Уважаемый {current_user.name}, вы молодец! Вы полностью подходите нам! '
        try:
            current_user.average_rate = result
            current_user.expert_review = expert_review
            db.session.commit()
            return render_template("result.html", result=result, expert_review=expert_review)
        except:
            return "Ошибка"
    return render_template("question.html")


if __name__ == "__main__":
    app.run(debug=True)