import os
from flask import Flask, url_for, redirect, render_template, request, abort, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore, \
    UserMixin, RoleMixin, login_required, current_user
from flask_security.utils import encrypt_password
from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib import sqla
from flask_admin import helpers as admin_helpers
from wtforms import TextAreaField
from wtforms.widgets import TextArea
from wtforms.validators import ValidationError
from flask_ckeditor import CKEditorField, CKEditor

app = Flask(__name__)

# For app configuration change config.py
app.config.from_pyfile('config.py')

db = SQLAlchemy(app)
ckeditor = CKEditor(app)

# Define models
roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

# classes
class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))

class Substitution(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    text = db.Column(db.Text)
    level = db.Column(db.String(100))
    language = db.Column(db.String(100))
    dailies = db.relationship('Daily', backref='substitution', lazy=True)

    def __repr__(self):
        return self.title

class Riddle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    text = db.Column(db.UnicodeText())
    level = db.Column(db.String(100))
    language = db.Column(db.String(100))
    dailies = db.relationship('Daily', backref='riddle', lazy=True)

    def __repr__(self):
        return self.title

class Daily(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    riddle_id = db.Column(db.Integer, db.ForeignKey('riddle.id'))
    substitution_id = db.Column(db.Integer, db.ForeignKey('substitution.id'))


### Setup Flask-Security ###

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

# Customized view classes

class MyHomeView(AdminIndexView):
    @expose('/')
    def index(self):
        dailies = Daily.query.all()
        return self.render('admin/index.html', dailies=dailies)

# Customized model view classes

# Basic Flask-Security customized model view class
class MyView(sqla.ModelView):
    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False

        if current_user.has_role('superuser'):
            return True

        return False

    def _handle_view(self, name, **kwargs):
        """
        Override builtin _handle_view in order to redirect users when a view is not accessible.
        """
        if not self.is_accessible():
            if current_user.is_authenticated:
                # permission denied
                abort(403)
            else:
                # login
                return redirect(url_for('security.login', next=request.url))

# Customized view class for Substitution
class SubstitutionView(MyView):
    column_exclude_list = ('text')
    form_widget_args = {
        'text': {
            'rows': 15,
        }
    }
    form_excluded_columns = ('dailies')

# Customized view class for Riddles with CKeditor

class RiddleView(MyView):
    column_exclude_list = ('text')
    form_overrides = {
        'text': CKEditorField
    }
    form_excluded_columns = ('dailies')
    edit_template = 'admin/edit.html'

# Customized view class for Dailies
class DailyView(MyView):
    # column_list = ('name', 'substitution.title', 'riddle.title')

    def on_model_change(self, form, model, is_created):
        dailies = Daily.query.all()
        for daily in dailies:
            if (daily.riddle_id and not daily.substitution_id) or (daily.substitution_id and not daily.riddle_id):
                return model
            elif daily.riddle_id and daily.substitution_id: 
                raise ValidationError('Daily can have only one active exercise (riddle or substitution)')
            else:
                raise ValidationError('Please select exercise (riddle or substitution) for this daily')
    

# define a context processor for merging flask-admin's template context into the
# flask-security views.
@security.context_processor
def security_context_processor():
    return dict(
        admin_base_template=admin.base_template,
        admin_view=admin.index_view,
        h=admin_helpers,
        get_url=url_for
    )    

# TO-DO just an example how to pass query in a view, change it so it is not global
# @app.context_processor
# def inject_paths():
#     # you will be able to access dict in all views
#     dailies = Daily.query.all()
#     return dict(dailies=dailies)

# Flask views
@app.route('/')
def index():
    return redirect(url_for('security.login'))

### Setup flask-admin interface ###

# create admin
admin = Admin(app, name='KriptoAdmin', base_template='my_master.html', template_mode='bootstrap3', index_view=MyHomeView())

# CRUD views
admin.add_view(DailyView(Daily, db.session))
admin.add_view(RiddleView(Riddle, db.session))
admin.add_view(SubstitutionView(Substitution, db.session))

import sample_db
# creates a test db with an admin user for login        
def test_db():
    db.drop_all()
    db.create_all()

    with app.app_context():
        # create roles
        role1 = Role(name = sample_db.role1['name'])
        role2 = Role(name = sample_db.role2['name'])
        db.session.add(role1)
        db.session.add(role2)
        db.session.commit()

        # create an admin user
        test_user = user_datastore.create_user(
            email = sample_db.user1['email'],
            password = encrypt_password(sample_db.user1['password']),
            roles=[role1 , role2]
        )
        db.session.commit()
        
        # create test exercises
        db.session.add(Riddle(title= sample_db.riddle1['title'], text= sample_db.riddle1['text'], level= sample_db.riddle1['level'], language= sample_db.riddle1['language']))
        db.session.add(Riddle(title= sample_db.riddle2['title'], text= sample_db.riddle2['text'], level= sample_db.riddle2['level'], language= sample_db.riddle2['language']))
        db.session.add(Substitution(title= sample_db.substitution1['title'], text= sample_db.substitution1['text'], level= sample_db.substitution1['level'], language= sample_db.substitution1['language']))
        db.session.add(Substitution(title= sample_db.substitution2['title'], text= sample_db.substitution2['text'], level= sample_db.substitution2['level'], language= sample_db.substitution2['language']))
        db.session.commit()

if __name__ == '__main__':


    # Uncomment this call to create a test db with a test db user
    # email: Admin
    # password: admin
    test_db()

    app.run(port=3001)

