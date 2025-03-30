from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, DateField, TextAreaField, IntegerField, DateTimeField, BooleanField
from wtforms.validators import DataRequired, Email, ValidationError, Optional, NumberRange, Length

class SubjectForm(FlaskForm):
    name = StringField("Subject Name", validators=[DataRequired(), Length(min=3, max=255)])
    description = TextAreaField("Description", validators=[Optional()])
    submit = SubmitField("Create Subject")

class ChapterForm(FlaskForm):
    subject_id = SelectField("Subject", coerce=int, validators=[DataRequired()])
    name = StringField("Chapter Name", validators=[DataRequired(), Length(min=3, max=255)])
    description = TextAreaField("Description", validators=[Optional()])
    submit = SubmitField("Create Chapter")

    def __init__(self, *args, **kwargs):
        super(ChapterForm, self).__init__(*args, **kwargs)
        from models import Subject
        self.subject_id.choices = [(s.id, s.name) for s in Subject.query.order_by(Subject.name).all()]

class QuizForm(FlaskForm):
    chapter_id = SelectField("Chapter", coerce=int, validators=[DataRequired()])
    title = StringField("Quiz Title", validators=[DataRequired(), Length(min=3, max=255)])
    description = TextAreaField("Description", validators=[Optional()])
    date_of_quiz = DateTimeField("Quiz Date", format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    time_duration = StringField("Duration (HH:MM)", validators=[DataRequired(), Length(min=5, max=5)])
    remarks = TextAreaField("Remarks", validators=[Optional()])
    submit = SubmitField("Create Quiz")

    def __init__(self, *args, **kwargs):
        super(QuizForm, self).__init__(*args, **kwargs)
        from models import Chapter
        self.chapter_id.choices = [(c.id, f"{c.subject.name} - {c.name}") for c in Chapter.query.order_by(Chapter.name).all()]

class QuestionForm(FlaskForm):
    text = TextAreaField("Question Text", validators=[DataRequired()])
    option1 = StringField("Option 1", validators=[DataRequired()])
    option2 = StringField("Option 2", validators=[DataRequired()])
    option3 = StringField("Option 3", validators=[DataRequired()])
    option4 = StringField("Option 4", validators=[DataRequired()])
    correct_option = SelectField("Correct Option", choices=[('1', 'Option 1'), ('2', 'Option 2'), ('3', 'Option 3'), ('4', 'Option 4')], validators=[DataRequired()])
    marks = IntegerField("Marks", validators=[DataRequired(), NumberRange(min=1, max=10)], default=1)
    submit = SubmitField("Add Question")

class SearchForm(FlaskForm):
    query = StringField("Search", validators=[DataRequired()])
    search_type = SelectField("Search Type", choices=[
        ('subject', 'Subjects'),
        ('chapter', 'Chapters'),
        ('quiz', 'Quizzes'),
        ('user', 'Users')
    ], validators=[DataRequired()])
    submit = SubmitField("Search") 