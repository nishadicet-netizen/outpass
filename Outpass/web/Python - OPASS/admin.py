from flask import *
from database import *
import uuid
import qrcode
from datetime import date,datetime

import smtplib
from email.mime.text import MIMEText
from flask_mail import Mail


admin=Blueprint('admin',__name__)

@admin.route('/admin_home')
def admin_home():
	if not session.get("lid") is None:
		return render_template("admin_home.html")
	else:
		return redirect(url_for("public.login"))



@admin.route('/resetpassword',methods=['get','post'])
def resetpassword():
	if not session.get('lid') is None:
		data={}	 
		if 'save' in request.form:
			opwd=request.form['opwd']
			npwd=request.form['npwd']
			cpwd=request.form['cpwd']
			if npwd==cpwd:
				q="select * from login where password='%s'"%(opwd)
				res=select(q)
				if res:
					q="update login set password='%s' where password='%s'"%(npwd,opwd)
					update(q)
					flash("password changed")
				else:
					flash("invalid password")
			else:
				flash("password is not correct")
		return render_template('resetpassword.html',data=data)
	else:
		return redirect(url_for('public.login'))



@admin.route('/admin_view_department_leave')
def admin_view_department_leave():
	if not session.get("lid") is None:
		data={}

		did=request.args['did']
		data['did']=did
		if 'action' in request.args:
			action=request.args['action']
			data['action']=action
		else:
			action=None
		if action=='teacher':
			if 'submit' in request.form:
				fdate=request.form['fdate']
				tdate=request.form['tdate']
				q1="SELECT *,CONCAT(`first_name`,' ',`last_name`) AS sname FROM `leave_requests` INNER JOIN `teachers` ON(`leave_requests`.`requested_id`=`teachers`.`login_id`) INNER JOIN hod USING(hod_id) WHERE `type`='teacher' and leave_requests.status!='cancelled' and dept_id='%s' and leave_requests.date between '%s' and '%s' ORDER BY `leave_requests`.`date_time` desc "%(did,fdate,tdate)
				res=select(q1)
				data['leave1']=res
			else:
				q1="SELECT *,CONCAT(`first_name`,' ',`last_name`) AS sname FROM `leave_requests` INNER JOIN `teachers` ON(`leave_requests`.`requested_id`=`teachers`.`login_id`) INNER JOIN hod USING(hod_id) WHERE `type`='teacher' and leave_requests.status!='cancelled' and dept_id='%s' ORDER BY `leave_requests`.`date_time` desc"%(did)
				data['leave1']=select(q1)


			
		if action=='student':
			if 'submit' in request.form:
				fdate=request.form['fdate']
				tdate=request.form['tdate']
				q2="SELECT *,CONCAT(`first_name`,' ',`last_name`) AS sname FROM `leave_requests` INNER JOIN `students` ON(`leave_requests`.`requested_id`=`students`.`login_id`) INNER JOIN courses USING(course_id) WHERE `type`='student' and dept_id='%s' and leave_requests.status!='cancelled'  and leave_requests.date between '%s' and '%s' ORDER BY `leave_requests`.`date_time` desc"%(did,fdate,tdate)
				data['leave2']=select(q2)
			else:
				q2="SELECT *,CONCAT(`first_name`,' ',`last_name`) AS sname FROM `leave_requests` INNER JOIN `students` ON(`leave_requests`.`requested_id`=`students`.`login_id`) INNER JOIN courses USING(course_id) WHERE `type`='student' and dept_id='%s' and leave_requests.status!='cancelled'  ORDER BY `leave_requests`.`date_time` desc"%(did)
				data['leave2']=select(q2)


		return render_template("admin_view_department_leave.html",data=data)
	else:
		return redirect(url_for("public.login"))

@admin.route('/admin_view_department_outpass',methods=['get','post'])
def admin_view_department_outpass():
	if not session.get("lid") is None:
		data={}
		did=request.args['did']
		data['did']=did
		if 'action' in request.args:
			action=request.args['action']
			data['action']=action
		else:
			action=None
		if action=='teacher':
			did=request.args['did']
			data['did']=did
			if 'submit' in request.form:
				fdate=request.form['fdate']
				tdate=request.form['tdate']
				q1="SELECT *,CONCAT(`first_name`,' ',`last_name`) AS sname FROM `out_passes` INNER JOIN `teachers` ON(`out_passes`.`requested_id`=`teachers`.`login_id`) INNER JOIN hod USING(hod_id) WHERE `type`='teacher' and dept_id='%s' and out_passes.status!='cancelled' and out_passes.request_date between '%s' and '%s' ORDER BY `out_passes`.`request_date` desc "%(did,fdate,tdate)
				res=select(q1)
				data['leave1']=res
				session['ps']=q1
				
				session['ss']=res
				
			else:
				q1="SELECT *,CONCAT(`first_name`,' ',`last_name`) AS sname FROM `out_passes` INNER JOIN `teachers` ON(`out_passes`.`requested_id`=`teachers`.`login_id`) INNER JOIN hod USING(hod_id) WHERE `type`='teacher' AND out_passes.status!='cancelled' and dept_id='%s' ORDER BY `out_passes`.`request_date` DESC"%(did)
				res=select(q1)
				data['leave1']=res
				session['ps']=q1


			
		if action=='student':
			did=request.args['did']
			data['did']=did
			if 'submit' in request.form:
				fdate=request.form['fdate']
				tdate=request.form['tdate']
				q2="SELECT *,CONCAT(`first_name`,' ',`last_name`) AS sname FROM `out_passes`INNER JOIN `students` ON(`out_passes`.`requested_id`=`students`.`login_id`) INNER JOIN courses USING(course_id) WHERE `type`!='teacher' and dept_id='%s' and out_passes.status!='cancelled'  and out_passes.request_date between '%s' and '%s' ORDER BY `out_passes`.`request_date` desc"%(did,fdate,tdate)
				res=select(q2)
				data['leave2']=res
				print(res)
			else:
				q2="SELECT *,CONCAT(`first_name`,' ',`last_name`) AS sname FROM `out_passes` INNER JOIN `students` ON(`out_passes`.`requested_id`=`students`.`login_id`) INNER JOIN courses USING(course_id) WHERE `type`!='teacher' and dept_id='%s' and out_passes.status!='cancelled' ORDER BY `out_passes`.`request_date` desc"%(did)
				res=select(q2)
				data['leave2']=res
				print(res)

		return render_template("admin_view_department_outpass.html",data=data)
	else:
		return redirect(url_for("public.login"))

