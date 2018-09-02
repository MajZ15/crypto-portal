import os
from flask import Flask, url_for, redirect, render_template, request, abort
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore, \
    UserMixin, RoleMixin, login_required, current_user
from flask_security.utils import encrypt_password
from flask_admin import Admin
from flask_admin.contrib import sqla
from flask_admin import helpers as admin_helpers
from wtforms import TextAreaField
from wtforms.widgets import TextArea

app = Flask(__name__)

# For app configuration change config.py
app.config.from_pyfile('config.py')

db = SQLAlchemy(app)

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
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

class Substitution(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    text = db.Column(db.Text)
    level = db.Column(db.String(100))
    language = db.Column(db.String(100))

class Riddle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    text = db.Column(db.UnicodeText())
    level = db.Column(db.String(100))
    language = db.Column(db.String(100))

### Setup Flask-Security ###

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

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
# Customized view class for Riddles
class CKTextAreaWidget(TextArea):
    def __call__(self, field, **kwargs):
        if kwargs.get('class'):
            kwargs['class'] += ' ckeditor'
        else:
            kwargs.setdefault('class', 'ckeditor')
        return super(CKTextAreaWidget, self).__call__(field, **kwargs)

class CKTextAreaField(TextAreaField):
    widget = CKTextAreaWidget()

class RiddleView(MyView):
    extra_js = ['//cdn.ckeditor.com/4.6.0/standard/ckeditor.js']
    column_exclude_list = ('text')
    form_overrides = {
        'text': CKTextAreaField
    }
    

# Flask views
@app.route('/')
def index():
    print(current_user)
    return redirect(url_for('security.login'))

### Setup flask-admin interface ###

# create admin
admin = Admin(app, name='KriptoAdmin', base_template='my_master.html', template_mode='bootstrap3')

# CRUD views
admin.add_view(RiddleView(Riddle, db.session))
admin.add_view(SubstitutionView(Substitution, db.session))

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

# creates a test db with an admin user for login        
def test_db():
    db.drop_all()
    db.create_all()

    with app.app_context():
        user_role = Role(name='user')
        super_user_role = Role(name='superuser')
        db.session.add(user_role)
        db.session.add(super_user_role)
        db.session.commit()

        test_user = user_datastore.create_user(
            email='admin',
            password=encrypt_password('admin'),
            roles=[user_role, super_user_role]
        )
        db.session.commit()

if __name__ == '__main__':


    # Uncomment this call to create a test db with a test db user
    # email: Admin
    # password: admin
    # test_db()

    app.run(debug=True, port=3001)

