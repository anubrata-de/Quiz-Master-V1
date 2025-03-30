from flask import Flask, render_template, redirect, url_for, session, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, DateField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Email, ValidationError, Optional, NumberRange
from functools import wraps
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import os
from datetime import date
from models import db, User, Quiz, Question, Option, Result
from werkzeug.security import generate_password_hash

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

instance_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "instance")
if not os.path.exists(instance_dir):
    os.makedirs(instance_dir)

app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(instance_dir, 'database.sqlite3')
db.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class RegisterForm(FlaskForm):
    name = StringField("Full Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired()])
    date_of_birth = DateField("Date of Birth", validators=[DataRequired()])
    submit = SubmitField("Register")

    def validate_email(self, field):
        user = User.query.filter_by(email=field.data).first()
        if user:
            raise ValidationError('This email is already registered. Please use a different email or login.')

    def validate(self, extra_validators=None):
        if not super().validate():
            return False
        if self.password.data != self.confirm_password.data:
            self.confirm_password.errors.append("Passwords do not match")
            return False
        return True

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")

class UserEditForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    role = SelectField("Role", choices=[('user', 'User'), ('admin', 'Admin')], validators=[DataRequired()])
    password = PasswordField("New Password", validators=[Optional()])
    submit = SubmitField("Update")

    def validate_email(self, field):
        user = User.query.filter(User.email == field.data, User.id != self.user_id).first()
        if user:
            raise ValidationError('Email already taken')

    def validate(self, extra_validators=None):
        if not super().validate():
            return False
        if self.password.data and len(self.password.data) < 6:
            self.password.errors.append("Password must be at least 6 characters long")
            return False
        return True

class QuizForm(FlaskForm):
    title = StringField("Quiz Title", validators=[DataRequired()])
    description = TextAreaField("Description", validators=[Optional()])
    time_limit = IntegerField("Time Limit (minutes)", validators=[DataRequired(), NumberRange(min=1, max=120)], default=30)
    submit = SubmitField("Create Quiz")

class QuestionForm(FlaskForm):
    text = StringField("Question Text", validators=[DataRequired()])
    option1 = StringField("Option 1", validators=[DataRequired()])
    option2 = StringField("Option 2", validators=[DataRequired()])
    option3 = StringField("Option 3", validators=[DataRequired()])
    option4 = StringField("Option 4", validators=[DataRequired()])
    correct_option = SelectField("Correct Option", choices=[('1', 'Option 1'), ('2', 'Option 2'), ('3', 'Option 3'), ('4', 'Option 4')], validators=[DataRequired()])
    submit = SubmitField("Add Question")

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            flash("Unauthorized access!", "danger")
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    form = RegisterForm()
    if form.validate_on_submit():
        try:
            existing_user = User.query.filter_by(email=form.email.data).first()
            if existing_user:
                flash("Email already registered. Please use a different email or login.", "danger")
                return redirect(url_for('register'))

            new_user = User(
                name=form.name.data,
                email=form.email.data,
                password_hash=generate_password_hash(form.password.data),
                dob=form.date_of_birth.data,
                role='user'
            )
            db.session.add(new_user)
            db.session.commit()
            flash("Registration successful! Please log in.", "success")
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash(f"An error occurred: {str(e)}", "danger")
    elif form.errors:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"{field.title()}: {error}", "danger")
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.verify_password(form.password.data):
            login_user(user)
            flash("Login successful!", "success")
            return redirect(url_for('admin_dashboard' if user.role == 'admin' else 'dashboard'))
        flash("Invalid email or password", "danger")
    return render_template('login.html', form=form)

@app.route('/dashboard')
@login_required
def dashboard():
    quizzes = Quiz.query.all()
    return render_template('user_dashboard.html', user=current_user, tests=quizzes)

@app.route('/attempt_test/<int:test_id>', methods=['GET'])
@login_required
def attempt_test(test_id):
    quiz = Quiz.query.get_or_404(test_id)
    questions = Question.query.filter_by(quiz_id=test_id).all()

    quiz_data = {
        "id": quiz.id,
        "title": quiz.title,
        "questions": [{
            "id": question.id,
            "text": question.text,
            "options": [{"id": opt.id, "text": opt.option_text} for opt in Option.query.filter_by(question_id=question.id).all()]
        } for question in questions]
    }

    return render_template("attempt_test.html", test=quiz_data, questions=quiz_data["questions"])

