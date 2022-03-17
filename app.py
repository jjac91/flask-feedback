"""Feedbak Application"""
from flask import Flask, request, redirect, render_template, session
from models import Feedback, db, connect_db, User
from forms import RegisterUserForm, LoginForm, FeedbackForm
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///feedbackdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.config['SECRET_KEY'] = "oh-so-secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()


@app.route("/")
def root():
    """redirects to the register page"""

    return redirect("/register")


@app.route("/register", methods=["GET", "POST"])
def register():
    """provides a form for a user to register and handles its submission"""
    if "username" in session:
        return redirect(f"/users/{session['username']}")

    form = RegisterUserForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        user = User.register(username, password, email, first_name, last_name)

        db.session.commit()

        session["username"] = user.username
        return redirect(f"/users/{session['username']}")
    else:
        return render_template("register_user.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    """provides a form for a user to log in and handles its submission"""
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)

        if user:
            session["username"] = user.username
            return redirect(f"/users/{session['username']}")
        else:
            form.username.errors = ["Invalid Username or Password"]

    return render_template("login_user.html", form=form)


@app.route("/users/<username>")
def user_details(username):
    """Example hidden page for logged-in users only."""

    if "username" not in session or username != session['username']:
        return redirect("/")

    user = User.query.get(username)

    return render_template("user_details.html", user=user)


@app.route("/logout")
def logout():
    """Logs user out and redirects to homepage."""

    session.pop("username")

    return redirect("/login")


@app.route("/users/<username>/delete", methods=["POST"])
def delete_user(username):
    if "username" not in session or username != session['username']:
        return redirect("/")

    user = User.query.get(username)
    db.session.delete(user)
    db.session.commit()
    session.pop("username")

    return redirect("/")


@app.route("/users/<username>/feedback/add", methods=["GET", "POST"])
def feedback_add(username):
    """provides a form for a user to log in and handles its submission"""

    if "username" not in session or username != session['username']:
        return redirect("/")

    form = FeedbackForm()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        username = username

        feedback = Feedback(
            title=title,
            content=content,
            username=username)

        db.session.add(feedback)
        db.session.commit()

        return redirect(f"/users/{session['username']}")

    return render_template("login_user.html", form=form)


@app.route("/feedback/<int:feedback_id>/update", methods=["GET", "POST"])
def feedback_update(feedback_id):
    """provides a form for a user to log in and handles its submission"""

    feedback = Feedback.query.get(feedback_id)

    if "username" not in session or feedback.username != session['username']:
        return redirect("/")

    form = FeedbackForm(obj=feedback)

    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data

        db.session.commit()

        return redirect(f"/users/{session['username']}")

    return render_template("/feedback_edit.html", form=form, feedback=feedback)


@app.route("/feedback/<int:feedback_id>/delete", methods=["POST"])
def delete_feedback(feedback_id):

    feedback = Feedback.query.get(feedback_id)

    if "username" not in session or feedback.username != session['username']:
        return redirect("/")

    db.session.delete(feedback)
    db.session.commit()

    return redirect("/")
