# Quiz Master

A comprehensive quiz management system built with Flask that allows administrators to create and manage quizzes while enabling users to take tests and track their performance.

## Features

### User Management
- User registration with email verification
- Role-based access control (Admin/User)
- User profile management
- Admin can manage all users
- Secure password hashing

### Subject and Chapter Management
- Create and manage subjects
- Add chapters to subjects
- Edit and delete subjects/chapters
- Hierarchical organization of content

### Quiz Management
- Create quizzes with:
  - Title and description
  - Date and time settings
  - Duration limit
  - Remarks/instructions
- Add multiple-choice questions
- Edit and delete quizzes
- View quiz statistics (attempts, questions)

### Quiz Taking Experience
- Dynamic subject and chapter filtering
- Real-time countdown timer
- Auto-submit when time expires
- Multiple choice questions
- Immediate score calculation
- View detailed results

### Admin Dashboard
- Overview of recent quizzes
- Manage users, subjects, and chapters
- View quiz records and statistics
- Create and edit quizzes
- Monitor user attempts

### User Dashboard
- View available quizzes
- Filter quizzes by subject and chapter
- See quiz details (duration, date, description)
- Track personal performance
- View attempt history

## Technical Features
- Flask web framework
- SQLAlchemy ORM
- Flask-Login for authentication
- WTForms for form handling
- SQLite database
- Responsive Bootstrap UI
- Dark mode interface

## Database Structure
- User: Stores user information and authentication
- Subject: Manages quiz subjects
- Chapter: Organizes content within subjects
- Quiz: Contains quiz details and settings
- Question: Stores quiz questions
- Option: Manages answer choices
- Result: Tracks user performance

## Security Features
- Password hashing
- Role-based access control
- Session management
- Input validation
- SQL injection prevention

## Usage

### Admin
1. Login as admin
2. Create subjects and chapters
3. Create quizzes with questions
4. Manage users and view statistics

### User
1. Register/Login
2. Browse available quizzes
3. Take quizzes within time limit
4. View results and performance history