@admin.route('/admin_manage_department',methods=['get','post'])
def admin_manage_department():
	if not session.get("lid") is None:
		data={}
		q="SELECT * FROM `department`"
		data['department']=select(q)
		if 'action' in request.args:
			action=request.args['action']
			did=request.args['did']
		else:
			action=None
		if action=='update':
			q="select * from department where dept_id='%s'"%(did)
			data['updatess']=select(q)
		if action=='delete':
			q="delete from department where dept_id='%s'"%(did)
			delete(q)
			flash("DELETED...")
			return redirect(url_for('admin.admin_manage_department'))
		if 'submits' in request.form:
			department=request.form['department']
			q="update `department` set `department`='%s' where dept_id='%s'"%(department,did)
			update(q)
			flash("UPDATED...")
			return redirect(url_for('admin.admin_manage_department'))

		if 'submit' in request.form:
			department=request.form['department']
			q="select * from department where department='%s'"%(department)
			res=select(q)
			if res:
				flash("department already Exist")
			else:
				q="INSERT INTO `department`(`department`) VALUES('%s')"%(department)
				insert(q)
				flash("ADDED...")
			return redirect(url_for('admin.admin_manage_department'))
		return render_template("admin_manage_department.html",data=data)
	else:
		return redirect(url_for("public.login"))

@admin.route('/admin_view_department',methods=['get','post'])
def admin_view_department():
	if not session.get("lid") is None:
		data={}
		q="SELECT * FROM department"
		data['dept']=select(q)

		if 'serach' in request.form:
			department=request.form['department']
			q="SELECT * FROM `department` where dept_id='%s'"%(department)
			print(q)
		else:
			q="SELECT * FROM `department`"
		res=select(q)
		data['department']=res
		print(res)
	return render_template("admin_view_department.html",data=data)
	# else:
	# 	return redirect(url_for('public.login'))
	   
@admin.route('/admin_manage_course',methods=['get','post'])
def admin_manage_course():
	if not session.get("lid") is None:
		data={}
		q="SELECT * FROM `department`"
		data['dept']=select(q)
		q="SELECT * FROM `courses` INNER JOIN `department` USING(`dept_id`)"
		data['courses']=select(q)
		if 'action' in request.args:
			action=request.args['action']
			cid=request.args['cid']
		else:
			action=None
		if action=='update':
			q="select * from courses  where course_id='%s'"%(cid)
			data['updatess']=select(q)
		if action=='delete':
			q="delete from courses where course_id='%s'"%(cid)
			delete(q)
			flash("DELETED...")
			return redirect(url_for('admin.admin_manage_course'))
		if 'submits' in request.form:
			course=request.form['course']
			duration=request.form['duration']
			department=request.form['department']
			q="update `courses` set `course_name`='%s',`duration`='%s',dept_id='%s' where course_id='%s'"%(course,duration,department,cid)
			update(q)
			flash("UPDATED...")
			return redirect(url_for('admin.admin_manage_course'))

		if 'submit' in request.form:
			course=request.form['course']
			duration=request.form['duration']
			department=request.form['department']
			q="INSERT INTO `courses`(`dept_id`,`course_name`,`duration`) VALUES('%s','%s','%s')"%(department,course,duration)
			insert(q)
			flash("ADDED...")
			return redirect(url_for('admin.admin_manage_course'))
		return render_template("admin_manage_course.html",data=data)
	else:
		return redirect(url_for("public.login"))

