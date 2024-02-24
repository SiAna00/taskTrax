from flask_wtf import FlaskForm
from wtforms import DateField, StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length

class RegisterForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
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
    due_date = DateField("Due")
    status = StringField("Status", validators=[DataRequired()])
    add_task_button = SubmitField("Add Task")