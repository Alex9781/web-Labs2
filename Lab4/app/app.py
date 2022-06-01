from flask import Flask, render_template, session, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, current_user, login_user, logout_user, login_required
from mysql_db import MySQL
import mysql.connector as connector

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.login_message = 'Для доступа к этой странице необходимо пройти процедуру аутентификации'
login_manager.login_message_category = 'warning'

app = Flask(__name__)
application = app

app.config.from_pyfile('config.py')

login_manager.init_app(app)

mysql = MySQL(app)

CREATE_PARAMS = ['login', 'password', 'first_name',
                 'last_name', 'middle_name', 'role_id']

UPDATE_PARAMS = ['first_name', 'last_name', 'middle_name', 'role_id']


def request_params(params_list):
    params = {}

    for param_name in params_list:
        params[param_name] = request.form.get(param_name) or None

    return params


def load_roles():
    with mysql.connection.cursor(named_tuple=True) as cursor:
        cursor.execute('SELECT id, name FROM roles;')
        roles = cursor.fetchall()
    return roles


class User(UserMixin):
    def __init__(self, user_id, login):
        super().__init__()
        self.id = user_id
        self.login = login


@login_manager.user_loader
def load_user(user_id):
    with mysql.connection.cursor(named_tuple=True) as cursor:
        cursor.execute('SELECT * FROM users WHERE id=%s;', (user_id,))
        db_user = cursor.fetchone()
    if db_user:
        return User(user_id=db_user.id, login=db_user.login)
    return None


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login_ = request.form.get('login')
        password_ = request.form.get('password')
        remember_me_ = request.form.get('remember_me') == 'on'

        with mysql.connection.cursor(named_tuple=True) as cursor:
            cursor.execute(
                'SELECT * FROM users WHERE login=%s and password_hash=SHA2(%s, 256);', (login_, password_))
            db_user = cursor.fetchone()

        if db_user:
            login_user(
                User(user_id=db_user.id, login=db_user.login), remember=remember_me_)

            flash('Вы успешно прошли процедуру аутентификации.', 'success')
            next_ = request.args.get('next')
            return redirect(next_ or url_for('index'))

        flash('Введены неверные логин и/или пароль.', 'danger')

    return render_template('login.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/users')
def users():

    with mysql.connection.cursor(named_tuple=True) as cursor:
        cursor.execute(
            'SELECT users.*, roles.name AS role_name FROM users LEFT JOIN roles ON users.role_id = roles.id;'
        )
        users = cursor.fetchall()

    return render_template('users/index.html', users=users)


@app.route('/users/new')
@login_required
def new():
    return render_template('users/new.html', errorCodes={}, user={}, roles=load_roles())


@app.route('/users/create', methods=['POST'])
@login_required
def create():
    params = request_params(CREATE_PARAMS)

    errorCodes = validate_inputs(params)
    if errorCodes['login'] is not None or errorCodes['password'] is not None or errorCodes['first_name'] is not None or errorCodes['last_name'] is not None:
        return render_template('users/new.html', errorCodes=errorCodes, user=params, roles=load_roles())

    params['role_id'] = int(params['role_id']) if params['role_id'] else None
    with mysql.connection.cursor(named_tuple=True) as cursor:
        try:
            cursor.execute(
                ('INSERT INTO users (login, password_hash, last_name, first_name, middle_name, role_id)'
                 'VALUES (%(login)s, SHA2(%(password)s, 256), %(last_name)s, %(first_name)s, %(middle_name)s, %(role_id)s);'),
                params
            )
            mysql.connection.commit()
        except connector.Error:
            flash('Введены некорректные данные. Ошибка сохранения', 'danger')
            return render_template('users/new.html', user=params, roles=load_roles(), errorCodes=errorCodes)
    flash(f"Пользователь {params.get('login')} был успешно создан!", 'success')
    return redirect(url_for('users'))


@app.route('/users/<int:user_id>')
def show(user_id):
    with mysql.connection.cursor(named_tuple=True) as cursor:
        cursor.execute('SELECT * FROM users WHERE id=%s;', (user_id,))
        user = cursor.fetchone()
    return render_template('users/show.html', user=user)


@app.route('/users/<int:user_id>/edit')
@login_required
def edit(user_id):
    with mysql.connection.cursor(named_tuple=True) as cursor:
        cursor.execute('SELECT * FROM users WHERE id=%s;', (user_id,))
        user = cursor.fetchone()
    return render_template('users/edit.html', user=user, errorCodes={}, roles=load_roles())


