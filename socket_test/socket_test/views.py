from flask import Flask, Blueprint
from flask import render_template, request, session, jsonify
from socket_test import app
from flask_socketio import *
# from authentication import *
from socket_test import socketio
import eventlet
import time
from threading import Thread

eventlet.monkey_patch()
api = Blueprint('api', __name__)
# socketio = SocketIO(app)
thread = None # keeping track of thread


@api.route('/login/')
def login():
    """
    Default Login Page
    :return:
    """
    return render_template("login.html")

@api.route('/register/')
def register():
    return render_template("register.html")

# @api.route('/authenticate/', methods=["POST"])
# def authenticate_login():
#     """
#     Validation of Credentials
#     :return:
#     """
#     username = request.form["username"]
#     password = request.form["password"]
#     print username, password
#     if authenticate_user(username, password):
#         return jsonify(response = "Success")
#     return jsonify(response = 'ADfs')

@app.errorhandler(Exception)
def exception_handler(error):

    return 'ERROR ' + repr(error)