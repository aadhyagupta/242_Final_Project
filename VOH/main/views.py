from flask import Flask, Blueprint
from flask import render_template, request, session, jsonify, redirect, url_for
from flask_socketio import *
from TA import *
from student import *
from VOH.main.forms import RegistrationForm, LoginForm, ChatForm
from authentication import *
from . import main
from .. import app
import os


@main.route('/')
@main.route('/index/')
def main_page():
    return render_template("base.html")

@main.route('/TA/', methods=['GET', 'POST'])
def ta_page():
    print("in index function")
    form = ChatForm()
    if form.validate_on_submit():
        print("submitted form")
        session['netID'] = form.netID.data
        session['chatID'] = form.chatID.data
        print("getting data from validated form ", session['netID'], session['chatID'])
        return redirect(url_for('.chat'))
    elif request.method == 'GET':
        print("IN GET REQUEST METHOD")
        form.netID.data = session.get('netID', '')
        print(form.netID.data)
        form.chatID.data = session.get('chatID', '')
        print(form.chatID.data)
    return render_template('TAView.html', form=form)

@main.route('/chat/')
def chat():
    print("in chat route")
    netID = session.get('netID', '')
    chatID = session.get('chatID', '')
    if netID == '' or chatID == '':
        return redirect(url_for('.TA'))
    return render_template('chat.html', netID=netID, chatID=chatID)




@main.route('/login/')
def login():
    form = LoginForm()
    return render_template("login.html", form = form)


@main.route('/register/')
def register():

    form = RegistrationForm()
    return render_template("register.html", form = form)

@main.route('/register/', methods=["POST"])
def register_user():
    # Get the Form
    form = RegistrationForm(request.form)
    # Validate the Form
    if request.method == "POST" and form.validate():
        # Register TA
        print form
        if form.instructor_type.data == "TA":
            # "Adding TA"
            add_TA(form.username.data, form.password.data, form.name.data, form.net_id.data, form.instructor_type.data)
        elif form.instructor_type.data == "student":
            # "Adding student"
            add_student(form.username.data, form.password.data, form.name.data, form.net_id.data, form.instructor_type.data)
    # Return a new form
    form = RegistrationForm()
    return render_template("register.html", form = form)

@main.route('/authenticate/', methods=["POST"])
def authenticate_login():
    # Get Login Form
    form = LoginForm(request.form)
    # Authenticate USER
    if authenticate_user(form.username.data, form.password.data, form.instructor_type.data):
        # Redirect to main Landing
        return flask.redirect('/landing/'+str(form.username.data))
    # Error! Redirect to Login Page
    return flask.redirect('/login/')

@main.route('/landing/<user>')
def landing_page(user):
    """
    Landing Page after Login
    :param netid: User Name
    :return:
    """
    return render_template("landing.html", netid = user)

@main.route('/instructor/',methods = ["GET","POST"])
def instructor_view():
    message = "No file uploaded"
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = file.filename
            path_of_file = "VOH/" + os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(path_of_file)
            message = "File has been uploaded!"
        else:
            message = "No file to upload!"
    return render_template("instructor.html", message = message)