@app.route('/users/<int:user_id>/update', methods=['POST'])
@login_required
def update(user_id):
    params = request_params(UPDATE_PARAMS)

    params['role_id'] = int(params['role_id']) if params['role_id'] else None
    params['id'] = user_id

    errorCodes = validate_inputs(params)
    if errorCodes['first_name'] is not None or errorCodes['last_name'] is not None:
        return render_template('users/edit.html', errorCodes=errorCodes, user=params, roles=load_roles())

    with mysql.connection.cursor(named_tuple=True) as cursor:
        try:
            cursor.execute(
                ('UPDATE users SET last_name=%(last_name)s, first_name=%(first_name)s, middle_name=%(middle_name)s, role_id=%(role_id)s,'
                 'middle_name=%(middle_name)s, role_id=%(role_id)s WHERE id=%(id)s;'), params)
            mysql.connection.commit()
        except connector.Error:
            flash('Введены некорректные данные. Ошибка сохранения', 'danger')
            return render_template('users/edit.html', user=params, roles=load_roles())
    flash("Пользователь был успешно обновлен!", 'success')
    return redirect(url_for('show', user_id=user_id))


@app.route('/users/<int:user_id>/delete', methods=['POST'])
@login_required
def delete(user_id):
    with mysql.connection.cursor(named_tuple=True) as cursor:
        try:
            cursor.execute(
                ('DELETE FROM users WHERE id=%s'), (user_id, ))
            mysql.connection.commit()
        except connector.Error:
            flash('Не удалось удалить пользователя', 'danger')
            return redirect(url_for('users'))
    flash("Пользователь был успешно удален!", 'success')
    return redirect(url_for('users'))


@app.route('/change', methods=['GET', 'POST'])
@login_required
def change():
    if request.method == 'POST':
        oldPass_ = request.form.get('oldPass')
        newPass_ = request.form.get('newPass')
        newNewPass_ = request.form.get('newNewPass')

        login_ = current_user.login

        with mysql.connection.cursor(named_tuple=True) as cursor:
            cursor.execute(
                'SELECT * FROM users WHERE login=%s and password_hash=SHA2(%s, 256);', (login_, oldPass_))
            db_user = cursor.fetchone()
        
        if db_user:
            if newPass_ != newNewPass_:
                flash('Введённые пароли не совпадают', 'danger')
                return redirect(url_for('change'))

            isPassValid = validate_password(newPass_)
            if isPassValid is not None:
                flash(isPassValid, 'danger')
                return render_template('change.html')
            
            with mysql.connection.cursor(named_tuple=True) as cursor:
                cursor.execute(
                    ("UPDATE users SET password_hash=SHA2(%s, 256) WHERE login=%s;"), (newPass_, login_))
                mysql.connection.commit()
            flash('Пароль успешно изменён', 'success')
            return redirect(url_for('index'))

    return render_template('change.html')


def validate_inputs(params: dict):
    errorCode = {'login': None, 'password': None,
                 'first_name': None, 'last_name': None}

    if params.get('login') is not None and params.get('password') is not None:
        errorCode['login'] = validate_login(params['login'])
        errorCode['password'] = validate_password(params['password'])
    errorCode['first_name'] = validate_first_name(params['first_name'])
    errorCode['last_name'] = validate_last_name(params['last_name'])

    return errorCode


def validate_login(login: str):
    if login is None:
        return "Поле не должно быть пустым"

    allowedChars = "abcdefghijklmnopqrstuvwxyz1234567890"

    if len(login) < 5:
        return "Длинна логина должна быть не менее 5 символов"

    for char in login:
        if allowedChars.find(char) == -1:
            return "Логин должен состоять только из латинских букв и цифр"

    return None


def validate_password(password: str):
    if password is None:
        return "Длинна пароля должна быть в пределах от 8 до 128"

    allowedChars = "abcdefghijklmnopqrstuvwxyz1234567890абвгдеёжзийклмнопрстуфхцчшщъыьэюя~!?@#$%^&*_-+()[]{>}</\|\"\'.,:;"

    if len(password) < 8 or len(password) > 128:
        return "Длинна пароля должна быть в пределах от 8 до 128"

    for char in password:
        if char == " ":
            return "Пароль не может содержать пробелы"
        if allowedChars.find(char.lower()) == -1:
            return "Пароль содержит недопустимые символы"

    hasUpper, hasLover = False, False
    for char in password:
        if char.islower():
            hasLover = True
        if char.isupper():
            hasUpper = True
        if hasUpper and hasLover:
            break
    if not hasUpper or not hasLover:
        return "Пароль должен содержать как минимум одну заглавную и одну строчную букву"

    return None


def validate_first_name(first_name: str):
    if first_name is None:
        return "Поле не должно быть пустым"
    if len(first_name) == 0:
        return "Поле не должно быть пустым"
    return None


def validate_last_name(last_name: str):
    if last_name is None:
        return "Поле не должно быть пустым"
    if len(last_name) == 0:
        return "Поле не должно быть пустым"
    return None