@admin.route('/admin_manage_batch',methods=['get','post'])
def admin_manage_batch():
	if not session.get("lid") is None:
		data={}
		q="SELECT * FROM `courses`"
		data['courses']=select(q)
		q="SELECT * FROM `batches` INNER JOIN `courses` USING(`course_id`)"
		data['batches']=select(q)

		if 'action' in request.args:
			action=request.args['action']
			bid=request.args['bid']
		else:
			action=None
		if action=='update':
			q="select * from batches INNER JOIN `courses` USING(`course_id`) where batch_id='%s'"%(bid)
			data['updatess']=select(q)
		if action=='delete':
			q="delete from batches where batch_id='%s'"%(bid)
			delete(q)
			flash("DELETED...")
			return redirect(url_for('admin.admin_manage_batch'))
		if 'submits' in request.form:
			course=request.form['course']
			syear=request.form['syear']
			eyear=request.form['eyear']
			q="UPDATE `batches` SET `course_id`='%s',`start_year`='%s',`end_year`='%s' WHERE `batch_id`='%s'"%(course,syear,eyear,bid)
			update(q)
			flash("UPDATED...")
			return redirect(url_for('admin.admin_manage_batch'))

		if 'submit' in request.form:
			course=request.form['course']
			syear=request.form['syear']
			eyear=request.form['eyear']
			
			q="INSERT INTO `batches`(`course_id`,`start_year`,`end_year`) VALUES('%s','%s','%s')"%(course,syear,eyear)
			insert(q)
			flash("ADDED...")
			return redirect(url_for('admin.admin_manage_batch'))
		return render_template("admin_manage_batch.html",data=data)
	else:
		return redirect(url_for("public.login"))

@admin.route('/admin_manage_hostel',methods=['get','post'])
def admin_manage_hostel():
	if not session.get("lid") is None:
		data={}
		q="SELECT * FROM `hostels`"
		data['hostel']=select(q)
		if 'action' in request.args:
			action=request.args['action']
			hid=request.args['hid']
		else:
			action=None
		if action=='update':
			q="select * from hostels where hostel_id='%s'"%(hid)
			data['updatess']=select(q)
		if action=='delete':
			q="delete from hostels where hostel_id='%s'"%(hid)
			delete(q)
			flash("DELETED...")
			return redirect(url_for('admin.admin_manage_hostel'))
		if 'submits' in request.form:
			hname=request.form['hname']
			place=request.form['place']
			lmark=request.form['lmark']
			phone=request.form['phone']
			email=request.form['email']
			q="UPDATE `hostels`set `name`='%s',`place`='%s',`landmark`='%s',`phone`='%s',`email`='%s' where hostel_id='%s'"%(hname,place,lmark,phone,email,hid)
			update(q)
			flash("UPDATED...")
			return redirect(url_for('admin.admin_manage_hostel'))
		if 'submit' in request.form:
			hname=request.form['hname']
			place=request.form['place']
			lmark=request.form['lmark']
			phone=request.form['phone']
			email=request.form['email']
			q="INSERT INTO `hostels`(`name`,`place`,`landmark`,`phone`,`email`) VALUES('%s','%s','%s','%s','%s')"%(hname,place,lmark,phone,email)
			insert(q)
			flash("ADDED...")
			return redirect(url_for('admin.admin_manage_hostel'))
		return render_template("admin_manage_hostel.html",data=data)
	else:
		return redirect(url_for("public.login"))
		



# @admin.route('/admin_manage_guards',methods=['get','post'])
# def admin_manage_guards():
# 	if not session.get("lid") is None:
# 		data={}
# 		gid=request.args['gid']
# 		data['hid']=hid
# 		q="SELECT *,`security_guards`.`place` AS s_place,`security_guards`.`phone` AS s_phone,`security_guards`.`email` AS s_email FROM `security_guards` INNER JOIN `hostels` USING(`hostel_id`)"
# 		data['guards']=select(q)
# 		if 'action' in request.args:
# 			action=request.args['action']
# 			gid=request.args['gid']
# 		else:
# 			action=None
# 		if action=='update':
# 			q="SELECT *,`security_guards`.`place` AS s_place,`security_guards`.`phone` AS s_phone,`security_guards`.`email` AS s_email FROM `security_guards` INNER JOIN `hostels` USING(`hostel_id`) where login_id='%s'"%(gid)
# 			data['updatess']=select(q)
# 		if action=='delete':
# 			q="delete from security_guards where login_id='%s'"%(gid)
# 			delete(q)
# 			q="delete from login where login_id='%s'"%(gid)
# 			flash('DELETED...')
# 			return redirect(url_for('admin.admin_manage_guards',hid=hid))
# 		if 'submits' in request.form:
# 			fname=request.form['fname']
# 			lname=request.form['lname']
# 			hname=request.form['hname']
# 			place=request.form['place']
# 			phone=request.form['phone']
# 			email=request.form['email']
			
# 			q="update `security_guards` set `hostel_id`='%s',`first_name`='%s',`last_name`='%s',`house_name`='%s',`place`='%s',`phone`='%s',`email`='%s' where login_id='%s' "%(hid,fname,lname,hname,place,phone,email,gid)
# 			update(q)
# 			flash('UPDATED...')
# 			return redirect(url_for('admin.admin_manage_guards',hid=hid))

