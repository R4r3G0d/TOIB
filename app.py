from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class Counter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    count = db.Column(db.Integer, nullable=False, default=0)

def create_tables():
    with app.app_context():
        db.create_all()

@app.route('/increment', methods=['POST'])
def increment():
    with app.app_context():
        counter = Counter.query.first()
        if not counter:
            counter = Counter(count=1)
            db.session.add(counter)
        else:
            counter.count += 1  
        db.session.commit()
    return 'Counter incremented', 200

@app.route('/')
def index():
    with app.app_context():
        counter = Counter.query.first()
        if counter:
            counter_value = counter.count
        else:
            counter_value = 0
    return render_template('index.html', counter=counter_value)

if __name__ == '__main__':
    create_tables()  
    app.run(debug=True)
# from flask import Flask, request
# from flask_sqlalchemy import SQLAlchemy
# import threading

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
# db = SQLAlchemy(app)

# # Мьютекс для синхронизации доступа к счетчику
# counter_lock = threading.Lock()

# class Counter(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     count = db.Column(db.Integer, nullable=False, default=0)

# # Функция для создания таблиц в базе данных
# def create_tables():
#     with app.app_context():
#         db.create_all()

# # Регистрируем функцию create_tables как обработчик для события before_first_request
# # app._got_first_request(create_tables)

# @app.route('/increment', methods=['POST'])
# def increment():
#     with counter_lock:
#         counter = Counter.query.first()
#         if not counter:
#             counter = Counter(count=1)
#             db.session.add(counter)
#         else:
#             counter.count += 1
#         db.session.commit()
#     return 'Counter incremented', 200

# @app.route('/')
# def index():
#     counter = Counter.query.first()
#     return f'Counter: {counter.count if counter else 0}'

# if __name__ == '__main__':
#     create_tables()
#     app.run(debug=True)