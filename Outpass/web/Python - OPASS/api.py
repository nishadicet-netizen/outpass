from flask import *
from database import *
import demjson

import uuid
import qrcode
import random

import os
from flask import Flask, jsonify

from flask.globals import request, session
from werkzeug.utils import secure_filename

import smtplib
from email.mime.text import MIMEText
from flask_mail import Mail

api=Blueprint("api",__name__)




@api.route('/login',methods=['get','post'])
def login():
	data={}
	username=request.args['username']
	password=request.args['password']
	
	q="select * from login where username='%s' and password='%s'" %(username,password)
	res=select(q)


	if res:
	
		data['status']="success"
		data['method']="login"
		data['data']=res
		
	else:
		data['status']="failed"
		data['method']="login"
	return str(data)


# @api.route('/register',methods=['get','post'])
# def register():
# 	data={}
# 	first_name=request.args['fname']
# 	last_name=request.args['lname']
# 	gender=request.args['gender']

# 	group=request.args['group']
# 	age=request.args['age']

# 	pincode=request.args['pin']
# 	phone=request.args['phone']
# 	email=request.args['email']
# 	username=request.args['uname']
# 	password=request.args['pass']
# 	q="insert into login values(NULL,'%s','%s','donor')"%(username,password)
# 	id=insert(q)
# 	q="insert into donors values (NULL,'%s','%s','%s','%s','%s','%s','%s','%s','%s')"%(id,first_name,last_name,group,gender,age,pincode,phone,email)
# 	iid=insert(q)
# 	if iid:
# 		data['status']="success"
# 		data['method']="register"
		
# 	else:
# 		data['status']="failed"
# 		data['method']="register"
# 	return str(data)




@api.route('/TeacherManageStudents',methods=['get','post'])
def TeacherManageStudents():
	data={}
	# q="SELECT * FROM `students` INNER JOIN `batches` USING(`batch_id`) INNER JOIN `courses` courses ON(`students`.`course_id`=`courses`.`course_id`)"
	q="SELECT *,CONCAT(`students`.`first_name`,' ',`students`.`last_name`) AS sname,students.email as emails,students.phone as phones FROM `students` INNER JOIN `batches` USING(`batch_id`) INNER JOIN `courses` ON(`students`.`course_id`=`courses`.`course_id`) INNER JOIN `department` USING(`dept_id`) INNER JOIN `hod` USING(`dept_id`) INNER JOIN `teachers` USING(`hod_id`)"
	print(q)
	res=select(q)
	if res:
		data['status']="success"
		data['method']="TeacherManageStudents"
		data['data']=res
		
	else:
		data['status']="failed"
		data['method']="TeacherManageStudents"
	return str(data)

@api.route('/teacher_send_leave_request',methods=['get','post'])
def teacher_send_leave_request():
	data={}
	login_id=request.args['login_id']
	date=request.args['leave_date']
	duration=request.args['nodays']
	reason=request.args['reason']
	leave_type=request.args['leave_type']
	q="insert into leave_requests values(NULL,'%s','teacher','%s','%s','%s',now(),'pending','pending','%s')"%(login_id,reason,date,duration,leave_type)
	id=insert(q)
	if id:
		data['status']="success"
		data['method']="teacher_send_leave_request"
		
	else:
		data['status']="failed"
		data['method']="teacher_send_leave_request"
	return str(data)




@api.route('/teacher_view_leave_request',methods=['get','post'])
def teacher_view_leave_request():
	data={}
	login_id=request.args['login_id']
	q="select * from leave_requests where requested_id='%s' order by date_time desc"%(login_id)
	res=select(q)

	if res:
		data['status']="success"
		data['method']="teacher_view_leave_request"
		data['data']=res
		
	else:
		data['status']="failed"
		data['method']="teacher_view_leave_request"
	return str(data)