@app.route('/submit_test/<int:test_id>', methods=['POST'])
@login_required
def submit_test(test_id):
    questions = Question.query.filter_by(quiz_id=test_id).all()
    total_questions = len(questions)
    score = 0
    
    print(f"Total questions in test: {total_questions}")
    
    for question in questions:
        selected_option_id = request.form.get(f"question_{question.id}")
        print(f"\nProcessing Question ID: {question.id}")
        print(f"Selected Option ID: {selected_option_id}")
        print(f"Correct Option ID: {question.correct_option}")
        
        if selected_option_id:
            selected_option_id = int(selected_option_id)
            selected_option = Option.query.get(selected_option_id)
            if selected_option:
                print(f"Selected Option Text: {selected_option.option_text}")
                correct_option = Option.query.get(question.correct_option)
                if correct_option:
                    print(f"Correct Option Text: {correct_option.option_text}")
                    if selected_option.id == correct_option.id:
                        print(f"Answer is correct! Selected: {selected_option.id}, Correct: {correct_option.id}")
                        score += 1
                    else:
                        print(f"Answer is wrong! Selected: {selected_option.id}, Correct: {correct_option.id}")
                else:
                    print("Correct option not found!")
            else:
                print("Selected option not found!")
        else:
            print("No option selected!")

    try:
        percentage = (score / total_questions * 100) if total_questions > 0 else 0
        
        result = Result(
            user_id=current_user.id,
            quiz_id=test_id,
            score=score,
            total_questions=total_questions,
            percentage=round(percentage, 2)
        )
        db.session.add(result)
        db.session.commit()
        
        print(f"\nFinal Score: {score}/{total_questions}")
        print(f"Percentage: {percentage}%")
        
        flash(f"Quiz submitted successfully! Your score: {score}/{total_questions} ({percentage}%)", "success")
        return redirect(url_for('view_score', test_id=test_id))
    except Exception as e:
        db.session.rollback()
        flash(f"Error saving result: {str(e)}", "danger")
        return redirect(url_for('dashboard'))

@app.route('/view_score/<int:test_id>', methods=['GET'])
@login_required
def view_score(test_id):
    result = Result.query.filter_by(
        user_id=current_user.id,
        quiz_id=test_id
    ).order_by(Result.created_at.desc()).first_or_404()
    
    print(f"\nView Score Debug:")
    print(f"Result ID: {result.id}")
    print(f"User ID: {result.user_id}")
    print(f"Quiz ID: {result.quiz_id}")
    print(f"Score: {result.score}")
    print(f"Total Questions: {result.total_questions}")
    print(f"Percentage: {result.percentage}")
    print(f"Created At: {result.created_at}")
    
    return render_template('view_score.html', 
                         score=result.score, 
                         total_questions=result.total_questions,
                         percentage=result.percentage)

@app.route('/admin_dashboard')
@admin_required
def admin_dashboard():
    recent_tests = db.session.query(
        Quiz,
        db.func.count(Question.id).label('question_count'),
        db.func.count(Result.id).label('attempt_count')
    ).outerjoin(Question, Quiz.id == Question.quiz_id)\
     .outerjoin(Result, Quiz.id == Result.quiz_id)\
     .group_by(Quiz.id, Quiz.title)\
     .order_by(Quiz.id.desc())\
     .limit(5)\
     .all()

    formatted_tests = [{
        'id': quiz.id,
        'title': quiz.title,
        'question_count': question_count,
        'attempt_count': attempt_count
    } for quiz, question_count, attempt_count in recent_tests]

    return render_template('admin_dashboard.html', 
                         admin=current_user.name, 
                         recent_tests=formatted_tests)

@app.route('/admin/manage_users')
@admin_required
def manage_users():
    return render_template('manage_users.html', users=User.query.all())

@app.route('/admin/edit_test/<int:test_id>', methods=['GET', 'POST'])
@admin_required
def edit_test(test_id):
    quiz = Quiz.query.get_or_404(test_id)
    form = QuizForm(obj=quiz)
    
    if form.validate_on_submit():
        try:
            quiz.title = form.title.data
            quiz.description = form.description.data
            quiz.time_limit = form.time_limit.data
            db.session.commit()
            flash("Test updated successfully!", "success")
            return redirect(url_for('manage_tests'))
        except Exception as e:
            db.session.rollback()
            flash(f"Error updating test: {str(e)}", "danger")
    return render_template('edit_test.html', form=form, test=quiz)

@app.route('/admin/edit_user/<int:user_id>', methods=['GET', 'POST'])
@admin_required
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    form = UserEditForm()
    form.user_id = user_id

    if request.method == 'GET':
        form.name.data = user.name
        form.email.data = user.email
        form.role.data = user.role

    if form.validate_on_submit():
        try:
            user.name = form.name.data
            user.email = form.email.data
            user.role = form.role.data
            if form.password.data:
                user.password_hash = generate_password_hash(form.password.data)
            db.session.commit()
            flash("User updated successfully!", "success")
            return redirect(url_for('manage_users'))
        except Exception as e:
            db.session.rollback()
            flash(f"Error updating user: {str(e)}", "danger")
    return render_template('edit_user.html', form=form, user=user)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "success")
    return redirect(url_for('login'))

