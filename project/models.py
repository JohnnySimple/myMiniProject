from project import db, login_manager
from flask_login import UserMixin
from project import app
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView




#table for lecturers
class Lecturers(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(120), unique=True, nullable=False)
	username = db.Column(db.String(120), unique=True, nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)
	password = db.Column(db.String(60), nullable=False)


	def __repr__(self):
		return format("Lecturer("+self.name+","+self.username+","+self.email+")")

class MyModelView(ModelView):
	def is_accessible(self):
		return False