@api.route('/teacher_view_leave_request_from_students',methods=['get','post'])
def teacher_view_leave_request_from_students():
	data={}
	
	# q="select * from leave_requests  join students on(students.login_id=leave_requests.requested_id) inner join courses using(course_id) inner join batches using(batch_id) where type='student'"
	q="SELECT *,CONCAT(`students`.`first_name`,' ',`students`.`last_name`) AS sname FROM `students` INNER JOIN `batches` USING(`batch_id`) INNER JOIN `courses` ON(`students`.`course_id`=`courses`.`course_id`) INNER JOIN `department` USING(`dept_id`) INNER JOIN `hod` USING(`dept_id`) INNER JOIN `teachers` USING(`hod_id`) INNER JOIN `leave_requests` ON `leave_requests`.`requested_id`=`students`.`login_id` WHERE `leave_requests`.`type`='student' GROUP BY `leave_requests`.`leave_id` ORDER BY `leave_id` DESC"
	res=select(q)
	print(q)

	if res:
		data['status']="success"
		data['method']="teacher_view_leave_request_from_students"
		data['data']=res
		
	else:
		data['status']="failed"
		data['method']="teacher_view_leave_request_from_students"
	return str(data)



@api.route('/teacher_approve_leave_request_from_students',methods=['get','post'])
def teacher_approve_leave_request_from_students():
	data={}
	leave_id=request.args['leave_id']

	path = "static/qrcode/" + str(uuid.uuid4()) + ".png"
	img = qrcode.make(leave_id)
	img.save(path)
	q="update leave_requests set status='teacher approved',qr='%s' where leave_id='%s'"%(path,leave_id)
	id=update(q)
	


	if id:
		data['status']="success"
		data['method']="teacher_approve_leave_request_from_students"

		
	else:
		data['status']="failed"
		data['method']="teacher_approve_leave_request_from_students"
	return str(data)





@api.route('/teacher_reject_leave_request_from_students',methods=['get','post'])
def teacher_reject_leave_request_from_students():
	data={}
	leave_id=request.args['leave_id']
	q="update leave_requests set status='rejected' where leave_id='%s'"%(leave_id)
	id=update(q)
	


	if id:
		data['status']="success"
		data['method']="teacher_reject_leave_request_from_students"

		
	else:
		data['status']="failed"
		data['method']="teacher_reject_leave_request_from_students"

	return str(data)





@api.route('/teacher_view_outpass_request_from_students',methods=['get','post'])
def teacher_view_outpass_request_from_students():
	data={}
	
	# q="select * from out_passes  join students on(students.login_id=out_passes.requested_id) inner join courses using(course_id) inner join batches using(batch_id) where type='student'"
	q="SELECT *,CONCAT(`students`.`first_name`,' ',`students`.`last_name`) AS sname FROM `students` INNER JOIN `batches` USING(`batch_id`) INNER JOIN `courses` ON(`students`.`course_id`=`courses`.`course_id`) INNER JOIN `department` USING(`dept_id`) INNER JOIN `hod` USING(`dept_id`) INNER JOIN `teachers` USING(`hod_id`) INNER JOIN `out_passes` ON `out_passes`.`requested_id`=`students`.`login_id` WHERE `out_passes`.`type`='student' GROUP BY `out_passes`.`pass_id` ORDER BY `pass_id` DESC"
	res=select(q)

	if res:
		data['status']="success"
		data['method']="teacher_view_outpass_request_from_students"
		data['data']=res
		
	else:
		data['status']="failed"
		data['method']="teacher_view_outpass_request_from_students"
	return str(data)


@api.route('/teacher_approve_outpass_request_from_students',methods=['get','post'])
def teacher_approve_outpass_request_from_students():
	data={}
	pass_id=request.args['pass_id']

	path = "static/qrcode/" + str(uuid.uuid4()) + ".png"
	img = qrcode.make(pass_id)
	img.save(path)
	q="update out_passes set status='accepted',qr='%s' where pass_id='%s'"%(path,pass_id)
	id=update(q)
	


	if id:
		data['status']="success"
		data['method']="teacher_approve_outpass_request_from_students"

		
	else:
		data['status']="failed"
		data['method']="teacher_approve_outpass_request_from_students"
	return str(data)





@api.route('/teacher_reject_outpass_request_from_students',methods=['get','post'])
def teacher_reject_outpass_request_from_students():
	data={}
	pass_id=request.args['pass_id']


	q="update out_passes set status='rejecetd' where pass_id='%s'"%(pass_id)
	id=update(q)
	


	if id:
		data['status']="success"
		data['method']="teacher_approve_outpass_request_from_students"

		
	else:
		data['status']="failed"
		data['method']="teacher_approve_outpass_request_from_students"
	return str(data)




