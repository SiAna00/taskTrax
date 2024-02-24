from datetime import date
from flask import Flask, abort, render_template, redirect, url_for, flash
from flask_bootstrap import Bootstrap5
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user, login_required
from flask_sqlalchemy import SQLAlchemy
import os
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import DateTime, Integer, String, Text, ForeignKey
from werkzeug.security import generate_password_hash, check_password_hash
from forms import AddTaskForm, LoginForm, RegisterForm

app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(32)
Bootstrap5(app)


# Create database
class Base(DeclarativeBase):
    pass
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DB_URI", "sqlite:///tasktrax.db")
db = SQLAlchemy(model_class=Base)
db.init_app(app)

# Create a User table for all registered users
class User(db.Model, UserMixin):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(100), nullable=False)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    tasks = relationship("Task", back_populates="author")

# Create a Task table for all tasks
class Task(db.Model):
    __tablename__ = "tasks"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    author_id: Mapped[int] = mapped_column(Integer, db.ForeignKey("users.id"))
    author = relationship("User", back_populates="tasks")
    task: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(String(250), nullable=False)
    created_date: Mapped[date] = mapped_column(DateTime(), nullable=False)
    due_date: Mapped[date] = mapped_column(DateTime(), nullable=False)
    status: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)

with app.app_context():
    db.create_all()


# Configure Flask login
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


current_year = date.today().strftime("%Y")


@app.route("/")
def home():
    return render_template("index.html", current_user=current_user, date=current_year)


@app.route("/tasks")
@login_required
def show_tasks():
    tasks = db.session.execute(db.select(Task)).scalars().all()
    return render_template("tasks.html", tasks=tasks, current_user=current_user, date=current_year)


@app.route("/register", methods=["GET", "POST"])
def register():
    register_form = RegisterForm()

    if register_form.validate_on_submit():
        name = register_form.name.data
        email = register_form.email.data
        password = generate_password_hash(register_form.password.data, method="pbkdf2:sha256:600000", salt_length=16)

        user = db.session.execute(db.select(User).where(User.name == name)).scalar()

        if user:
            return redirect("/login")
        
        new_user = User(
            name=name,
            email=email,
            password=password
        )

        db.session.add(new_user)
        db.session.commit()

        login_user(user)

        return redirect("/tasks")
        
    return render_template("register.html", form=register_form, current_user=current_user, date=current_year)


@app.route("/login", methods=["GET", "POST"])
def login():
    login_form = LoginForm()

    if login_form.validate_on_submit():
        email = login_form.email.data
        password = login_form.password.data

        user = db.session.execute(db.select(User).where(User.email == email)).scalar()

        if user:
            if check_password_hash(user.password, password):
                login_user(user)
                return redirect("/tasks")
            
            flash("Incorrect password. Please try again.")
            return render_template("login.html", form=login_form, current_user=current_user, date=current_year)
        
        return redirect("/register")

    return render_template("login.html", form=login_form, current_user=current_user, date=current_year)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route("/add", methods=["GET", "POST"])
@login_required
def add_task():
    add_form = AddTaskForm()

    if add_form.validate_on_submit():
        task = add_form.task.data
        description = add_form.description.data
        created_date = date.today()
        due_date = add_form.due_date.data
        status = add_form.status.data

        new_task = Task(
            author=current_user,
            task=task,
            description=description,
            created_date=created_date,
            due_date=due_date,
            status=status
        )

        db.session.add(new_task)
        db.session.commit()

        flash("Task added successfully.")
        return redirect("/tasks")
    
    return render_template("add.html", form=add_form, current_user=current_user, date=current_year)



if __name__ == "__main__":
    app.run(debug=True)