# 		if 'submit' in request.form:
# 			fname=request.form['fname']
# 			lname=request.form['lname']
# 			hname=request.form['hname']
# 			place=request.form['place']
# 			phone=request.form['phone']
# 			email=request.form['email']
# 			uname=request.form['uname']
# 			pwd=request.form['pwd']
# 			q="insert into login(username,password,usertype) values('%s','%s','guard')"%(uname,pwd)
# 			lid=insert(q)
# 			q="INSERT INTO `security_guards`(`login_id`,`hostel_id`,`first_name`,`last_name`,`house_name`,`place`,`phone`,`email`) VALUES('%s','%s','%s','%s','%s','%s','%s','%s')"%(lid,hid,fname,lname,hname,place,phone,email)
# 			insert(q)
# 			flash('ADDED...')
# 			return redirect(url_for('admin.admin_manage_guards',hid=hid))

# 		return render_template("admin_manage_guards.html",data=data)
# 	else:
# 		return redirect(url_for("public.login"))

@admin.route('/admin_manage_guards',methods=['get','post'])
def admin_manage_guards():
	if not session.get("lid") is None:
		data={}
		q="SELECT * FROM `security_guards`"
		data['security_guards']=select(q)
		if 'action' in request.args:
			action=request.args['action']
			gid=request.args['gid']
		else:
			action=None
		if action=='update':
			q="SELECT * FROM `security_guards` where login_id='%s'"%(gid)
			data['updatess']=select(q)
		if action=='delete':
			q="delete from security_guards where login_id='%s'"%(gid)
			delete(q)
			flash("DELETED...")
			return redirect(url_for('admin.admin_manage_guards'))
		if 'submits' in request.form:
			fname=request.form['fname']
			lname=request.form['lname']
			hname=request.form['hname']
			place=request.form['place']
			phone=request.form['phone']
			email=request.form['email']
			
			q="update `security_guards` set `first_name`='%s',`last_name`='%s',`house_name`='%s',`place`='%s',`phone`='%s',`email`='%s' where login_id='%s' "%(fname,lname,hname,place,phone,email,gid)
			update(q)
			flash("UPDATED...")
			return redirect(url_for('admin.admin_manage_guards'))

		if 'submit' in request.form:
			fname=request.form['fname']
			lname=request.form['lname']
			hname=request.form['hname']
			place=request.form['place']
			phone=request.form['phone']
			email=request.form['email']
			uname=request.form['uname']
			pwd=request.form['pwd']
			q="insert into login(username,password,usertype) values('%s','%s','guard')"%(uname,pwd)
			lid=insert(q)
			print(q)
			q="select * from security_guards where email='%s'"%(email)
			res=select(q)
			if res:
				flash("Email id is already Exist")
			else:
				q="INSERT INTO `security_guards`(`login_id`,`first_name`,`last_name`,`house_name`,`place`,`phone`,`email`) VALUES('%s','%s','%s','%s','%s','%s','%s')"%(lid,fname,lname,hname,place,phone,email)
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
			return redirect(url_for('admin.admin_manage_guards'))

		return render_template("admin_manage_guards.html",data=data)
	else:
		return redirect(url_for("public.login"))


@admin.route('/admin_manage_warden',methods=['get','post'])
def admin_manage_warden():
	if not session.get("lid") is None:
		data={}
		hid=request.args['hid']
		data['hid']=hid


		
		q="SELECT *,`wardens`.`place` AS w_place,`wardens`.`phone` AS w_phone,`wardens`.`email` AS w_email FROM `wardens` INNER JOIN `hostels` USING(`hostel_id`)"
		res=select(q)
		data['warden']=res



		if 'action' in request.args:
			action=request.args['action']
			wid=request.args['wid']
		else:
			action=None
		if action=='update':
			q="SELECT * FROM wardens  where login_id='%s'"%(wid)
			data['updatess']=select(q)
		if action=='delete':
			q="delete from wardens where login_id='%s'"%(wid)
			delete(q)
			q="delete from login where login_id='%s'"%(wid)
			delete(q)
			flash("DELETED...")
			return redirect(url_for('admin.admin_manage_warden',hid=hid))
		if 'submits' in request.form:
			fname=request.form['fname']
			lname=request.form['lname']
			hname=request.form['hname']
			place=request.form['place']
			phone=request.form['phone']
			email=request.form['email']
			
			q="update `wardens` set `hostel_id`='%s',`first_name`='%s',`last_name`='%s',`house_name`='%s',`place`='%s',`phone`='%s',`email`='%s' where login_id='%s' "%(hid,fname,lname,hname,place,phone,email,wid)
			update(q)
			flash("UPDATED...")
			return redirect(url_for('admin.admin_manage_warden',hid=hid))

		if 'submit' in request.form:
			fname=request.form['fname']
			lname=request.form['lname']
			hname=request.form['hname']
			place=request.form['place']
			phone=request.form['phone']
			email=request.form['email']
			uname=request.form['uname']
			pwd=request.form['pwd']
			q="insert into login(username,password,usertype) values('%s','%s','warden')"%(uname,pwd)
			lid=insert(q)
			q="select * from wardens where email='%s'"%(email)
			res=select(q)
			if res:
				flash("Email id is already Exist")
			else:
				q="INSERT INTO `wardens`(`login_id`,`hostel_id`,`first_name`,`last_name`,`house_name`,`place`,`phone`,`email`) VALUES('%s','%s','%s','%s','%s','%s','%s','%s')"%(lid,hid,fname,lname,hname,place,phone,email)
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
					flash("EMAIL SEND SUCCESFULLY")
					


				except Exception as e:
					print("COULDN'T SEND EMAIL", str(e))
				else:
					flash("INVALID DETAILS")
				flash('ADDED...')
			return redirect(url_for('admin.admin_manage_warden',hid=hid))

		return render_template("admin_manage_warden.html",data=data)
	else:
		return redirect(url_for("public.login"))


