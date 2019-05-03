from project import db, login_manager
from datetime import datetime
from flask_login import UserMixin
from project import app
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

@login_manager.user_loader
def load_lecturer(user_id):
	return User.query.get(int(user_id))

comms = db.Table('comms',
	db.Column('lecturer_id', db.Integer, db.ForeignKey('user.id')),
	db.Column('student_id', db.Integer, db.ForeignKey('user.id'))
	)

#user table
class User(db.Model, UserMixin):
 	id = db.Column(db.Integer, primary_key=True)
 	name = db.Column(db.String(120), unique=True, nullable=False)
 	username = db.Column(db.String(120), unique=True, nullable=False)
 	email = db.Column(db.String(120), unique=True, nullable=False)
 	password = db.Column(db.String(60), nullable=False)
 	accessCode = db.Column(db.String(6), nullable=False)
 	is_lecturer = db.Column(db.Boolean, default=True, nullable=False)
 	assignments = db.relationship('Assignment_Posted', backref='ass')
 	updates = db.relationship('Update', backref='upt')
 	studs = db.relationship('User', secondary=comms,
 		primaryjoin=(comms.c.lecturer_id == id), secondaryjoin=(comms.c.student_id == id))
 		# backref=db.backref('lecStudent', lazy='dynamic'), lazy='dynamic')
 	received_assignment = db.relationship('Assignment_Received', backref='assReceived')	


 	def __repr__(self):
 		return format("User("+self.name+","+self.username+","+self.email+","+self.accessCode+","+str(self.is_lecturer)+")")

#table for lecturers
# class Lecturers(db.Model, UserMixin):
# 	id = db.Column(db.Integer, primary_key=True)
# 	name = db.Column(db.String(120), unique=True, nullable=False)
# 	username = db.Column(db.String(120), unique=True, nullable=False)
# 	email = db.Column(db.String(120), unique=True, nullable=False)
# 	password = db.Column(db.String(60), nullable=False)
# 	accessCode = db.Column(db.String(6), nullable=False)
# 	studs = db.relationship('Students', secondary=comms, backref=db.backref('lecStudent', lazy='dynamic'))
# 	assignments = db.relationship('Assignment_Posted', backref='ass')

# 	def __repr__(self):
# 		return format("Lecturer("+self.name+","+self.username+","+self.email+")")


# table for students
# class Students(db.Model, UserMixin):
# 	id = db.Column(db.Integer, primary_key=True)
# 	name = db.Column(db.String(120), unique=True, nullable=False)
# 	username = db.Column(db.String(120), unique=True, nullable=False)
# 	email = db.Column(db.String(120), unique=True, nullable=False)
# 	password = db.Column(db.String(60), nullable=False)
# 	lec_code = db.Column(db.String(6), nullable=False)

# 	def __repr__(self):
# 		return format("Student(" + self.name + "," + self.username + "," + self.email + ")")


# table for updates posted by lecturers
class Update(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	content = db.Column(db.Text, nullable=False)
	lec_id = db.Column(db.Integer, db.ForeignKey('user.id'))

	def __repr__(self):
		return format("Update("+self.content+","+str(self.date_posted)+")")


class Assignment_Posted(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	topic = db.Column(db.String(20), nullable=False)
	description = db.Column(db.Text,nullable=False)
	submission_date = db.Column(db.DateTime, nullable=False)
	lec_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	# received = db.relationship('Assignment_Received', backref='receivedAss')

	def __repr__(self):
		return format("Assignment(" + self.description + "," + str(self.submission_date) + ")")


class Assignment_Received(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(300))
	data = db.Column(db.LargeBinary)
	sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	# posted_id = db.Column(db.Integer, db.ForeignKey('Assignment_Posted.id'))

class MyModelView(ModelView):
	def is_accessible(self):
		return False

