from flask import render_template, url_for, flash, redirect, request, send_file
from project import app
from project import db
from project.forms import LecturerLoginForm, UpdateForm, AssignmentForm, AccessCodeForm, StudentSignUpForm, StudentLoginForm, AssignmentSubmissionForm
from flask_login import login_user, current_user, logout_user
from project.models import User, Update, Assignment_Posted, Assignment_Received
from io import BytesIO
from werkzeug.utils import secure_filename
# from flask_sqlalchemy_session import flask_scoped_session


# session = flask_scoped_session(session_factory, app)

UPLOAD_FOLDER = '/path/to/the/uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/',methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
	if current_user.is_authenticated:
		return redirect(url_for('lecturer_home'))
	lec_form = LecturerLoginForm()
	access_code = AccessCodeForm()

	if lec_form.validate_on_submit():
		lecturer = User.query.filter_by(username=lec_form.lec_username.data).first()
		if lecturer and lecturer.password == lec_form.lec_password.data:
			if lecturer.is_lecturer == True:
				login_user(lecturer)
				return redirect(url_for('lecturer_home'))
			else:
				flash('User not a lecturer!!!', 'danger')
		else:
			flash('Login unsuccessful.Please check your username and password!', 'danger')


	if access_code.validate_on_submit():
		lec_code = User.query.filter_by(accessCode = access_code.code.data).first()
		if lec_code:
			return redirect(url_for('student_signUp_login', code=lec_code))
		else:
			flash('Incorrect access code!', 'danger')
	return render_template("index.html", title="Home", lec_form=lec_form, access_code=access_code)



@app.route('/lecturer_home', methods=['GET', 'POST'])
def lecturer_home():
	update_form = UpdateForm()
	assignment_form = AssignmentForm()

	students_num = 0
	users = User.query.all()

	for a in users:
		if a.is_lecturer == False and a.accessCode == current_user.accessCode:
			students_num = students_num + 1

	if update_form.validate_on_submit():
		update = Update(content= update_form.content.data, lec_id=current_user.id)
		db.session.add(update)
		db.session.commit()
		
		flash(format('Update posted successfully! ' ), 'success')

		return redirect(url_for("lecturer_home"))

	if assignment_form.validate_on_submit():
		assign = Assignment_Posted(topic=assignment_form.topic.data, description=assignment_form.description.data, 
			submission_date=assignment_form.due_date.data, lec_id=current_user.id)
		db.session.add(assign)
		db.session.commit()

		flash(format('Assignment posted successfully! '), 'success')


	assignments = Assignment_Posted.query.all()
	ass_posted = []

	for a in assignments:
		if a.lec_id == current_user.id:
			ass_posted.append(a)

	return render_template("lecturer_home.html", title="Lecturer Home", update_form=update_form, 
		assignment_form=assignment_form, students_num=students_num, ass_posted=ass_posted, assignments=assignments)


@app.route('/student_home', methods=['GET', 'POST'])
def student_home():
	assignments = Assignment_Posted.query.all()
	users = User.query.all()
	assignment_form = AssignmentSubmissionForm()
	squad = []
	user=User()
	updates = Update.query.all()

	# if request.method == 'POST':
	# 	file = request.files['inputFile']


	# if assignment_form.validate_on_submit():
	# 	assignment_file = Assignment_Received(name=file.filename, data=file.read())
	# 	db.session.add(assignment_file)
	# 	db.session.commit()
	# 	flash(format('Assignment sent successfully!'), 'success')
	return render_template('student_home.html',user=user, users=users, assignments=assignments,
	updates=updates, assignment_form=assignment_form)

@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
	if request.method == 'POST':
		f = request.files['inputFile']
		# f.save(secure_filename(f.filename))
		assignment_file = Assignment_Received(name=f.filename, data=f.read(), sender_id=current_user.id)
		db.session.add(assignment_file)
		db.session.commit()
		flash(format('successful'), 'success')

	return 'file uploaded successfully!!!'

@app.route('/student_signUp_login', methods=['GET', 'POST'])
def student_signUp_login():

	form = StudentSignUpForm()
	login_form = StudentLoginForm()
	# code = Lecturers.query.filter_by(accessCode=code)

	if form.validate_on_submit():
		student = User(name=form.name.data, username=form.username.data, email=form.email.data, password=form.password.data, accessCode=form.lec_access_code.data, is_lecturer=False)
		db.session.add(student)
		db.session.commit()
		flash(format('Account created successfully'),'success')

		return redirect('student_signUp_login')

	#logging in student
	if login_form.validate_on_submit():
		student = User.query.filter_by(username=login_form.student_username.data).first()
		if student and student.password == login_form.student_password.data:
			if student.is_lecturer == False:
				login_user(student)
				stud = login_form.student_username.data
				return redirect(url_for('student_home'))
			else:
				flash('User not a student!!!', 'danger')
		else:
			flash('Username or password not correct!!!', 'danger')

	return render_template('student_signUp_login.html', form=form, login_form=login_form)

@app.route('/admin')
def admin():
	return render_template("admin")


@app.route('/student_assignment_page/<name>')
def student_assignment_page(name):
	assignments = Assignment_Posted.query.filter_by(id=name).first()
	return render_template('student_assignment_page.html', assignments=assignments)


@app.route('/submitted_assignment')
def submitted_assignment():
	assignments = Assignment_Received.query.all()
	users = User()

	return render_template('submitted_assignment.html', assignments=assignments, users=users)

@app.route('/return_files/<content>')
def return_files(content):
	file_data = Assignment_Received.query.filter_by(name=content).first()
	return send_file(BytesIO(file_data.data), attachment_filename=file_data.name, as_attachment=True)

# route for deleting assignments by lecturers
@app.route('/remove/<ass_id>', methods=['GET', 'POST'])
def remove(ass_id):
	asses = Assignment_Posted.query.all()
	Assignment_Posted.query.filter_by(id=ass_id).delete()
	db.session.commit()
	return "Deleted successfully!"

#route for logging out
@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))