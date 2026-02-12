# Quiz App - Flask & SQLite

A role-based quiz application built with Flask and SQLite database.

## Project Structure

```
quiz_app/
├── app/
│   ├── __init__.py           # Flask app factory
│   ├── models.py             # Database models
│   ├── auth.py               # Authentication routes
│   ├── routes.py             # Main routes (admin, teacher, student)
│   ├── templates/
│   │   ├── base.html         # Base template
│   │   ├── login.html        # Login page
│   │   ├── register.html     # Registration page
│   │   ├── admin/
│   │   │   ├── dashboard.html
│   │   │   └── users.html
│   │   ├── teacher/
│   │   │   ├── dashboard.html
│   │   │   ├── create_quiz.html
│   │   │   └── edit_quiz.html
│   │   └── student/
│   │       ├── dashboard.html
│   │       ├── attempt_quiz.html
│   │       └── result.html
│   └── static/
│       ├── css/
│       └── js/
├── config.py                 # Configuration file
├── run.py                    # Application entry point
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## Features

### Admin Panel
- Predefined login (username: `admin`, password: `admin123`)
- View dashboard with statistics
- Manage users (view and delete)

### Teacher Features
- Create quizzes
- Add questions with multiple options
- View quiz details and results

### Student Features
- View available quizzes
- Attempt quizzes
- View detailed results and score

### Database Models
- **User**: stores user information with roles (admin, teacher, student)
- **Quiz**: quiz information created by teachers
- **Question**: multiple choice questions for each quiz
- **Result**: student quiz submission and scores
- **Answer**: student's answers for each question

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd quiz_app
```

2. Create virtual environment:
```bash
python -m venv venv
venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
python run.py
```

The app will run on `http://localhost:5000`

## Default Login Credentials

- **Admin**: 
  - Username: `admin`
  - Password: `admin123`

## Usage

1. **Admin**: Login with predefined credentials to manage users
2. **Teacher**: Register as teacher, create quizzes and add questions
3. **Student**: Register as student and attempt quizzes

## Database

The app uses SQLite database which is automatically created on first run:
- **Database file**: `quiz_app.db`
- Located in the root directory

## Technologies Used

- **Framework**: Flask 2.3.3
- **Database**: SQLite3
- **ORM**: Flask-SQLAlchemy
- **Authentication**: Flask-Login
- **Frontend**: Bootstrap 5

## License

MIT License
