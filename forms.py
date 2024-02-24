from flask_wtf import FlaskForm
from wtforms import DateField, StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length

class RegisterForm(FlaskForm):
    first_name = StringField("First Name", validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])
    email = StringField("Email Address", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8)])
    register_button = SubmitField("Create Account")

class LoginForm(FlaskForm):
    email = StringField("Email Address", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8)])
    login_button = SubmitField("Log In")

class AddTaskForm(FlaskForm):
    task = StringField("Task", validators=[DataRequired()])
    description = StringField("Description", validators=[DataRequired()])
    created_date = DateField("Created", format="%d-%m-%Y")
    due_date = DateField("Due", format="%d-%m-%Y")
    status = StringField("Status", validators=[DataRequired()])
    add_task_button = SubmitField("Add Task")