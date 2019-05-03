from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DateField
from wtforms.widgets import TextArea
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_wtf.file import FileField,FileRequired
from project.models import User

#class for lecturer login form
class LecturerLoginForm(FlaskForm):
	lec_username = StringField('USERNAME',
		validators=[DataRequired(), Length(min=2, max=20)])
	lec_password = PasswordField('PASSWORD',
		validators=[DataRequired()])
	submit = SubmitField('LOGIN')


class UpdateForm(FlaskForm):
	content = StringField('CONTENT',
		validators=[DataRequired()], widget=TextArea())
	submit = SubmitField('POST')

class AssignmentForm(FlaskForm):
	topic = StringField('TOPIC',
		validators=[DataRequired(), Length(min=2, max=20)])
	description = StringField('DESCRIPTION',
		validators=[DataRequired()], widget=TextArea())
	due_date = DateField('DUE DATE',
		validators=[DataRequired()])
	submit = SubmitField('SEND')

# class for student access code form
class AccessCodeForm(FlaskForm):
	code = StringField('CODE',
		validators=[DataRequired()])
	submit = SubmitField('SEND')

#class for student sign up form
class StudentSignUpForm(FlaskForm):
	name = StringField('NAME',
		validators=[DataRequired(), Length(min=2, max=120)])
	username = StringField('USERNAME',
		validators=[DataRequired(), Length(min=2, max=60)])
	email = StringField('EMAIL',
		validators=[DataRequired(), Email()])
	password = PasswordField('PASSWORD',
		validators=[DataRequired()])
	confirm_password = PasswordField('CONFIRM PASSWORD',
		validators=[DataRequired(), EqualTo('password')])
	lec_access_code = StringField('LECTURER ACCESS CODE',
		validators=[DataRequired(), Length(min=2, max=6)])
	submit = SubmitField('SIGN UP')

	# function to throw an error if student username already exists
	def validate_username(self, username):
		check = User.query.filter_by(username=username.data).first()
		if check:
			raise ValidationError('The username already exists! Please choose another name.')

	# function to throw an error if student email already exists
	def validate_username(self, email):
		check = User.query.filter_by(email=email.data).first()
		if check:
			raise ValidationError('The email already exists! Please choose another email.')

#class for student login form
class StudentLoginForm(FlaskForm):
	student_username = StringField('USERNAME',
		validators=[DataRequired(), Length(min=2, max=20)])
	student_password = PasswordField('PASSWORD',
		validators=[DataRequired()])
	submit = SubmitField('LOGIN')

class AssignmentSubmissionForm(FlaskForm):
	upload = FileField(validators=[FileRequired()])
	submit = SubmitField('UPLOAD')
	