@api.route('/teacher_send_outpass_request',methods=['get','post'])
def teacher_send_outpass_request():
	data={}
	login_id=request.args['login_id']
	date=request.args['date']
	time=request.args['time']
	reason=request.args['reason']
	q="select * from out_passes where request_date=curdate() and type='teacher' and request_time='%s' and reason='%s' and requested_id='%s'"%(time,reason,login_id)
	res=select(q)
	if res:
		data['status']="failed"
		pass
	else:
		q="insert into out_passes values(NULL,'%s','teacher',curdate(),'%s','%s','pending','pending','%s')"%(login_id,time,reason,date)
		id=insert(q)
		if id:
			data['status']="success"
			data['method']="teacher_send_outpass_request"
		
		else:
			data['status']="failed"
	data['method']="teacher_send_outpass_request"
	return str(data)







@api.route('/teacher_view_outpass_request',methods=['get','post'])
def teacher_view_outpass_request():
	data={}
	login_id=request.args['login_id']
	q="select * from out_passes where requested_id='%s'"%(login_id)
	res=select(q)

	if res:
		data['status']="success"
		data['method']="teacher_view_outpass_request"
		data['data']=res
		
	else:
		data['status']="failed"
		data['method']="teacher_view_outpass_request"
	return str(data)



	

@api.route('/view_profile',methods=['get','post'])
def view_profile():
	data={}
	login_id=request.args['login_id']
	q="select * from students inner join courses using(course_id) inner join batches using(batch_id) where login_id='%s'"%(login_id)
	res=select(q)

	if res:
		data['status']="success"
		data['method']="view_profile"
		data['data']=res
		
	else:
		data['status']="failed"
		data['method']="view_profile"
	return str(data)





@api.route('/student_send_leave_request',methods=['get','post'])
def student_send_leave_request():
	data={}
	login_id=request.args['login_id']
	date=request.args['leave_date']
	duration=request.args['nodays']
	reason=request.args['reason']
	q="insert into leave_requests values(NULL,'%s','student','%s','%s','%s',now(),'pending','pending','')"%(login_id,reason,date,duration)
	id=insert(q)
	if id:
		data['status']="success"
		data['method']="student_send_leave_request"
		
	else:
		data['status']="failed"
		data['method']="student_send_leave_request"
	return str(data)




@api.route('/student_view_leave_request',methods=['get','post'])
def student_view_leave_request():
	data={}
	login_id=request.args['login_id']
	q="select * from leave_requests where requested_id='%s'"%(login_id)
	res=select(q)

	if res:
		data['status']="success"
		data['method']="student_view_leave_request"
		data['data']=res
		
	else:
		data['status']="failed"
		data['method']="student_view_leave_request"
	return str(data)




@api.route('/student_send_outpass_request',methods=['get','post'])
def student_send_outpass_request():
	data={}
	login_id=request.args['login_id']
	date=request.args['date']
	time=request.args['time']
	# time1=request.args['time1']
	reason=request.args['reason']
	q="insert into out_passes values(NULL,'%s','student','%s','%s','%s','pending','pending','pending')"%(login_id,date,time,reason)
	id=insert(q)
	if id:
		data['status']="success"
		data['method']="student_send_outpass_request"
		
	else:
		data['status']="failed"
		data['method']="student_send_outpass_request"
	return str(data)










@api.route('/student_view_outpass_request',methods=['get','post'])
def student_view_outpass_request():
	data={}
	login_id=request.args['login_id']
	q="select * from out_passes where requested_id='%s'"%(login_id)
	res=select(q)

	if res:
		data['status']="success"
		data['method']="student_view_outpass_request"
		data['data']=res
		
	else:
		data['status']="failed"
		data['method']="student_view_outpass_request"
	return str(data)


	


@api.route('/view_qr_code',methods=['get','post'])
def view_qr_code():
	data={}
	outpass_id=request.args['outpass_id']


	q="select * from out_passes where pass_id='%s'"%(outpass_id)
	res1=select(q)
	print(q)
	if res1:
		if res1[0]['type']=='student':
			q="select * from out_passes join students on(students.login_id=out_passes.requested_id) inner join courses using(course_id) inner join batches using(batch_id) where pass_id='%s'"%(outpass_id)
			res=select(q)

			if res:
				data['status']="success"
				data['method']="view_qr_code"
				data['data']=res
			else:
				data['status']="failed"
				data['method']="view_qr_code"
			
		else:
			q="select * from out_passes join teachers on(teachers.login_id=out_passes.requested_id)  where pass_id='%s'"%(outpass_id)
			res=select(q)

			if res:
				data['status']="success"
				data['method']="view_qr_code_for_teacher"
				data['data']=res
				
			else:
				data['status']="failed"
				data['method']="view_qr_code_for_teacher"

	return str(data)




