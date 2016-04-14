from flask import render_template
from database import student as s
from VOH.main.database.authentication import *
from . import main


@main.route('/student/<net_id>', methods=['GET','POST'])
def student_page(net_id):
    student = s.get_student(net_id)
    return render_template("landing.html", netid = student[0]["name"] ,form = None, login_status = check_login_status()) # Render landing page