@admin.route('/admin_manage_teachers',methods=['get','post'])
def admin_manage_teachers():
	if not session.get("lid") is None:
		data={}
		q="SELECT * FROM `teachers`"
		data['teachers']=select(q)
		q="SELECT * FROM `batches` inner join courses using (course_id)"
		data['batch']=select(q)
		if 'action' in request.args:
			action=request.args['action']
			tid=request.args['tid']
		else:
			action=None
		if action=='update':
			q="SELECT * FROM `teachers` where login_id='%s'"%(tid)
			data['updatess']=select(q)
		if action=='delete':
			q="delete from teachers where login_id='%s'"%(tid)
			delete(q)
			flash("DELETED...")
			return redirect(url_for('admin.admin_manage_teachers'))
		if 'submits' in request.form:
			fname=request.form['fname']
			lname=request.form['lname']
			hname=request.form['hname']
			place=request.form['place']
			phone=request.form['phone']
			email=request.form['email']
			
			q="update `teachers` set `first_name`='%s',`last_name`='%s',`house_name`='%s',`place`='%s',`phone`='%s',`email`='%s' where login_id='%s' "%(fname,lname,hname,place,phone,email,tid)
			update(q)
			flash("UPDATED...")
			return redirect(url_for('admin.admin_manage_teachers'))

		if 'submit' in request.form:
			fname=request.form['fname']
			lname=request.form['lname']
			hname=request.form['hname']
			place=request.form['place']
			phone=request.form['phone']
			email=request.form['email']
			bid=request.form['bid']
			uname=request.form['uname']
			pwd=request.form['pwd']
			q="insert into login(username,password,usertype) values('%s','%s','teacher')"%(uname,pwd)
			lid=insert(q)
			q="INSERT INTO `teachers`(`login_id`,batch_id,`first_name`,`last_name`,`house_name`,`place`,`phone`,`email`) VALUES('%s','%s','%s','%s','%s','%s','%s','%s')"%(lid,bid,fname,lname,hname,place,phone,email)
			insert(q)
			flash("ADDED...")
			return redirect(url_for('admin.admin_manage_teachers'))

		return render_template("admin_manage_teachers.html",data=data)
	else:
		return redirect(url_for("public.login"))


@admin.route('/admin_view_hod',methods=['get','post'])
def admin_view_hod():
	if not session.get("lid") is None:
		data={}
		did=request.args['did']
		q="SELECT * FROM hod where dept_id='%s'"%(did)
		data['hod']=select(q)
	return render_template("admin_view_hod.html",data=data)


@admin.route('/admin_view_teachers',methods=['get','post'])
def admin_view_teachers():
	if not session.get("lid") is None:
		data={}
		hid=request.args['hid']
		q="SELECT * FROM teachers INNER JOIN `hod` USING(hod_id) where dept_id='%s'"%(hid)
		data['teacher']=select(q)
	return render_template("admin_view_teachers.html",data=data)


 
@admin.route('/admin_view_leave_requests')
def admin_view_leave_requests():
	if not session.get("lid") is None:
		data={}
		q="SELECT *,CONCAT(`first_name`,' ',`last_name`) AS sname FROM `leave_requests`  INNER JOIN `teachers` ON(`leave_requests`.`requested_id`=`teachers`.`login_id`) WHERE `type`='teacher' and leave_requests.status!='cancelled' ORDER BY `leave_requests`.`date_time`"
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
			return redirect(url_for('admin.admin_view_leave_requests'))
		if action=='reject':
			q="update leave_requests set status='rejected' where leave_id='%s'"%(lid)
			update(q)
			flash('REJECTED...')
			return redirect(url_for('admin.admin_view_leave_requests'))
		

		return render_template("admin_view_leave_requests.html",data=data)
	else:
		return redirect(url_for("public.login"))