@api.route('/students',methods=['get','post'])
def students():
	data={}


	q="SELECT *,concat(first_name,'',last_name) as name FROM `students`"
	print(q)
	# q="select *,concat(first_name,'',last_name) as name from students"
	res=select(q)

	if res:
		data['status']="success"
		data['method']="students"
		data['data']=res
		
	else:
		data['status']="failed"
		data['method']="students"
	return str(data)



@api.route('/guard_send_late',methods=['get','post'])
def guard_send_late():
	data={}
	student_id=request.args['student_id']
	late=request.args['late']
	q="insert into  late_coming values(NULL,'%s',now(),'%s')"%(student_id,late)
	id=insert(q)
	q="select count(student_id) as c from late_coming where student_id='%s'"%(student_id)
	res=select(q)
	print(res[0]['c'],'/////////////////////////////')
	q="select * from students where student_id='%s'"%(student_id)
	res1=select(q)

	# if res[0]['c']>= 5:
	try:
		gmail = smtplib.SMTP('smtp.gmail.com', 587)

		gmail.ehlo()

		gmail.starttls()

		gmail.login('sngistoutpass.com','messageforall')

	except Exception as e:
		print("Couldn't setup email!!"+str(e))

	msg = MIMEText("Your Child Was Late  "  )
	# msg = MIMEText("Your password is Haii")

	msg['Subject'] = 'Late Report'

	msg['To'] = res1[0]['parent_email']

	msg['From'] = 'sngistoutpass@gmail.com'

	try:

		gmail.send_message(msg)
		print(msg)
		data['status']="success"
		data['method']="guard_send_late"
	

	except Exception as e:

		print("COULDN'T SEND EMAIL", str(e))
		data['status']="failed"
		data['method']="guard_send_late"


	# if res:
	# 	data['status']="success"
	# 	data['method']="guard_send_late"
	
		
	# else:
	# 	data['status']="failed"
	# 	data['method']="guard_send_late"
	return str(data)


@api.route('/Qr_Details',methods=['get','post'])
def Qr_Details():
	data={}
	contents=request.args['contents']
	print(contents)
	q="SELECT * FROM `login` WHERE `login_id`='%s'"%(contents)
	res=select(q)
	if res:
		if res[0]['usertype']=="student":
			q="SELECT *,CONCAT(`first_name`,' ',`last_name`) AS rqname FROM `out_passes` INNER JOIN `students` ON `requested_id`=`login_id` WHERE `requested_id`='%s'"%(contents)
			rs=select(q)
			data['status']="success"
			data['data']=rs
		elif res[0]['usertype']=="teacher":
			q="SELECT *,CONCAT(`first_name`,' ',`last_name`) AS rqname FROM `out_passes` INNER JOIN `teachers` ON `requested_id`=`login_id` WHERE `requested_id`='%s'"%(contents)
			rs=select(q)
			data['status']="success"
			data['data']=rs
	else:
		data['status']="failed"
	data['method']="Qr_Details"
	return str(data)


@api.route('/Guard_view_dept',methods=['get','post'])
def Guard_view_dept():
	data={}
	
	q="SELECT * FROM `department` INNER JOIN `courses` USING(`dept_id`) INNER JOIN `batches` USING(`course_id`)"
	res=select(q)
	if res:
		data['status']="success"
		data['data']=res
		
	else:
		data['status']="failed"
	data['method']="Guard_view_dept"
	return str(data)




	# ////////////////////////////////////////
