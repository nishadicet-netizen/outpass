from flask import *
from admin import admin
from public import public
from teacher import teacher
from principal import principal
from hod import hod
from student import student
from warden import warden
from security import security
from api import api


import smtplib
from email.mime.text import MIMEText
from flask_mail import Mail

app=Flask(__name__)

app.secret_key="abacd"
app.register_blueprint(public)
app.register_blueprint(admin,url_prefix='/admin')
app.register_blueprint(teacher,url_prefix='/teacher')
app.register_blueprint(principal,url_prefix='/principal')
app.register_blueprint(hod,url_prefix='/hod')
app.register_blueprint(student,url_prefix='/student')
app.register_blueprint(warden,url_prefix='/warden')
app.register_blueprint(security,url_prefix='/security')
app.register_blueprint(api,url_prefix='/api')

mail=Mail(app)
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'pmgoutpass@gmail.com'
app.config['MAIL_PASSWORD'] = 'izgqjuqneorhokje'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True


app.run(debug=True,port=5676,host="0.0.0.0") 
 