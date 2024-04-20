import os
import secrets
import datetime
import random
from cs50 import SQL  
from flask import (
    Flask,
    redirect,
    render_template,
    jsonify,
    request,
    session,
    flash,
    url_for
)
from flask_session import Session
from flask_mail import Mail, Message

from dotenv import find_dotenv, load_dotenv

from functools import wraps
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from helpers import (
    apology, 
    login_required, 
    admin_required, 
)

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

my_secret_email = os.getenv("my_secret_email")
my_secret_pass = os.getenv("my_secret_pass")






app = Flask(__name__)

current_username = ""
current_password = ""
current_email= ""
current_verification_code = {}

app.config['MAIL_SERVER'] = 'smtp.office365.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = my_secret_email
app.config['MAIL_PASSWORD'] = my_secret_pass
app.config['MAIL_DEFAULT_SENDER'] = my_secret_email

mail = Mail(app)

app.config["SECRET_KEY"] = secrets.token_hex(32)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Using CS50 SQL library to connect to my database
db = SQL("sqlite:///users.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    return render_template("index.html")


@app.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():
    if request.method == "POST":
        # Ensure old password, new password, and confirmation are submitted
        old_password = request.form.get("old_password")
        new_password = request.form.get("new_password")
        confirmation = request.form.get("confirmation")

        # Query database for user's current hashed password
        user_id = session["user_id"]
        current_hashed_password = db.execute("SELECT hash FROM users WHERE id = ?", user_id)[0]["hash"]

        if not check_password_hash(current_hashed_password, old_password):
            return apology("Invalid old password", 403)

        if new_password != confirmation:
            return apology("New password and confirmation do not match", 403)

        new_hashed_password = generate_password_hash(new_password)
        db.execute("UPDATE users SET hash = ? WHERE id = ?", new_hashed_password, user_id)
        print("password changed for id:",user_id)

        # Redirect user to home page with a success message
        flash("Password changed successfully!", "success")
        return redirect("/")
    
    return render_template("change_password.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        current_username = request.form.get("username")

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/verification", methods=["GET", "POST"])
def verification():  #works fine
    #
    send_verification_email(current_email,current_verification_code)
    
    if request.method == "POST":
        code = request.form.get("verification_code")
        print("code recived is: ",code)
        print("code:",code, "  verification_code: ",current_verification_code)
        if str(code).strip() == str(current_verification_code).strip():
    
            print("All went good!")
            hash = generate_password_hash(current_password)

            try:
                new_user = db.execute(
                    "INSERT INTO users (username, hash, email) VALUES(?, ?, ?)", current_username, hash, current_email
                )
            except:
                return apology("Username Already Exists")
            session["user_id"] = new_user
            return redirect("/")
        
        return render_template("register.html")
    else: 
        return render_template("verification.html")
def send_verification_email(email, code):  #*Works well
    subject = "Email Verification Code"
    
    # HTML-formatted body with a larger and copyable verification code
    body = f"""
        <p>Dear User,</p>
        <p>Thank you for registering to our TODO! Your verification code is:</p>
        <p style="font-size: 18px; font-weight: bold; background-color: #f4f4f4; padding: 10px; border-radius: 5px; user-select: all;">{code}</p>
        <p>Please enter this code on the website to complete the registration process.</p>
        <p>Best regards,<br>Á TODO !</p>
    """

    message = Message(subject, recipients=[email], html=body)

    try:
        mail.send(message)
        print("Email sent successfully")
    except Exception as e:
        print(f"Error sending email: {e}")


def verification_code():
    global current_verification_code
    current_verification_code = str(random.randint(100000, 999999))
    return 


@app.route("/register", methods=["GET", "POST"]) 
def register():
    """Register user"""
    global current_username
    global current_password
    global current_email
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        email = request.form.get("email")

        # Check if the email already exists in the database
        existing_user = db.execute("SELECT * FROM users WHERE email = ?", email)
        if existing_user:
            return apology("Email already exists. Please use a different email.")

        # checking if the values are acceptable
        if not username:
            return apology("Username Error")
        if not password:
            return apology("Password Error")
        if not confirmation:
            return apology("Confirmation Error")

        if password != confirmation:
            return apology("Password and Confirmation DO NOT MATCH")
        
        current_username = username
        current_password = password
        current_email = email
        verification_code()
        return redirect("/verification")

    else:
        return render_template("register.html")

from flask import jsonify

@app.route("/todos")
@login_required
def todos():
    """Display all current todos for the logged-in user"""
    user_id = session["user_id"]
    # Retrieve all todos for the logged-in user from the database
    todos = db.execute("SELECT * FROM todos WHERE user_id = ?", user_id)
    return render_template("todos.html", todos=todos)

@app.route("/add_todo", methods=["POST"])
@login_required
def add_todo():
    """Add a new todo item for the logged-in user"""
    user_id = session["user_id"]
    todo_item = request.form.get("todo_item")
    deadline_date = request.form.get("deadline_date")
    # Insert the new todo item into the database
    db.execute("INSERT INTO todos (user_id, todo_item, deadline_date) VALUES (?, ?, ?)", user_id, todo_item, deadline_date)
    flash("Todo item added successfully!", "success")
    return redirect("/todos")

@app.route("/delete_todo/<int:todo_id>", methods=["POST"])
@login_required
def delete_todo(todo_id):
    """Delete a todo item"""
    user_id = session["user_id"]
    # Delete the todo item from the database
    db.execute("DELETE FROM todos WHERE id = ? AND user_id = ?", todo_id, user_id)
    flash("Todo item deleted successfully!", "success")
    return redirect("/todos")


@app.route("/mark_completed/<int:todo_id>", methods=["POST"])
@login_required
def mark_completed(todo_id):
    """Mark a todo item as completed"""
    user_id = session["user_id"]
    # Update the todo item to mark it as completed
    db.execute("UPDATE todos SET completed = 1 WHERE id = ? AND user_id = ?", todo_id, user_id)
    flash("Todo item marked as completed!", "success")
    return redirect("/todos")

@app.route("/list_todos")
@login_required
def list_todos():
    """Display todos based on status (Current, Completed, Overdue)"""
    user_id = session["user_id"]
    # Retrieve current todos for the logged-in user from the database
    current_todos = db.execute("SELECT * FROM todos WHERE user_id = ? AND completed = 0", user_id)
    # Retrieve completed todos for the logged-in user from the database
    completed_todos = db.execute("SELECT * FROM todos WHERE user_id = ? AND completed = 1", user_id)
    # Retrieve overdue todos for the logged-in user from the database
    overdue_todos = db.execute("SELECT * FROM todos WHERE user_id = ? AND completed = 0 AND deadline_date < DATE('now')", user_id)
    # Render the list_todos template with the fetched todos
    return render_template("list_todos.html", current_todos=current_todos, completed_todos=completed_todos, overdue_todos=overdue_todos)


# Add a new route to display current and overdue todos with an option to edit
@app.route("/edit_todo")
@login_required
def edit_todo():
    """Display current and overdue todos with an option to edit"""
    user_id = session["user_id"]
    # Retrieve current and overdue todos for the logged-in user from the database
    current_and_overdue_todos = db.execute("SELECT * FROM todos WHERE user_id = ? AND (completed = 0 OR (completed = 0 AND deadline_date < DATE('now')))", user_id)
    # Render the edit_todo template with the fetched todos
    return render_template("edit_todo.html", todos=current_and_overdue_todos)

@app.route("/update_todo/<int:todo_id>", methods=["GET", "POST"])
@login_required
def update_todo(todo_id):
    """Update a todo item"""
    if request.method == "POST":
        # Get the updated todo item from the form
        updated_todo_item = request.form.get("updated_todo_item")
        updated_deadline_date = request.form.get("updated_deadline_date")
        # Update the todo item in the database
        db.execute("UPDATE todos SET todo_item = ?, deadline_date = ? WHERE id = ?", updated_todo_item, updated_deadline_date, todo_id)
        flash("Todo item updated successfully!", "success")
        return redirect("/edit_todo")
    else:
        # Retrieve the todo item to be updated
        todo = db.execute("SELECT * FROM todos WHERE id = ?", todo_id)
        if not todo:
            return apology("Todo not found", 404)
        return render_template("update_todo.html", todo=todo[0])




if __name__ == "__main__":
    app.run(debug=True)
