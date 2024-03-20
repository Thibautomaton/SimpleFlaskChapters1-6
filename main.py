# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import os
from datetime import datetime
from flask import Flask, render_template, url_for, redirect, session, flash
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment
from forms import UserForm


basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SECRET_KEY'] = "chaine de caracteres"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, ".sqlite3")

bootstrap = Bootstrap(app)

db = SQLAlchemy(app)

moment = Moment(app)

class Role(db.Model):
    __tablename__ = "roles"
    name = db.Column(db.String(64), unique=True)
    id = db.Column(db.Integer, primary_key=True)

    users = db.relationship('User', backref='role')

    def __repr__(self):
        return "<Role %r>" % self.name

class User(db.Model):
    __tablename__ = "users"
    name = db.Column(db.String(64), unique=True)
    id = db.Column(db.Integer, primary_key=True)

    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return "<User %r>" % self.name


@app.route('/', methods=["GET", "POST"])
def index():
    form = UserForm()
    if form.validate_on_submit():
        user = User.query.filter_by(name=form.name.data).first()
        if user is None:
            user = User(name=form.name.data, role_id = form.role.data[0])
            print(user)

            db.session.add(user)
            db.session.commit()
            session["known"] = False
        else:
            flash("user is already known")
            session["known"] = True
        form.name.data = ''
        return redirect(url_for('index'))
    return render_template("index.html", form=form, known=session.get("known", False))

@app.route('/users')
def users():
    users = User.query.all()
    return render_template("users.html", users=users)

@app.route(('/admins'))
def admins():
    admins = Role.query.filter_by(name="Admin").first().users
    return render_template("users.html", users=admins)

if __name__ == '__main__':

    with app.app_context():
        db.drop_all()
        db.create_all()
        admin_role = Role(name="Admin", id=1)
        honor_role = Role(name="Honor", id=2)
        user_role = Role(name="User", id=3)
        user = User(name="john", role=user_role)
        user2 = User(name="pat", role=admin_role)
        db.session.add_all([admin_role, honor_role, user_role, user, user2])
        db.session.commit()
        app.run(debug=True)