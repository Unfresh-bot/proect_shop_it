from models import Course, Review, db
from flask import Flask, render_template, request, redirect, url_for
from __init__ import app
@app.route('/')
def index():
    courses = Course.query.all()
    return render_template('index.html', courses=courses)

@app.route('/add', methods=['GET', 'POST'])
def add_course():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        new_course = Course(name=name, description=description)
        db.session.add(new_course)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_course.html')

@app.route('/course/<int:course_id>', methods=['GET'])
def course_detail(course_id):
    course = Course.query.get_or_404(course_id)
    return render_template('course_detail.html', course=course)

@app.route('/course/<int:course_id>/review', methods=['GET', 'POST'])
def review_course(course_id):
    course = Course.query.get_or_404(course_id)
    if request.method == 'POST':
        content = request.form['content']
        rating = request.form['rating']  # Получаем оценку из формы
        new_review = Review(content=content, rating=rating, course_id=course.id)
        db.session.add(new_review)
        db.session.commit()
        return redirect(url_for('course_detail', course_id=course.id))
    return render_template('review_course.html', course=course)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Создаем таблицы базы данных
    app.run(debug=True)