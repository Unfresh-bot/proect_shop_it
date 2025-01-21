from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database_koments.db'
db = SQLAlchemy(app)


class Course(db.Model):
    __tablename__ = 'courses'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Float, nullable=True)


@app.route('/')
def index():
    courses = Course.query.all()  # Получаем все курсы из базы данных
    return render_template('index.html', courses=courses)


@app.route('/add', methods=['GET', 'POST'])
def add_course():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        rating = request.form['rating']

        new_course = Course(name=name, description=description, rating=float(rating))
        db.session.add(new_course)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('add_course.html')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Создание таблиц
        app.run(debug=True)
