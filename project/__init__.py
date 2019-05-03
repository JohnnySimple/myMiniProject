from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView



app = Flask(__name__)

app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

#creating the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///miniProjDb.db'
db = SQLAlchemy(app)
login_manager = LoginManager(app)

from project.models import User, Update, Assignment_Posted, Assignment_Received

#lecturers = Lecturers()

admin = Admin(app)
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Update, db.session))
admin.add_view(ModelView(Assignment_Posted, db.session))
admin.add_view(ModelView(Assignment_Received, db.session))

from project import routes