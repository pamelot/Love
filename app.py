from flask import (Flask, g, render_template, flash, redirect, url_for, request, session)
import bcrpyt
from flask_bcrypt import check_password_hash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

import forms
import models
import datetime
from datetime import *; from dateutil.relativedelta import *
import calendar
from datetime import datetime as dt
import csv

DEBUG = True
PORT = 8000
HOST = '0.0.0.0'

app = Flask(__name__)
app.secret_key = 'sdonsadkksdglj,dfsg'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(userid):
	try:
		return models.User.get(models.User.id == userid)
	except models.DoesNotExist:
		return None

@app.before_request
def before_request():
	"""Connect to the db before each request."""
	g.db = models.DATABASE
	g.db.get_conn()
	g.user = current_user

@app.after_request
def after_request(response):
	"""Close the db connection after each request."""
	g.db.close()
	return response

@app.route('/register', methods=('GET', 'POST'))
def register():
	form = forms.RegisterForm()
	if form.validate_on_submit():
		flash('Yay, you registered!', 'success')
		models.User.create_user(
			username=form.username.data,
			email=form.email.data,
			password=form.password.data)
		return redirect(url_for('index'))
	return render_template('register.html', form=form)

@app.route('/login', methods=('GET', 'POST'))
def login():
	form = forms.LoginForm()
	if form.validate_on_submit():
		try:
			user = models.User.get(models.User.email == form.email.data)
		except models.DoesNotExist:
			flash("Your email and password don't match.", "error")
		else:
			if check_password_hash(user.password, form.password.data):
				login_user(user)
				flash("You've been logged in!", "success")
				return redirect(url_for('index'))
			else:
				flash("Your email and password don't match.", "error")
	return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
	logout_user()
	flash("You've been logged out", "success")
	return redirect(url_for('login'))

@app.route('/upload', methods=('GET', 'POST'))
@login_required
def upload():

	if request.method == 'POST':
		now = dt.now()
		if request.form['submit'] == 'contacts':
			with open("contact_details.csv", "rU") as csvfile:
				pamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
				for line in pamreader:

					id = line[0]
					d = line[1]
					date_added = datetime.strptime(d,"%Y-%m-%d %H:%M:%S")
					first_name = line[2]
					middle_name = line[3]
					last_name = line[4]
					email = line[5]
					phone = line[6]
					company = line[7]
					position = line[8]
					industry = line[9]
					address1 = line[10]
					address2 = line[11]
					city = line[12]
					state = line[13]
					zipcode = line[14]
					country = line[15]
					alert = line[16]
					l = line[17]
					last_updated = datetime.strptime(l, "%Y-%m-%d %H:%M:%S")
					a = line[18]
					alert_date = datetime.strptime(a, "%Y-%m-%d %H:%M:%S")

					models.Contact.create(date_added=date_added,
		                                first_name=first_name,
		                                middle_name=middle_name,
		                                last_name=last_name,
		                                email=email,
		                                phone=phone,
		                                company=company,
		                                position=position,
		                                industry=industry,
		                                address1=address1,
		                                address2=address2,
		                                city=city,
		                                state=state,
		                                zipcode=zipcode,
		                                country=country,
		                                alert=alert,
		                                last_updated=last_updated,
		                                alert_date=alert_date)

			return redirect(url_for('index'))
		if request.form['submit'] == 'notes':
			with open("note_details.csv", "rU") as csvfile:
				pamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
				for line in pamreader:
					id = line[0]
					t = line[1]
					timestamp = now
					contact = line[2]
					content = line[3]
					important = line[4]

					models.Note.create(timestamp=timestamp,
														user=1,
														contact=3,
														content=content,
														important=important)
			return redirect(url_for('index'))


	return render_template('upload.html')



@app.route('/contact', methods=('GET', 'POST'))
@login_required
def contact():
	form1 = forms.ContactForm()
	if request.method == 'POST':
		contact = models.Contact.create(first_name=form1.first_name.data,
										middle_name=form1.middle_name.data,
										last_name=form1.last_name.data,
										email=form1.email.data,
										phone=form1.phone.data,
										company=form1.company.data,
										position=form1.position.data,
										industry=form1.industry.data,
										address1=form1.address1.data,
										address2=form1.address2.data,
										city=form1.city.data,
										state=form1.state.data,
										zipcode=form1.zipcode.data,
										country=form1.country.data)
		flash("Contact saved!", "success")
		return redirect(url_for('index'))

	return render_template('contact.html', form1=form1)

@app.route('/contact_edit/<int:id>', methods=['GET','POST'])
@login_required
def contact_edit(id):
	contact = models.Contact.select().where(models.Contact.id**id).get()
	notes = contact.notes
	form1 = forms.ContactForm()
	form2 = forms.NoteForm()
	# if form1.validate_on_submit():
	if request.method == 'POST':
		if request.form['submit'] == 'update':

			contact = models.Contact(id=id,
									first_name=form1.first_name.data,
									middle_name=form1.middle_name.data,
									last_name=form1.last_name.data,
									email=form1.email.data,
									phone=form1.phone.data,
									company=form1.company.data,
									position=form1.position.data,
									industry=form1.industry.data,
									address1=form1.address1.data,
									address2=form1.address2.data,
									alert=form1.alert.data,
									city=form1.city.data,
									state=form1.state.data,
									zipcode=form1.zipcode.data,
									country=form1.country.data,
									last_updated=dt.now(),
									alert_date=(dt.now() + relativedelta(weeks=+1)))
			contact.save()
			return redirect(url_for('contact_edit', id=id))
		elif request.form['submit'] == 'save':
			note = models.Note.create(user=g.user._get_current_object(), contact_id=id, content=form2.content.data, important=form2.important.data)
			contact.last_updated = dt.now()
			contact.save()
			return redirect(url_for('contact_edit', id=id))

	return render_template("contact_edit.html", contact=contact, notes=notes, form1=form1, form2=form2)

