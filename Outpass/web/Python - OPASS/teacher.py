from flask import *
from database import *
import uuid
import qrcode
from datetime import date,datetime

import smtplib
from email.mime.text import MIMEText
from flask_mail import Mail

teacher=Blueprint('teacher',__name__)

@teacher.route('/teacher_home')
def teacher_home():
	if not session.get("lid") is None:
		

		return render_template("teacher_home.html")
@teacher.route('/teacher_approve_student_leave')
def teacher_approve_student_leave():
	if not session.get("lid") is None:
		data={}
		
		q="SELECT *,CONCAT(`first_name`,' ',`last_name`) AS sname FROM leave_requests INNER JOIN `students` ON(`leave_requests`.`requested_id`=`students`.`login_id`) WHERE `type`='student' AND leave_requests.status='pending' OR leave_requests.status='teacher approved'"
		res=select(q)
		if res:
			data['leave']=res


		if 'action' in request.args:
			action=request.args['action']
			lid=request.args['lid']
		else:
			action=None

		if action=="accept":
			q="update leave_requests set status='teacher approved' where leave_id='%s'"%(lid)
			update(q)
			return redirect(url_for('teacher.teacher_approve_student_leave'))


		if action=="reject":
			q="update leave_requests set status='Rejected' where leave_id='%s'"%(lid)
			update(q)
			return redirect(url_for('teacher.teacher_approve_student_leave'))
		return render_template("teacher_approve_student_leave.html",data=data)

@teacher.route('/teacher_approve_student_outpass')
def teacher_approve_student_outpass():
	if not session.get("lid") is None:
		data={}

		


		tid=session['tid']
		
		q="SELECT *,CONCAT(`first_name`,' ',`last_name`) AS sname FROM `out_passes` INNER JOIN `students` ON(`out_passes`.`requested_id`=`students`.`login_id`) INNER JOIN `courses` USING(`course_id`) INNER JOIN `department` USING(dept_id) WHERE `type`!='teacher'"
		res=select(q)
		print(q)
		print(res)
		data['outpass']=res

		if 'action' in request.args:
			action=request.args['action']
			pid=request.args['pid']
		else:
			action=None

		if action=="accept":
			q="update out_passes set status='teacher approved' where pass_id='%s'"%(pid)
			update(q)
			return redirect(url_for('teacher.teacher_approve_student_outpass'))


		if action=="reject":
			q="update out_passes set status='Rejected' where pass_id='%s'"%(pid)
			update(q)
			return redirect(url_for('teacher.teacher_approve_student_outpass'))

		

		return render_template("teacher_approve_student_outpass.html",data=data)
	else:
		return redirect(url_for("public.login"))

