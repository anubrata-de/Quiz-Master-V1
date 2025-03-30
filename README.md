# Quiz Master

A modern web-based quiz application built with Flask that allows users to take quizzes and administrators to manage them.

## Features

### For Users
- User registration and authentication
- View available quizzes
- Take quizzes with multiple-choice questions
- View quiz results and performance history
- Track progress with detailed statistics
- Responsive design for all devices

### For Administrators
- Create and manage quizzes
- Add/delete questions
- View quiz statistics and user performance
- Manage user accounts
- Monitor quiz attempts

## Tech Stack

- **Backend**: Python/Flask
- **Database**: SQLite with SQLAlchemy ORM
- **Frontend**: HTML5, CSS3, Bootstrap 5
- **Authentication**: Flask-Login
- **Forms**: Flask-WTF
- **Styling**: Custom CSS with dark theme

## Default Admin Account

- Email: admin@example.com
- Password: admin123

## Project Structure

```
quiz-master/
├── app.py              # Main application file
├── models.py           # Database models
├── forms.py            # Form definitions
├── init_db.py          # Database initialization
├── requirements.txt    # Project dependencies
├── instance/          # Instance-specific files
│   └── database.sqlite3
└── templates/         # HTML templates
    ├── base.html
    ├── index.html
    ├── login.html
    ├── register.html
    ├── dashboard.html
    ├── profile.html
    ├── quiz.html
    ├── view_score.html
    └── ... (other templates)
```

## Database Models

### User
- Basic user information (name, email, password)
- Role-based access (admin/user)
- Date of birth and account creation date

### Quiz
- Title and description
- Time limit
- Questions and options
- Results tracking

### Question
- Question text
- Multiple choice options
- Correct answer

### Result
- User's quiz attempts
- Score tracking
- Performance metrics