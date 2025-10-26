from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'твой-секретный-ключ'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plans.db'

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    plans = db.relationship('Plan', backref='author', lazy=True)


class Plan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    completed = db.Column(db.Boolean, default=False)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    completed_date = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Это имя уже занято! Выбери другое.', 'error')
            return render_template('register.html')

        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash('Регистрация успешна! Теперь войди в аккаунт.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Успешный вход!', 'success')
            return redirect(url_for('tplans'))
        else:
            flash('Неверное имя или пароль!', 'error')

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Ты вышел из аккаунта.', 'info')
    return redirect(url_for('index'))


@app.route('/lamp')
@login_required
def lamp():
    return render_template('lamp.html')


@app.route('/tplans')
@login_required
def tplans():
    user_plans = Plan.query.filter_by(user_id=current_user.id, completed=False).all()
    return render_template('tplans.html', plans=user_plans)


@app.route('/fplans')
@login_required
def fplans():
    completed_plans = Plan.query.filter_by(user_id=current_user.id, completed=True).all()
    return render_template('fplans.html', plans=completed_plans)


@app.route('/add_plan', methods=['POST'])
@login_required
def add_plan():
    title = request.form['title']
    description = request.form.get('description', '')

    new_plan = Plan(title=title, description=description, user_id=current_user.id)
    db.session.add(new_plan)
    db.session.commit()

    flash('План добавлен!', 'success')
    return redirect(url_for('tplans'))


@app.route('/complete_plan/<int:plan_id>')
@login_required
def complete_plan(plan_id):
    plan = Plan.query.get_or_404(plan_id)

    if plan.user_id != current_user.id:
        flash('Это не твой план!', 'error')
        return redirect(url_for('tplans'))

    plan.completed = True
    plan.completed_date = datetime.utcnow()
    db.session.commit()


    flash('План выполнен! Молодец! 🎉', 'success')
    return redirect(url_for('tplans'))


@app.route('/delete_plan/<int:plan_id>')
@login_required
def delete_plan(plan_id):
    plan = Plan.query.get_or_404(plan_id)

    if plan.user_id != current_user.id:
        flash('Это не твой план!', 'error')
        return redirect(url_for('tplans'))

    db.session.delete(plan)
    db.session.commit()

    flash('План удален!', 'info')
    return redirect(url_for('tplans'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