@teacher.route('/teacher_manage_students',methods=['get','post'])
def teacher_manage_students():
	if not session.get("lid") is None:
		data={}
		q="select * from batches"
		data['batches']=select(q)
		q="select * from courses"
		data['courses']=select(q)
		q="SELECT * FROM `students` INNER JOIN `batches` USING(`batch_id`) INNER JOIN `courses` courses ON(`students`.`course_id`=`courses`.`course_id`)"
		data['students']=select(q)
		if 'action' in request.args:
			action=request.args['action']
			sid=request.args['sid']
		else:
			action=None
		if action=='update':
			q="SELECT * FROM `students` INNER JOIN `batches` USING(`batch_id`) INNER JOIN courses ON(`students`.`course_id`=`courses`.`course_id`) WHERE login_id='%s'"%(sid)
			data['updatess']=select(q)
		if action=='delete':
			q="delete from students where login_id='%s'"%(sid)
			delete(q)
			q="delete from login where login_id='%s'"%(sid)
			delete(q)
			flash('DELETED...')
			return redirect(url_for('teacher.teacher_manage_students'))
		if 'submits' in request.form:
			batch=request.form['batch']
			course=request.form['course']
			fname=request.form['fname']
			lname=request.form['lname']
			hname=request.form['hname']
			place=request.form['place']
			pmail=request.form['pmail']
			phone=request.form['phone']
			email=request.form['email']
			
			
			
			q="UPDATE  `students` SET `batch_id`='%s',course_id='%s',`first_name`='%s',`last_name`='%s',`house_name`='%s',`place`='%s',`parent_email`='%s',`phone`='%s',`email`='%s' where login_id='%s'"%(batch,course,fname,lname,hname,place,pmail,phone,email,sid)
			update(q)
			flash('UPDATED...')
			return redirect(url_for('teacher.teacher_manage_students'))
		if 'submit' in request.form:
			batch=request.form['batch']
			course=request.form['course']
			fname=request.form['fname']
			lname=request.form['lname']
			hname=request.form['hname']
			place=request.form['place']
			pmail=request.form['pmail']
			phone=request.form['phone']
			hostel=request.form['Hostel']
			email=request.form['email']
			uname=request.form['uname']
			pwd=request.form['pwd']
			q="insert into login(username,password,usertype) values('%s','%s','student')"%(uname,pwd)
			lid=insert(q)
			q="select * from students where email='%s'"%(email)
			res=select(q)
			if res:
				flash("Email id is already Exist")
			else:
				q="INSERT INTO `students`(`login_id`,`batch_id`,course_id,`first_name`,`last_name`,`house_name`,`place`,`parent_email`,`phone`,`email`,hostel) VALUES('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"%(lid,batch,course,fname,lname,hname,place,pmail,phone,email,hostel)
				insert(q)

				pwd=str(pwd)
				email=email
				print(email)
				pwd="YOUR USERNAME :"+uname+" "+"PASSWORD :"+pwd
				print(pwd)
				try:
					gmail = smtplib.SMTP('smtp.gmail.com', 587)
					gmail.ehlo()
					gmail.starttls()
					gmail.login('sngistoutpass@gmail.com','izgqjuqneorhokje')
				except Exception as e:
					print("Couldn't setup email!!"+str(e))

				pwd = MIMEText(pwd)

				pwd['Subject'] = 'USERNAME AND PASSWORD'

				pwd['To'] = email

				pwd['From'] = 'sngistoutpass@gmail.com'

				try:
					gmail.send_message(pwd)
					print(pwd)
					flash("EMAIL SENED SUCCESFULLY")
					


				except Exception as e:
					print("COULDN'T SEND EMAIL", str(e))
				else:
					flash("INVALID DETAILS")
				flash('ADDED...')
			return redirect(url_for('teacher.teacher_manage_students'))

		return render_template("teacher_manage_students.html",data=data)
	else:
		return redirect(url_for("public.login"))

@teacher.route('/teacher_request_for_leave',methods=['get','post'])
def teacher_request_for_leave():
	if not session.get("lid") is None:
		data={}
		q="SELECT * FROM `leave_requests` WHERE `requested_id`='%s' AND `type`='teacher'"%(session['lid'])
		data['leave']=select(q)
		if 'action' in request.args:
			action=request.args['action']
			lid=request.args['lid']
		else:
			action=None
		if action=='cancel':
			q="update leave_requests set status='cancelled' where leave_id='%s'"%(lid)
			update(q)
			flash('Request Cancelled...')
			return redirect(url_for('teacher.teacher_request_for_leave'))
		if 'submit' in request.form:
			reason=request.form['reason']
			date=request.form['date']
			duration=request.form['duration']
			q="INSERT INTO `leave_requests`(`requested_id`,`type`,`reason`,`date`,`duration`,`date_time`,`status`) VALUES('%s','teacher','%s','%s','%s',now(),'pending')"%(session['lid'],reason,date,duration)
			insert(q)
			flash('Your Request Has Been Sent...Wait For The Response')
			return redirect(url_for('teacher.teacher_request_for_leave'))
		

		return render_template("teacher_request_for_leave.html",data=data)
	else:
		return redirect(url_for("public.login"))
		
