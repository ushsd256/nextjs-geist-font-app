from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, RadioField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from app import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    role = RadioField('Role', choices=[
        ('admin', 'Admin'),
        ('principal', 'Principal'),
        ('teacher', 'Teacher')
    ], default='teacher')
    submit = SubmitField('Login')

class AdminSignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=6, message='Password must be at least 6 characters long')
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password', message='Passwords must match')
    ])
    admin_code = StringField('Admin Code', validators=[DataRequired()])
    submit = SubmitField('Sign Up')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already exists')

    def validate_admin_code(self, field):
        if field.data != "3075":  # Admin code from requirements
            raise ValidationError('Invalid admin code')

class ForgotPasswordForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    admin_code = StringField('Admin Code', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[
        DataRequired(),
        Length(min=6, message='Password must be at least 6 characters long')
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('new_password', message='Passwords must match')
    ])
    submit = SubmitField('Reset Password')

    def validate_admin_code(self, field):
        if field.data != "3075":
            raise ValidationError('Invalid admin code')

    def validate_username(self, field):
        user = User.query.filter_by(username=field.data).first()
        if not user:
            raise ValidationError('Username does not exist')
