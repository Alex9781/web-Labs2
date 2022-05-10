from flask import Blueprint, Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user
from app import mysql, app
from users_policy import UsersPolicy
import functools

bp = Blueprint('auth', __name__, url_prefix='/auth')

class User(UserMixin):
    def __init__(self, user_id, login, role_id):
        super().__init__()
        self.id = user_id
        self.login = login
        self.role_id = role_id

    @property
    def is_admin(self):
        return app.config.get('ADMIN_ROLE_ID') == self.role_id

    def can(self, action, record = None):
        user_policy = UsersPolicy(record=record)
        method = getattr(user_policy, action, None)
        if method is not None: return method()
        else: return False


def check_rights(action):
    def decorator(function):
        @functools.wraps(function)
        def wrapper(*args, **kwargs):
            user = load_user(kwargs.get('user_id'))
            if not current_user.can(action, record=user):
                flash('У вас недостаточно прав для доступа к данной странице.', 'danger')
                return redirect(url_for('index'))
            return function(*args, **kwargs)
        return wrapper
    return decorator


def load_user(user_id):
    #if user_id is None: return None
    with mysql.connection.cursor(named_tuple=True) as cursor:
        cursor.execute('SELECT * FROM users WHERE id=%s;', (user_id,))
        db_user = cursor.fetchone()
    if db_user:
        return User(user_id=db_user.id, login=db_user.login, role_id=db_user.role_id)
    return None


@bp.route('/login', methods=['GET', 'POST'])
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
                User(user_id=db_user.id, login=db_user.login, role_id=db_user.role_id), remember=remember_me_)

            flash('Вы успешно прошли процедуру аутентификации.', 'success')
            next_ = request.args.get('next')
            return redirect(next_ or url_for('index'))

        flash('Введены неверные логин и/или пароль.', 'danger')

    return render_template('login.html')


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


def init_login_manager(app: Flask):
    login_manager = LoginManager()
    login_manager.login_view = 'login'
    login_manager.login_message = 'Для доступа к этой странице необходимо пройти процедуру аутентификации'
    login_manager.login_message_category = 'warning'
    login_manager.user_loader(load_user)
    login_manager.init_app(app)