@admin.route('/admin_search_student',methods=['get','post'])
def admin_search_student():
	if not session.get("lid") is None:
		data={}
		q="select * from batches"
		data['batches']=select(q)
		q="select * from courses"
		data['courses']=select(q)
		if 'action' in request.args:
			action=request.args['action']
			data['action']=action
		else:
			action=None
		if action=='batch':
			if 'submit' in request.form:
				syear=request.form['syear']
				eyear=request.form['eyear']
				q1="SELECT * FROM `students` INNER JOIN `batches` USING(`batch_id`) INNER JOIN `courses` courses ON(`students`.`course_id`=`courses`.`course_id`) where `batches`.`start_year`='%s' AND `batches`.`end_year`='%s'"%(syear,eyear)
				res1=select(q1)
				if res1:
					data['stud']=res1
				else:
					flash("No Results Found...")
					return redirect(url_for('admin.admin_search_student'))

		if action=='course':
			if 'submit' in request.form:
				cname=request.form['cname']
				q2="SELECT * FROM `students` INNER JOIN `batches` USING(`batch_id`) INNER JOIN `courses` courses ON(`students`.`course_id`=`courses`.`course_id`) where `courses`.`course_name`='%s'"%(cname)
				res2=select(q2)
				if res2:
					data['stud1']=res2
				else:
					flash("No Results Found...")
					return redirect(url_for('admin.admin_search_student'))
		if action=='name':
			if 'submit' in request.form:
				sname=request.form['sname']
				q3="SELECT *,CONCAT(`first_name`,' ',`last_name`) AS `sname` FROM `students` INNER JOIN `batches` USING(`batch_id`) INNER JOIN `courses` courses ON(`students`.`course_id`=`courses`.`course_id`) WHERE `students`.`first_name` LIKE '%s'"%(sname)
				res3=select(q3)
				if res3:
					data['name']=res3
				else:
					flash("No Results Found...")
					return redirect(url_for('admin.admin_search_student'))



		q="SELECT * FROM `students` INNER JOIN `batches` USING(`batch_id`) INNER JOIN `courses` courses ON(`students`.`course_id`=`courses`.`course_id`)"
		data['students']=select(q)
		return render_template("admin_search_student.html",data=data)
	else:
		return redirect(url_for("public.login"))


@admin.route('/admin_view_outpass_request')
def admin_view_outpass_request():
	if not session.get("lid") is None:
		data={}
		q="SELECT *,CONCAT(`first_name`,' ',`last_name`) AS sname FROM `out_passes` INNER JOIN `teachers` ON(`out_passes`.`requested_id`=`teachers`.`login_id`) WHERE `type`='teacher' and out_passes.status!='cancelled' ORDER BY `out_passes`.`request_date`"
		data['outpass']=select(q)
		if 'action' in request.args:
			action=request.args['action']
			pid=request.args['pid']
		else:
			action=None
		if action=='accept':
			path = "static/qrcode/" + str(uuid.uuid4()) + ".png"
			img = qrcode.make(pid)
			img.save(path)
			q="update out_passes set status='accepted',qr='%s' where pass_id='%s'"%(path,pid)
			id=update(q)
			
			flash('ACCEPTED...')
			return redirect(url_for('admin.admin_view_outpass_request'))
		if action=='reject':
			q="update out_passes set status='rejected' where pass_id='%s'"%(pid)
			update(q)
			flash('REJECTED...')
			return redirect(url_for('admin.admin_view_outpass_request'))
		

		return render_template("admin_view_outpass_request.html",data=data)
	else:
		return redirect(url_for("public.login"))


@admin.route('/admin_manage_principal',methods=['get','post'])
def admin_manage_principal():
	if not session.get("lid") is None:
		data={}


		q="SELECT * FROM `principal`"
		res=select(q)
		data['principal']=res


		if 'action' in request.args:
			action=request.args['action']
			pid=request.args['pid']
		else:
			action=None
		if action=='update':
			q="select * from principal where login_id='%s'"%(pid)
			data['updatess']=select(q)
		if action=='delete':
			q="delete from principal where login_id='%s'"%(pid)
			delete(q)
			q="delete from login where login_id='%s'"%(pid)
			delete(q)
			flash('DELETED...')
			return redirect(url_for('admin.admin_manage_principal'))


		if 'submits' in request.form:
			fname=request.form['fname']
			lname=request.form['lname']
			place=request.form['place']
			phone=request.form['phone']
			email=request.form['email']
			q="update `principal` set `fname`='%s',`lname`='%s' ,`place`='%s',phone='%s',email='%s'where login_id='%s'"%(fname,lname,place,phone,email,pid)
			update(q)
			flash('UPDATED...')
			return redirect(url_for('admin.admin_manage_principal'))

		if 'submit' in request.form:
			fname=request.form['fname']
			lname=request.form['lname']
			place=request.form['place']
			phone=request.form['phone']
			email=request.form['email']
			username=request.form['username']
			password=request.form['password']
			q="select * from principal where email='%s'"%(email)
			res=select(q)
			if res:
				flash("Email id is already Exist")
			else:
				q="insert into login(username,password,usertype) values('%s','%s','principal')"%(username,password)
				lid=insert(q)
				q="INSERT INTO `principal`(`login_id`,`fname`,`lname`,`place`,`phone`,`email`) VALUES('%s','%s','%s','%s','%s','%s')"%(lid,fname,lname,place,phone,email)
				insert(q)
				flash('ADDED...')
			return redirect(url_for('admin.admin_manage_principal'))
		return render_template("admin_manage_principal.html",data=data)
	else:
		return redirect(url_for("public.login"))


