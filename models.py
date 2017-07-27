
import datetime

from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import UserMixin
from peewee import *

DATABASE = SqliteDatabase('crm.db')

class User(UserMixin, Model):
	username = CharField(unique=True)
	email = CharField(unique=True)
	password = CharField(max_length=100)
	joined_at = DateTimeField(default=datetime.datetime.now)
	is_admin = BooleanField(default=False)

	class Meta:
		database = DATABASE
		order_by = ('-joined_at',)

	def get_notes(self):
		return Note.select().where(Note.user == self)

	def get_stream(self):
		return Note.select().where((Note.user == self))

	@classmethod
	def create_user(cls, username, email, password, admin=False):
		try:
			cls.create(
				username=username,
				email=email,
				password=generate_password_hash(password),
				is_admin=admin)
		except IntegrityError:
			# if the values are not unique
			raise ValueError('User already exists')

class Contact(Model):
	id = IntegerField(primary_key=True)
	date_added = DateTimeField(default=datetime.datetime.now)
	first_name = CharField()
	middle_name = CharField()
	last_name = CharField()
	email = CharField()
	phone = CharField()
	company = CharField()
	position = CharField()
	industry = CharField()
	address1 = CharField()
	address2 = CharField()
	city = CharField()
	state = CharField()
	zipcode = CharField()
	country = CharField(default="United States")
	alert = BooleanField(default=False)
	last_updated = DateTimeField(default=datetime.datetime.now)
	alert_date = DateTimeField()

	class Meta:
		database = DATABASE
		order_by = ('-last_name',)


class Reminder(Model):
	id = IntegerField(primary_key=True)
	timestamp = DateTimeField(default=datetime.datetime.now)
	user = ForeignKeyField(rel_model=User, related_name='reminders')
	contact = ForeignKeyField(rel_model=Contact, related_name='reminders')
	content = TextField()
	date = DateTimeField()
	status = CharField(default="active")


	class Meta:
		database = DATABASE
		order_by = ('-timestamp',)

class Note(Model):
	id = IntegerField(primary_key=True)
	timestamp = DateTimeField(default=datetime.datetime.now)
	user = ForeignKeyField(rel_model=User, related_name='notes')
	contact = ForeignKeyField(rel_model=Contact, related_name='notes')
	content = TextField()
	reminder = DateTimeField(default=datetime.datetime.now)
	important = BooleanField(default=False)

	class Meta:
		database = DATABASE
		order_by = ('-timestamp',)


def initialize():
	DATABASE.get_conn()
	DATABASE.create_tables([User, Contact, Reminder, Note], safe=True)
	DATABASE.close()
