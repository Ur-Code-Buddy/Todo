# TodoList Application Documentation

## Overview
This Flask application, named TodoList, is designed to provide users with a platform for managing their todo lists. It offers features such as user registration, login, password change, todo item management, and email verification. The application utilizes a SQLite database for storing user information and todo items, and it integrates Flask-Mail for sending email verification codes during registration. Passwords are securely hashed using the `werkzeug.security` module.

## Dependencies
- **Flask**: A micro web framework for Python.
- **Flask-Mail**: An extension for Flask that adds email sending capabilities.
- **Flask-Session**: An extension for Flask that manages user sessions.
- **CS50**: A library that provides access to a SQLite database.
- **Secrets**: A module for generating secure random tokens.
- **Bootstrap**: A front-end framework for developing responsive and mobile-first websites.
- **Custom CSS**: Additional custom CSS for styling.

## Installation
1. Clone the repository:
   ```bash
   git clone <repository_url>

2. Install dependencies:
   ```bash
    pip install -r requirements.txt

3. **Set up environment variables for email credentials (`my_secret_email` and `my_secret_pass`).**

## Database Schema
The SQLite database (`users.db`) consists of the following tables:

- `users`: Stores user information including username, hashed password, email, and verification status.
- `todos`: Stores todo items associated with each user, along with their completion status and deadline date.

## Functionality
### Routes in `app.py`
- `/change_password`: Allows users to change their passwords.
- `/login`: Handles user login functionality.
- `/logout`: Logs out the current user.
- `/register`: Allows users to register for the application.
- `/verification`: Handles email verification during registration.
- `/todos`: Displays all todos for the logged-in user.
- `/add_todo`: Adds a new todo item for the logged-in user.
- `/delete_todo/int:todo_id`: Deletes a todo item.
- `/mark_completed/int:todo_id`: Marks a todo item as completed.
- `/list_todos`: Displays todos based on their status (current, completed, overdue).
- `/edit_todo`: Displays current and overdue todos with an option to edit.
- `/update_todo/int:todo_id`: Updates a todo item.

### Helper Functions in `helpers.py`
- `apology(message, code=400)`: Renders an apology message with a given status code.
- `login_required`: Decorator function to restrict access to routes for authenticated users only.
- `admin_required(func)`: Decorator function to restrict access to routes for administrators only.
- `is_admin()`: Checks if the current user is an administrator.

## Usage
1. **Run the Flask application:**
   ```bash
   python app.py
2. **Access the application in your web browser at [http://localhost:5000](http://localhost:5000) or online at [attendance.fun](http://attendance.fun).**

## Styling
The application uses Bootstrap for responsive design and layout. Custom CSS is also utilized for additional styling and customization.

## Contributing
Contributions are welcome! Please feel free to submit pull requests or open issues for any improvements or bug fixes.

## License
This project is licensed under the MIT License.