@app.route('/admin/create_test', methods=['GET', 'POST'])
@admin_required
def create_test():
    form = QuizForm()
    if form.validate_on_submit():
        try:
            quiz = Quiz(
                title=form.title.data,
                description=form.description.data
            )
            db.session.add(quiz)
            db.session.commit()
            flash("Quiz created successfully! Now add questions.", "success")
            return redirect(url_for('add_questions', quiz_id=quiz.id))
        except Exception as e:
            db.session.rollback()
            flash(f"Error creating quiz: {str(e)}", "danger")
    return render_template('create_test.html', form=form)

@app.route('/admin/add_questions/<int:quiz_id>', methods=['GET', 'POST'])
@admin_required
def add_questions(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    form = QuestionForm()
    
    if form.validate_on_submit():
        try:
            options = [
                Option(option_text=form.option1.data),
                Option(option_text=form.option2.data),
                Option(option_text=form.option3.data),
                Option(option_text=form.option4.data)
            ]
            db.session.add_all(options)
            db.session.flush()

            correct_option_index = int(form.correct_option.data) - 1
            correct_option_id = options[correct_option_index].id

            question = Question(
                quiz_id=quiz_id,
                text=form.text.data,
                correct_option=correct_option_id
            )
            db.session.add(question)
            db.session.flush()

            for option in options:
                option.question_id = question.id
            
            print(f"Question ID: {question.id}")
            print(f"Correct Option Index: {correct_option_index}")
            print(f"Correct Option ID: {correct_option_id}")
            print(f"Correct Option Text: {options[correct_option_index].option_text}")
            
            db.session.commit()
            flash("Question added successfully!", "success")
            return redirect(url_for('add_questions', quiz_id=quiz_id))
        except Exception as e:
            db.session.rollback()
            flash(f"Error adding question: {str(e)}", "danger")
    return render_template('add_questions.html', form=form, quiz_id=quiz_id)

@app.route('/admin/manage_tests')
@admin_required
def manage_tests():
    tests = db.session.query(
        Quiz,
        db.func.count(Question.id).label('question_count'),
        db.func.count(Result.id).label('attempt_count')
    ).outerjoin(Question, Quiz.id == Question.quiz_id)\
     .outerjoin(Result, Quiz.id == Result.quiz_id)\
     .group_by(Quiz.id, Quiz.title)\
     .all()
    
    formatted_tests = [{
        'id': quiz.id,
        'title': quiz.title,
        'question_count': question_count,
        'attempt_count': attempt_count
    } for quiz, question_count, attempt_count in tests]
    
    return render_template('manage_tests.html', tests=formatted_tests)

@app.route('/admin/delete_test/<int:test_id>')
@admin_required
def delete_test(test_id):
    try:
        quiz = Quiz.query.get_or_404(test_id)
        db.session.delete(quiz)
        db.session.commit()
        flash("Test deleted successfully!", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error deleting test: {str(e)}", "danger")
    return redirect(url_for('manage_tests'))

@app.route('/admin/quiz_records')
@admin_required
def quiz_records():
    records = db.session.query(
        User.name.label('user_name'),
        Quiz.title.label('quiz_title'),
        Result.score,
        Result.total_questions,
        Result.percentage,
        Result.created_at
    ).join(User, Result.user_id == User.id)\
     .join(Quiz, Result.quiz_id == Quiz.id)\
     .order_by(Result.created_at.desc())\
     .all()
    
    formatted_records = [{
        'user_name': record.user_name,
        'quiz_title': record.quiz_title,
        'score': record.score,
        'total_questions': record.total_questions,
        'percentage': record.percentage,
        'created_at': record.created_at
    } for record in records]
    
    return render_template('quiz_records.html', records=formatted_records)

@app.route('/my_results')
@login_required
def my_results():
    results = db.session.query(
        Quiz.title.label('quiz_title'),
        Result.score,
        Result.total_questions,
        Result.percentage,
        Result.created_at
    ).join(Quiz, Result.quiz_id == Quiz.id)\
     .filter(Result.user_id == current_user.id)\
     .order_by(Result.created_at.desc())\
     .all()
    
    formatted_results = [{
        'quiz_title': result.quiz_title,
        'score': result.score,
        'total_questions': result.total_questions,
        'percentage': result.percentage,
        'created_at': result.created_at
    } for result in results]
    
    return render_template('my_results.html', results=formatted_results)

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)

@app.route('/admin/delete_user/<int:user_id>')
@admin_required
def delete_user(user_id):
    try:
        user = User.query.get_or_404(user_id)
        if user.role == 'admin':
            flash("Cannot delete admin users!", "danger")
            return redirect(url_for('manage_users'))
        db.session.delete(user)
        db.session.commit()
        flash("User deleted successfully!", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error deleting user: {str(e)}", "danger")
    return redirect(url_for('manage_users'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