@app.route('/contact_search', methods=['GET', 'POST'])
@login_required
def contact_search():
	form = forms.ContactForm()


	if request.method == 'POST':
		if request.form['submit'] == 'find':

			firstname = form.first_name.data
			middlename = form.middle_name.data
			lastname = form.last_name.data
			email = form.email.data
			phone = form.phone.data
			company = form.company.data
			position = form.position.data
			address = form.address1.data
			city = form.city.data
			zipcode = form.zipcode.data

			contacts = models.Contact.select().where(models.Contact.first_name.contains(firstname),
																							models.Contact.middle_name.contains(middlename),
																							models.Contact.email.contains(email),
																							models.Contact.phone.contains(phone),
																							models.Contact.company.contains(company),
																							models.Contact.position.contains(position),
																							models.Contact.address1.contains(address),
																							models.Contact.city.contains(city),
																							models.Contact.zipcode.contains(zipcode))

			return render_template('contact_search.html', form=form, contacts=contacts)

		elif request.form['submit'] == 'create':
			if form.validate_on_submit():
				message = "Contact successfully saved."
				contact = models.Contact.create(first_name=form.first_name.data,
											middle_name=form.middle_name.data,
											last_name=form.last_name.data,
											email=form.email.data,
											phone=form.phone.data,
											company=form.company.data,
											position=form.position.data,
											industry=form.industry.data,
											address1=form.address1.data,
											address2=form.address2.data,
											city=form.city.data,
											state=form.state.data,
											zipcode=form.zipcode.data,
											country=form.country.data,
											alert=form.alert.data,
											alert_date=(dt.now() + relativedelta(weeks=+1)))
				return render_template('contact_search.html', form=form, message=message)
			else:
				message = "First name is required."
				return render_template('contact_search.html', form=form, message=message)
	return render_template('contact_search.html', form=form)

@app.route('/', methods=['GET', 'POST'])
@login_required
def index():

	stream = models.Note.select().limit(100)
	now = dt.now()
	d = now + relativedelta(weeks=+1)
	reminders = models.Reminder.select().where((models.Reminder.status == 'active') & (models.Reminder.date < d)).order_by(models.Reminder.date)
	notes = models.Note.select().order_by(models.Note.timestamp.desc()).limit(5)
	contacts = models.Contact.select().limit(5)
	old_contacts = models.Contact.select().where((models.Contact.alert_date < d) & (models.Contact.alert == True)).order_by(models.Contact.alert_date)

	if request.method == 'POST':
		if request.form['submit'] == 'cancel':
			id = request.form['id']
			reminder = models.Reminder.select().where(models.Reminder.id**id).get()
			reminder.status = 'cancel'
			reminder.save()
			return redirect(url_for('index'))
		elif request.form['submit'] == 'snooze':
			id = request.form['id']
			reminder = models.Reminder.select().where(models.Reminder.id**id).get()
			reminder.date = now + relativedelta(weeks=1)
			reminder.save()
			return redirect(url_for('index'))
		elif request.form['submit'] == 'done':
			id = request.form['id']
			reminder = models.Reminder.select().where(models.Reminder.id**id).get()
			reminder.status = 'done'
			reminder.save()
			return redirect(url_for('index'))
		elif request.form['submit'] == 'save':
			date_data = request.form['date']
			if date_data:
				reminder = models.Reminder.create(user=g.user._get_current_object(),
								  												content=request.form['content'],
								  												contact=g.user._get_current_object(),
								  												date=request.form['date'],
								  												status='active')
				return redirect(url_for('index'))
			else:
				message = "Date is required"
				return render_template('stream.html', stream=stream, reminders=reminders, contacts=contacts, notes=notes, now=now, old_contacts=old_contacts, user=current_user, message=message)

		elif request.form['submit'] == 'cancel_alert':
			id = request.form['contact_id']
			contact = models.Contact.select().where(models.Contact.id**id).get()
			contact.alert = False
			contact.save()
			return redirect(url_for('index'))
		elif request.form['submit'] == 'snooze_alert':
			id = request.form['contact_id']
			contact = models.Contact.select().where(models.Contact.id**id).get()
			if (contact.alert_date < now):
				contact.alert_date = now + relativedelta(weeks=+1)
			contact.alert_date = contact.alert_date + relativedelta(weeks=+1)
			contact.save()
			return redirect(url_for('index'))
		elif request.form['submit'] == 'update':
			id = request.form['contact_id']
			contact = models.Contact.select().where(models.Contact.id**id).get()
			contact.alert_date = now + relativedelta(weeks=+3)
			contact.save()
			return redirect(url_for('index'))
		return redirect(url_for('index'))
	return render_template('stream.html', stream=stream, reminders=reminders, contacts=contacts, notes=notes, now=now, old_contacts=old_contacts, user=current_user)

@app.route('/stream')
@app.route('/stream/<username>')
def stream(username=None):
	template = 'stream.html'
	if username and username != current_user.username:
		user = models.User.select().where(models.User.username**username).get()
		stream = user.notes.limit(100)
	else:
		stream = current_user.get_stream().limit(100)
		user = current_user
	if username:
		template = 'user_stream.html'
	return render_template(template, stream=stream, user=user)


if __name__ == '__main__':
    models.initialize()
    try:
	       models.User.create_user(
	            username='user',
	            email='user@email.com',
	            password='password',
	            admin=True
	        )
    except ValueError:
        pass
    app.run(debug=DEBUG, host=HOST, port=PORT)