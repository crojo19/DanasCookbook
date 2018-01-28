import flask
import flask_login
from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
import datetime
from sqlalchemy.ext.hybrid import hybrid_method, hybrid_property
from sqlalchemy_utils import PasswordType, force_auto_coercion
from flask_bcrypt import Bcrypt

from login.forms import SignupForm, LoginForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Smokey19!@localhost/login'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'TRUE'
app.config['SECRET_KEY'] = "random string"

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.login_view = 'login'


class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(60), unique=True, nullable=False)
    _password = db.Column(db.Binary(60), nullable=False)
    authenticated = db.Column(db.Boolean, default=False)
    email_confirmation_sent_on = db.Column(db.DateTime, nullable=True)
    email_confirmed = db.Column(db.Boolean, nullable=True, default=False)
    email_confirmed_on = db.Column(db.DateTime, nullable=True)
    registered_on = db.Column(db.DateTime, nullable=True)
    last_logged_in = db.Column(db.DateTime, nullable=True)
    current_logged_in = db.Column(db.DateTime, nullable=True)
    active = db.Column(db.Boolean, nullable=False)
    first_name = db.Column(db.String(60), unique=False, nullable=False)
    last_name = db.Column(db.String(60), unique=False, nullable=False)
    middle_name = db.Column(db.String(60), unique=False, nullable=True)
    cell_phone = db.Column(db.String(60), unique=False, nullable=True)
    street_address = db.Column(db.String(60), unique=False, nullable=True)
    city = db.Column(db.String(60), unique=False, nullable=True)
    zip_code = db.Column(db.String(10), unique=False, nullable=True)
#    role = db.Column(db.String, default='user')

    def __init__(self, email, plaintext_password, first_name, last_name,
                 middle_name, cell_phone, street_address, city, zip_code,
                 email_confirmation_sent_on=None, role='user'):
        self.email = email
        self.password = plaintext_password
        self.authenticated = True
        self.email_confirmation_sent_on = email_confirmation_sent_on
        self.email_confirmed = False
        self.email_confirmed_on = None
        self.registered_on = datetime.now()
        self.last_logged_in = None
        self.current_logged_in = datetime.now()
        self.role = role
        self.active = True
        self.first_name = first_name
        self.last_name = last_name
        self.middle_name = middle_name
        self.cell_phone = cell_phone
        self.street_address = street_address
        self.city = city
        self.zip_code = zip_code

    def __repr__(self):
        return '<User %r>' % self.email

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def set_password(self, plaintext_password):
        self._password = bcrypt.generate_password_hash(plaintext_password)

    @hybrid_method
    def is_correct_password(self, test_creds):
        print("new: " + str(bcrypt.generate_password_hash(test_creds),'utf-8'))
        print("old: " + str(self._password,'utf-8'))
        return bcrypt.check_password_hash(self.password, test_creds)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.email


def init_db():
    db.init_app(app)
    db.app = app
    db.create_all()

@app.before_request
def before_request():
    flask.session.permanent = True
    app.permanent_session_lifetime = datetime.timedelta(minutes=1)
    print(datetime.timedelta(minutes=1))
    flask.session.modified = True
    flask.g.user = flask_login.current_user

@login_manager.user_loader
def load_user(email):
    return User.query.filter_by(email = email).first()


@app.route('/')
def index():
    return "Welcome to Flask"


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if request.method == 'GET':
        return render_template('signup.html', form = form)
    elif request.method == 'POST':
        if form.validate_on_submit():
            if User.query.filter_by(email=form.email.data).first():
                return "Email address already exists"
            else:
                newuser = User(form.email.data, form.password.data, form.first_name.data, form.last_name.data,
                               form.middle_name.data, form.cell_phone.data, form.street_address.data,
                               form.city.data, form.zip_code.data)
                db.session.add(newuser)
                db.session.commit()
                return "User created!!!"
    else:
        return "Form didn't validate"

@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if request.method == 'GET':
        return render_template('login.html', form=form)
    elif request.method == 'POST':
        if form.validate_on_submit():
            user=User.query.filter_by(email=form.email.data).first()
            if user:
                if user.is_correct_password(form.password.data):
                    login_user(user, False)
                    return "logged in"
                else:
                    return "Wrong password"
            else:
                return "user doesn't exist"
        else:
            return "form not validated"
    else:
        return "should never be response"

@app.route('/protecteduser')
@login_required
def protecteduser():
    return render_template('admin.html', users = User.query.all())

@app.route('/protectedadmin')
def protectedadmin():
    print(current_user.is_authenticated)
    return render_template('admin.html')


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


@login_manager.user_loader
def load_user(user_id):
    try:
        return User.query.filter_by(email=user_id).first()
    except:
        return None

if __name__ == '__main__':
    init_db()
    login_manager.init_app(app)
    app.run(port=5000, host='localhost', debug=True)