@teacher.route('/teacher_request_for_outpass',methods=['get','post'])
def teacher_request_for_outpass():
	if not session.get("lid") is None:
		from datetime import date,datetime
		data={}

		today=date.today()
		print("ddddddddddddddd",today)
		data['today']=today


		now=datetime.now()
		current_time=now.strftime("%H:%M")
		print("tttttttttttttttt",current_time)
		data['current_time']=current_time



		q="SELECT * FROM `out_passes` WHERE `requested_id`='%s' AND `type`='teacher'"%(session['lid'])
		data['opass']=select(q)
		if 'action' in request.args:
			action=request.args['action']
			pid=request.args['pid']
		else:
			action=None
		if action=='cancel':
			q="update out_passes set status='cancelled' where pass_id='%s'"%(pid)
			update(q)
			flash('Request Cancelled...')
			return redirect(url_for('teacher.teacher_request_for_outpass'))
		if 'submit' in request.form:
			reason=request.form['reason']
			date=request.form['date']
			time=request.form['time']
			return_time=request.form['return_time']
			
			q="INSERT INTO `out_passes`(`requested_id`,`type`,`request_date`,`request_time`,`reason`,`status`,return_time) VALUES('%s','teacher','%s','%s','%s','pending','%s')"%(session['lid'],date,time,reason,return_time)
			id=insert(q)
			s=qrcode.make(str(id))
			path="static/qrcode/"+str(uuid.uuid4())+".png"
			s.save(path)
			flash('Your Request Has Been Sent...Wait For The Response')
			return redirect(url_for('teacher.teacher_request_for_outpass'))
		

		return render_template("teacher_request_for_outpass.html",data=data)
	else:
		return redirect(url_for("public.login"))

@teacher.route('/teacher_view_leave_request')
def teacher_view_leave_request():
	if not session.get("lid") is None:
		data={}
		q="SELECT *,CONCAT(`first_name`,' ',`last_name`) AS sname FROM `leave_requests` INNER JOIN `students` ON(`leave_requests`.`requested_id`=`students`.`login_id`) WHERE `type`='student' ORDER BY `leave_requests`.`date_time`"
		data['leave']=select(q)
		if 'action' in request.args:
			action=request.args['action']
			lid=request.args['lid']
		else:
			action=None
		if action=='accept':
			q="update leave_requests set status='accepted' where leave_id='%s'"%(lid)
			update(q)
			flash('ACCEPTED...')
			return redirect(url_for('teacher.teacher_view_leave_request'))
		if action=='reject':
			q="update leave_requests set status='rejected' where leave_id='%s'"%(lid)
			update(q)
			flash('REJECTED...')
			return redirect(url_for('teacher.teacher_view_leave_request'))
		

		return render_template("teacher_view_leave_request.html",data=data)
	else:
		return redirect(url_for("public.login"))

@teacher.route('/teacher_view_outpass_request')
def teacher_view_outpass_request():
	if not session.get("lid") is None:
		data={}
		# q="SELECT *,CONCAT(`first_name`,' ',`last_name`) AS sname FROM `out_passes` INNER JOIN `students` ON(`out_passes`.`requested_id`=`students`.`login_id`) WHERE `type`='class' and out_passes.status!='cancelled' ORDER BY `out_passes`.`request_date`"
		q="select * from out_passes  join students on(students.login_id=out_passes.requested_id) inner join courses using(course_id) inner join batches using(batch_id) where type='student'"
		print(q)

		data['outpass']=select(q)
		if 'action' in request.args:
			action=request.args['action']
			pid=request.args['pid']
		else:
			action=None
		if action=='accept':
			q="update out_passes set status='accepted' where pass_id='%s'"%(pid)
			update(q)
			flash('ACCEPTED...')
			return redirect(url_for('teacher.teacher_view_outpass_request'))
		if action=='reject':
			q="update out_passes set status='rejected' where pass_id='%s'"%(pid)
			update(q)
			flash('REJECTED...')
			return redirect(url_for('teacher.teacher_view_outpass_request'))
		

		return render_template("teacher_view_outpass_request.html",data=data)
	else:
		return redirect(url_for("public.login"))