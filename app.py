from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database_koments.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Определение модели Course




class Course(db.Model):
    __tablename__ = 'courses'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)

class Review(db.Model):
    __tablename__ = 'reviews'  # Имя таблицы в базе данных
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    review = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)

@app.route('/')
def index():
    courses = Course.query.all()
    return render_template('index.html', courses=courses)

@app.route('/course/<int:course_id>', methods=['GET', 'POST'])
def course_detail(course_id):
    course = Course.query.get_or_404(course_id)
    if request.method == 'POST':
        review_text = request.form['review']
        rating = request.form['rating']
        new_review = Review(course_id=course.id, review=review_text, rating=int(rating))
        db.session.add(new_review)
        db.session.commit()
        return redirect(url_for('course_detail', course_id=course.id))
    return render_template('course_detail.html', course=course)

@app.route('/add_course', methods=['GET', 'POST'])
def add_course():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        new_course = Course(name=name, description=description)
        db.session.add(new_course)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_course.html')

if __name__ == '__main__':
    with app.app_context():
        try:
            db.create_all()
            print("Таблицы успешно созданы.")
        except Exception as e:
            print(f"Ошибка при создании таблиц: {e}")
        # Проверка, существуют ли уже курсы, чтобы избежать дублирования
        if Course.query.count() == 0:
            # Добавление нескольких курсов
            course1 = Course(name='Python для начинающих', description='Изучите основы программирования на Python.')
            course2 = Course(name='Веб-разработка с Flask', description='Создание веб-приложений с использованием Flask.')
            course3 = Course(name='Анализ данных с Pandas', description='Научитесь анализировать данные с помощью библиотеки Pandas.')

            db.session.add(course1)
            db.session.add(course2)
            db.session.add(course3)
            db.session.commit()

    app.run(debug=True)
