from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__, template_folder='.', static_folder='.')

# Конфигурация базы данных (SQLite)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///messages.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-secret-key-here'  # Для flash-сообщений

db = SQLAlchemy(app)


# Модель для сообщений
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    subject = db.Column(db.String(200))
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())


# Создаем таблицы при первом запуске
with app.app_context():
    db.create_all()


# Главная страница (index.html)
@app.route('/')
def index():
    return render_template('index.html')


# Страница контактов (item.html)
@app.route('/item.html', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        try:

            new_message = Message(
                name=request.form['name'],
                email=request.form['email'],
                subject=request.form['subject'],
                message=request.form['message']
            )

            db.session.add(new_message)
            db.session.commit()

            flash('Ваше сообщение отправлено! Преподаватель ответит вам в ближайшее время.', 'success')
            return redirect(url_for('contact'))

        except Exception as e:
            db.session.rollback()
            flash('Ошибка при отправке сообщения. Пожалуйста, попробуйте позже.', 'error')

    return render_template('item.html')


if __name__ == '__main__':
    app.run(debug=True)
from flask import abort


# Добавляем в app.py после основного кода
@app.route('/admin/messages')
def view_messages():
    # Простая защита - можно добавить настоящую аутентификацию
    if request.args.get('secret') != 'your-admin-secret':
        abort(403)

    messages = Message.query.order_by(Message.created_at.desc()).all()
    return render_template('messages_list.html', messages=messages)