# @admin.route('/admin_view_leave_report',methods=['get','post'])
# def admin_view_leave_report():
# 	if not session.get("lid") is None:
# 		data={}
# 		if 'action' in request.args:
# 			action=request.args['action']
# 			data['action']=action
# 		else:
# 			action=None
# 		if action=='teacher':
# 			if 'submit' in request.form:
# 				fdate=request.form['fdate']
# 				tdate=request.form['tdate']
# 				q1="SELECT *,CONCAT(`first_name`,' ',`last_name`) AS sname FROM `leave_requests` INNER JOIN `teachers` ON(`leave_requests`.`requested_id`=`teachers`.`login_id`) WHERE `type`='teacher' and leave_requests.status!='cancelled' and leave_requests.date between '%s' and '%s' ORDER BY `leave_requests`.`date_time` desc "%(fdate,tdate)
# 				data['leave1']=select(q1)
# 			else:
# 				q1="SELECT *,CONCAT(`first_name`,' ',`last_name`) AS sname FROM `leave_requests` INNER JOIN `teachers` ON(`leave_requests`.`requested_id`=`teachers`.`login_id`) WHERE `type`='teacher' and leave_requests.status!='cancelled' ORDER BY `leave_requests`.`date_time` desc"
# 				data['leave1']=select(q1)


			
# 		if action=='student':
# 			if 'submit' in request.form:
# 				fdate=request.form['fdate']
# 				tdate=request.form['tdate']
# 				q2="SELECT *,CONCAT(`first_name`,' ',`last_name`) AS sname FROM `leave_requests` INNER JOIN `students` ON(`leave_requests`.`requested_id`=`students`.`login_id`) WHERE `type`='student' and leave_requests.status!='cancelled'  and leave_requests.date between '%s' and '%s' ORDER BY `leave_requests`.`date_time` desc"%(fdate,tdate)
# 				data['leave2']=select(q2)
# 			else:
# 				q2="SELECT *,CONCAT(`first_name`,' ',`last_name`) AS sname FROM `leave_requests` INNER JOIN `students` ON(`leave_requests`.`requested_id`=`students`.`login_id`) WHERE `type`='student' and leave_requests.status!='cancelled'  ORDER BY `leave_requests`.`date_time` desc"
# 				data['leave2']=select(q2)


			

# 		return render_template("admin_view_leave_report.html",data=data)
# 	else:
# 		return redirect(url_for("public.login"))




@admin.route('/admin_view_leave_report',methods=['get','post'])
def admin_view_leave_report():
	if not session.get("lid") is None:
		data={}
		if 'action' in request.args:
			action=request.args['action']
			data['action']=action
		else:
			action=None
		if action=='teacher':
			if 'submit' in request.form:
				fdate=request.form['fdate']
				tdate=request.form['tdate']
				q1="SELECT *,CONCAT(`first_name`,' ',`last_name`) AS sname FROM `leave_requests` INNER JOIN `teachers` ON(`leave_requests`.`requested_id`=`teachers`.`teacher_id`) WHERE `type`='teacher' and leave_requests.status!='cancelled' and leave_requests.date between '%s' and '%s' ORDER BY `leave_requests`.`date_time` desc "%(fdate,tdate)
				res=select(q1)
				data['leave1']=res
				session['leavereport']=data['leave1']
				print()

			else:
				q1="SELECT *,CONCAT(`first_name`,' ',`last_name`) AS sname FROM `leave_requests` INNER JOIN `teachers` ON(`leave_requests`.`requested_id`=`teachers`.`teacher_id`) WHERE `type`='teacher' and leave_requests.status!='cancelled' ORDER BY `leave_requests`.`date_time` desc"
				data['leave1']=select(q1)


			
		if action=='student':
			if 'submit' in request.form:
				fdate=request.form['fdate']
				tdate=request.form['tdate']
				q2="SELECT *,CONCAT(`first_name`,' ',`last_name`) AS sname FROM `leave_requests` INNER JOIN `students` ON(`leave_requests`.`requested_id`=`students`.`student_id`) WHERE `type`='student' and leave_requests.status!='cancelled'  and leave_requests.date between '%s' and '%s' ORDER BY `leave_requests`.`date_time` desc"%(fdate,tdate)
				data['leave2']=select(q2)
			else:
				q2="SELECT *,CONCAT(`first_name`,' ',`last_name`) AS sname FROM `leave_requests` INNER JOIN `students` ON(`leave_requests`.`requested_id`=`students`.`student_id`) WHERE `type`='student' and leave_requests.status!='cancelled'  ORDER BY `leave_requests`.`date_time` desc"
				data['leave2']=select(q2)


			

		return render_template("admin_view_leave_report.html",data=data)
	else:
		return redirect(url_for("public.login"))




@admin.route('/admin_print_leave_report',methods=['get','post'])
def admin_print_leave_report():
	if not session.get("lid") is None:
		data={}

		today=date.today()
		print(today)
		data['today']=today
		now=datetime.now()
		current_time=now.strftime("%H:%M:%S")
		print(current_time)
		data['current_time']=current_time


		
		q1="SELECT *,CONCAT(`first_name`,' ',`last_name`) AS tname FROM `leave_requests` INNER JOIN `teachers` ON(`leave_requests`.`requested_id`=`teachers`.`login_id`) WHERE `type`='teacher' and leave_requests.status!='cancelled'  ORDER BY `leave_requests`.`date_time` desc "
		data['leave1']=select(q1)

		return render_template("admin_print_leave_report.html",data=data)
	else:
		return redirect(url_for("public.login"))



