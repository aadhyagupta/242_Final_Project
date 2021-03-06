from database import TA
from flask.ext.wtf import Form as form
from database import student
from wtforms import Form, RadioField, PasswordField, validators, HiddenField
from wtforms.fields import StringField, SubmitField
from wtforms.validators import DataRequired

from VOH.main.database.authentication import *


class RegistrationForm(Form):
    """
    A registration form which allows the user to add name, username, net_id and password
    where there are conditions to check that the repeated password is the same as the original
    password
    """
    name = StringField('Name', [validators.Length(min=2, max=25)])
    net_id = StringField('Net ID', [validators.Length(min=2, max=35)])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')  # makes sure that passwords match
    ])
    confirm = PasswordField('Repeat Password')
    instructor_type = RadioField('Register as', choices=[('TA', 'Teaching Assistant'), ('student', 'Student')], default='student')

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        """
        Validation for Registration Forms
        Checks for type of user and checks if "net id" has already been registered
        Performs sanity checks as well (same passwords)

        If There are errors, appends errors to the form
        :return: True if no Errors else False
        """
        # Authenticate USER
        if Form.validate(self) == False:
            return False
        if self.instructor_type.data == "TA":
            if TA.check_in_ta_list(self.net_id.data) == False:
                self.net_id.errors.append("This Net ID is not a valid TA")
            elif TA.check_ta_registration(self.net_id.data) == True:
                self.net_id.errors.append("This Net ID has already been registered")
            else:
                return True
        elif self.instructor_type.data == "student":
            if student.check_in_student_list(self.net_id.data) == False:
                self.net_id.errors.append("This NETID is not a valid Student")
            elif student.check_student_registration(self.net_id.data) == True:
                self.net_id.errors.append("This Net ID has already been registered")
            else:
                return True

        return False


class LoginForm(Form):
    """
    A login form which allows a user to login depending upon whether he is a TA or a student
    """
    instructor_type = RadioField('Login as', choices=[('TA', 'Teaching Assistant'), ('student', 'Student')], default='student')
    net_id = StringField('Net ID')
    password = PasswordField('Password')

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        """
        Validation for Login
        :return:
        """
        Form.validate(self)
        if authenticate_user(self.net_id.data, self.password.data, self.instructor_type.data):
            return True
        self.password.errors.append('Password and Username do not match')
        return False


class TARating(form):
    """
    Create a TA rating form which allows you to rate a TA on a scale from 1 to 5 and has two hidden fields which store
    the rating for and by
    """
    rating = RadioField('Rate TA', choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')],
                                 default='student')
    rating_for = HiddenField('Default TA')
    rating_by = HiddenField('Default Student')


class StudentRating(form):
    """
    Create a Student rating form which allows you to rate a student on a scale from 1 to 5 and has two hidden fields which store
    the rating for and by
    """
    rating = RadioField('Rate Student',choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')],
                                 default='student')
    rating_for = HiddenField('Default Student')
    rating_by = HiddenField('Default TA')