@api.route('/Forgot_password/', methods=['get', 'post'])
def Forgot_password():
    data = {}
    username = request.args['username']
    email = request.args['email']

    q = """SELECT `security_guards`.`email` AS emails,`login`.`username` AS duser,`login`.`login_id` AS loginid,`login`.`usertype` AS usertype  FROM `security_guards` INNER JOIN `login` USING(`login_id`) WHERE `security_guards`.`email`='%s' AND `login`.`username`='%s'
UNION
SELECT `students`.`email` AS emails,`login`.`username` AS ruser,`login`.`login_id` AS loginid,`login`.`usertype` AS usertype FROM `students` INNER JOIN `login` USING(`login_id`) WHERE `students`.`email`='%s' AND `login`.`username`='%s'
UNION
SELECT `teachers`.`email` AS emails,`login`.`username` AS vuser,`login`.`login_id` AS loginid,`login`.`usertype` AS usertype FROM `teachers` INNER JOIN `login` USING(`login_id`) WHERE `teachers`.`email`='%s' AND `login`.`username`='%s'""" % (
    email, username, email, username, email, username)
    print(q)
    res = select(q)
    print(res)
    if res:
        email = res[0]['emails']
        loginid = res[0]['loginid']

    otp = random.randint(1000, 9999)
    # email=email
    # print(email)
    pwd = "YOUR OTP : " + str(otp)
    print(pwd)
    try:
        gmail = smtplib.SMTP('smtp.gmail.com', 587)
        gmail.ehlo()
        gmail.starttls()
        gmail.login('sngistoutpass@gmail.com','izgqjuqneorhokje')
    except Exception as e:
        print("Couldn't setup email!!" + str(e))

    pwd = MIMEText(pwd)

    pwd['Subject'] = 'One Time Password'

    pwd['To'] = email

    pwd['From'] = 'sngistoutpass@gmail.com'

    try:
        gmail.send_message(pwd)
        print(pwd)
        data['status'] = "success"

    except Exception as e:
        print("COULDN'T SEND EMAIL", str(e))
    else:
        data['status'] = "failed"

    data['status'] = "success"
    data['data'] = otp
    data['data1'] = loginid

    return str(data)


@api.route('/Enter_new_password/', methods=['get', 'post'])
def Enter_new_password():
    data = {}
    confirm = request.args['confirm']
    login_id = request.args['login_id']
    q = "UPDATE `login` SET `password`='%s' WHERE `login_id`='%s'" % (confirm, login_id)
    print(q)
    update(q)

    data['status'] = 'success'

    data['method'] = 'Enter_new_password'
    return str(data)


@api.route('/changepassword',methods=['get','post'])
def changepassword():
	data={}
	login_id=request.args['login_id']
	npass=request.args['npass']
	passs=request.args['pass']
	q="select * from login where password='%s' and login_id='%s'" %(passs,login_id)
	res=select(q)
	if res:

		q="update login set password='%s'where login_id='%s'"%(npass,login_id)
		update(q)
	
		data['status']="success"
	else:
		data['status']="NA"
	data['method']="changepassword"
		
	
	return str(data)





@api.route('/viewroom_amount',methods=['get','post'])
def viewroom_amount():
	data={}
	login_id=request.args['lid']
	q="select * from request where student_id=(select student_id from students where login_id='%s') and requested_for='room'"%(login_id)
	res=select(q)

	if res:
		data['status']="success"
		data['method']="viewroom_amount"
		data['data']=res
		
	else:
		data['status']="failed"
		data['method']="viewroom_amount"
	return str(data)




@api.route('/roompayment',methods=['get','post'])
def roompayment():
	data={}
	rid=request.args['rid']
	amount=request.args['amount']
	q="update request set status='Payment Completed' where request_id='%s'"%(rid)
	update(q)
	q="insert into payment values (null,'%s','%s',curdate())"%(rid,amount)
	insert(q)

	data['status']="success"
	return str(data)



@api.route('/viewmess_amount',methods=['get','post'])
def viewmess_amount():
	data={}
	login_id=request.args['lid']
	q="select * from request where student_id=(select student_id from students where login_id='%s') and requested_for='mess'"%(login_id)
	print(q)
	res=select(q)

	if res:
		data['status']="success"
		data['method']="viewmess_amount"
		data['data']=res
		
	else:
		data['status']="failed"
		data['method']="viewmess_amount"
	return str(data)




@api.route('/messpayment',methods=['get','post'])
def messpayment():
	data={}
	rid=request.args['rid']
	amount=request.args['amount']
	q="update request set status='Payment Completed' where request_id='%s'"%(rid)
	update(q)
	q="insert into payment values (null,'%s','%s',curdate())"%(rid,amount)
	insert(q)

	data['status']="success"
	return str(data)