@admin.route('/admin_view_outpass_report',methods=['get','post'])
def admin_view_outpass_report():
	if not session.get("lid") is None:
		data={}
		if 'action' in request.args:
			action=request.args['action']
			data['action']=action
		else:
			action=None
		if action=='teacher':
			if 'submit' in request.form:
				fdate=request.form['fdate']
				tdate=request.form['tdate']
				q1="SELECT *,CONCAT(`first_name`,' ',`last_name`) AS sname FROM `out_passes` INNER JOIN `teachers` ON(`out_passes`.`requested_id`=`teachers`.`login_id`) WHERE `type`='teacher' and out_passes.status!='cancelled' and out_passes.request_date between '%s' and '%s' ORDER BY `out_passes`.`request_date` desc "%(fdate,tdate)
				res=select(q1)
				data['leave1']=res
				session['ps']=q1
				
				session['ss']=res
				
			else:
				q1="SELECT *,CONCAT(`first_name`,' ',`last_name`) AS sname FROM `out_passes` INNER JOIN `teachers` ON(`out_passes`.`requested_id`=`teachers`.`login_id`) WHERE `type`='teacher' AND out_passes.status!='cancelled' ORDER BY `out_passes`.`request_date` DESC"
				res=select(q1)
				data['leave1']=res
				session['ps']=q1


			
		if action=='student':
			if 'submit' in request.form:
				fdate=request.form['fdate']
				tdate=request.form['tdate']
				q2="SELECT *,CONCAT(`first_name`,' ',`last_name`) AS sname FROM `out_passes` INNER JOIN `students` ON(`out_passes`.`requested_id`=`students`.`student_id`) WHERE `type`!='teacher' and out_passes.status!='cancelled'  and out_passes.request_date between '%s' and '%s' ORDER BY `out_passes`.`request_date` desc"%(fdate,tdate)
				data['leave2']=select(q2)
			else:
				q2="SELECT *,CONCAT(`first_name`,' ',`last_name`) AS sname FROM `out_passes` INNER JOIN `students` ON(`out_passes`.`requested_id`=`students`.`student_id`) WHERE `type`!='teacher' and out_passes.status!='cancelled' ORDER BY `out_passes`.`request_date` desc"
				data['leave2']=select(q2)

		return render_template("admin_view_outpass_report.html",data=data)
	else:
		return redirect(url_for("public.login"))




@admin.route('/admin_print_outpass_report',methods=['get','post'])
def admin_print_outpass_report():
	if not session.get("lid") is None:
		data={}

		today=date.today()
		print(today)
		data['today']=today
		now=datetime.now()
		current_time=now.strftime("%H:%M:%S")
		print(current_time)
		data['current_time']=current_time

		ps=session['ps']
		print("mmmmmmmmmmmmmm",ps)
		
		q1=session['ps']
		res=select(q1)
		data['opass']=res

		return render_template("admin_print_outpass_report.html",data=data)
	else:
		return redirect(url_for("public.login"))
# @admin.route('/admin_view_outpass_report',methods=['get','post'])
# def admin_view_outpass_report():
# 	if not session.get("lid") is None:
# 		data={}
# 		if 'action' in request.args:
# 			action=request.args['action']
# 			data['action']=action
# 		else:
# 			action=None
# 		if action=='teacher':
# 			if 'submit' in request.form:
# 				fdate=request.form['fdate']
# 				tdate=request.form['tdate']
# 				q1="SELECT *,CONCAT(`first_name`,' ',`last_name`) AS sname FROM `out_passes` INNER JOIN `teachers` ON(`out_passes`.`requested_id`=`teachers`.`login_id`) WHERE `type`='teacher' and out_passes.status!='cancelled' and out_passes.request_date between '%s' and '%s' ORDER BY `out_passes`.`request_date` desc "%(fdate,tdate)
# 				data['leave1']=select(q1)
# 			else:
# 				q1="SELECT *,CONCAT(`first_name`,' ',`last_name`) AS sname FROM `out_passes` INNER JOIN `teachers` ON(`out_passes`.`requested_id`=`teachers`.`login_id`) WHERE `type`='teacher' and out_passes.status!='cancelled' ORDER BY `out_passes`.`request_date` desc"
# 				data['leave1']=select(q1)


			
# 		if action=='student':
# 			if 'submit' in request.form:
# 				fdate=request.form['fdate']
# 				tdate=request.form['tdate']
# 				q2="SELECT *,CONCAT(`first_name`,' ',`last_name`) AS sname FROM `out_passes` INNER JOIN `students` ON(`out_passes`.`requested_id`=`students`.`login_id`) WHERE `type`!='teacher' and out_passes.status!='cancelled'  and out_passes.request_date between '%s' and '%s' ORDER BY `out_passes`.`request_date` desc"%(fdate,tdate)
# 				data['leave2']=select(q2)
# 			else:
# 				q2="SELECT *,CONCAT(`first_name`,' ',`last_name`) AS sname FROM `out_passes` INNER JOIN `students` ON(`out_passes`.`requested_id`=`students`.`login_id`) WHERE `type`!='teacher' and out_passes.status!='cancelled' ORDER BY `out_passes`.`request_date` desc"
# 				data['leave2']=select(q2)


			

# 		return render_template("admin_view_outpass_report.html",data=data)
# 	else:
# 		return redirect(url_for("public.login"))