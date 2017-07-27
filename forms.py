from flask_wtf import Form
from wtforms import StringField, PasswordField, IntegerField, TextAreaField, DateField, FormField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Regexp, ValidationError, Email, Length, EqualTo
from models import User, Note, Contact, Reminder
import datetime

def name_exists(form, field):
	if User.select().where(User.username == field.data).exists():
		raise ValidationError('User with that name already exists.')

def email_exists(form, field):
	if User.select().where(User.email == field.data).exists():
		raise ValidationError('User with that email already exists.')


class RegisterForm(Form):
	username = StringField(
		'Username',
		validators=[
			DataRequired(),
			Regexp(
				r'^[a-zA-Z0-9_]+$',
				message=("Username should be one word, letters, numbers, and underscores only.")
			),
			name_exists
		])
	email = StringField(
		'Email',
		validators=[
			DataRequired(),
			Email(),
			email_exists
		])
	password = PasswordField(
		'Password',
		validators=[
			DataRequired(),
			Length(min=2),
			EqualTo('password2', message='Passwords must match.')
		])
	password2 = PasswordField(
		'Confirm Password',
		validators=[DataRequired()]
	)

class LoginForm(Form):
	email = StringField("Email", validators=[DataRequired(), Email()])
	password = PasswordField("Password", validators=[DataRequired()])

class NoteForm(Form):
	content = TextAreaField("content", validators=[DataRequired()])
	submit = SubmitField('submit')
	important = BooleanField()

class ContactNoteForm(Form):
	first_name = StringField('First Name')
	last_name = StringField('Last Name')

class ContactForm(Form):
	first_name = StringField('First Name', validators=[DataRequired()])
	middle_name = StringField('Middle Name')
	last_name = StringField('Last Name')
	email = StringField('Email')
	phone = StringField('phone')
	company = StringField('Company')
	position = StringField('Position')
	industry = StringField('Industry')
	address1 = StringField('Address Line 1')
	address2 = StringField('Address Line 2')
	city = StringField('City')
	state = StringField('State')
	zipcode = StringField('Zipcode')
	country = StringField('Country')
	note = StringField('Note')
	alert = BooleanField()

class ReminderForm(Form):
	content = StringField('Content', validators=[DataRequired()])
	date = DateField('DatePicker', format='%Y-%m-%d', validators=[DataRequired()])
	snooze = SubmitField(label='snooze')
	reset = SubmitField(label='reset')
	cancel = SubmitField(label='cancel')






