from flask import *
from database import *
import qrcode
import uuid
hod=Blueprint('hod',__name__)

@hod.route('/hod_home')
def hod_home():
	if not session.get("lid") is None:
		return render_template("hod_home.html")
	else:
		return redirect(url_for("public.login"))


@hod.route('/hod_apporve_teacher_outpass')
def hod_apporve_teacher_outpass():
	if not session.get("lid") is None:
		data={}
		
		hod=session['hod']
		q="SELECT *,CONCAT(`first_name`,' ',`last_name`) AS sname,out_passes.status AS ss FROM `out_passes` INNER JOIN `teachers` ON `teachers`.`login_id`=`out_passes`.`requested_id` WHERE TYPE='teacher' AND hod_id='%s'"%(hod)
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
			q="update out_passes set status='hod approved teacher outpass' where pass_id='%s'"%(pid)
			update(q)
			return redirect(url_for('hod.hod_apporve_teacher_outpass'))


		if action=="reject":
			q="update out_passes set status='Rejected' where pass_id='%s'"%(pid)
			update(q)
		return render_template("hod_apporve_teacher_outpass.html",data=data)
	else:
		return redirect(url_for("public.login"))


@hod.route('/hod_approve_teacher_leave')
def hod_approve_teacher_leave():
	if not session.get("lid") is None:
		data={}

		hod=session['hod']
		q="SELECT *,CONCAT(`first_name`,' ',`last_name`) AS sname FROM leave_requests INNER JOIN `teachers` ON(`leave_requests`.`requested_id`=`teachers`.`login_id`) WHERE `type`='teacher' AND leave_requests.status='pending' OR leave_requests.status='hod approved teacher leave' or leave_requests.status='Rejected'"
		res=select(q)
		if res:
			data['leave']=res


		if 'action' in request.args:
			action=request.args['action']
			lid=request.args['lid']
		else:
			action=None

		if action=="accept":
			q="update leave_requests set status='hod approved teacher leave' where leave_id='%s'"%(lid)
			update(q)
			return redirect(url_for('hod.hod_approve_teacher_leave'))


		if action=="reject":
			q="update leave_requests set status='Rejected' where leave_id='%s'"%(lid)
			update(q)
		return render_template("hod_approve_teacher_leave.html",data=data)
	else:
		return redirect(url_for("public.login"))
@hod.route('/hod_approve_student_outpass')
def hod_approve_student_outpass():
	if not session.get("lid") is None:
		data={}
		did=session['dept_id']
		q="SELECT *,CONCAT(`first_name`,' ',`last_name`) AS sname FROM `out_passes` INNER JOIN `students` ON(`out_passes`.`requested_id`=`students`.`login_id`) INNER JOIN `courses` USING(`course_id`) INNER JOIN `department` USING(dept_id) WHERE `type`!='teacher' AND STATUS='teacher approved' or STATUS='hod approved' and dept_id='%s'"%(did)
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
			s=qrcode.make(str(pid))
			path="static/qrcode/"+str(uuid.uuid4())+".png"
			s.save(path)
			q="update out_passes set status='hod approved',qr='%s' where pass_id='%s'"%(path,pid)
			update(q)
			print(q)
			return redirect(url_for('hod.hod_approve_student_outpass'))


		if action=="reject":
			q="update out_passes set status='Rejected' where pass_id='%s'"%(pid)
			update(q)
			return redirect(url_for('hod.hod_approve_student_outpass'))

		return render_template("hod_approve_student_outpass.html",data=data)
	else:
		return redirect(url_for("public.login"))
@hod.route('/hod_approve_student_leave')
def hod_approve_student_leave():
	if not session.get("lid") is None:
		data={}
		q="SELECT *,CONCAT(`first_name`,' ',`last_name`) AS sname FROM leave_requests INNER JOIN `students` ON(`leave_requests`.`requested_id`=`students`.`login_id`) WHERE `type`='student' AND leave_requests.status='hod approved' OR leave_requests.status='teacher approved'"
		res=select(q)
		if res:
			data['leave']=res
			print(res)


		if 'action' in request.args:
			action=request.args['action']
			lid=request.args['lid']
		else:
			action=None

		if action=="accept":
			q="update leave_requests set status='hod approved' where leave_id='%s'"%(lid)
			update(q)
			return redirect(url_for('hod.hod_approve_student_leave'))


		if action=="reject":
			q="update leave_requests set status='Rejected' where leave_id='%s'"%(lid)
			update(q)
			return redirect(url_for('hod.hod_approve_student_leave'))
		
		return render_template("hod_approve_student_leave.html",data=data)
	else:
		return redirect(url_for("public.login"))

@hod.route('/hod_manage_batch',methods=['get','post'])
def hod_manage_batch():
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
			return redirect(url_for('hod.hod_manage_batch'))
		if 'submits' in request.form:
			course=request.form['course']
			syear=request.form['syear']
			eyear=request.form['eyear']
			q="UPDATE `batches` SET `course_id`='%s',`start_year`='%s',`end_year`='%s' WHERE `batch_id`='%s'"%(course,syear,eyear,bid)
			update(q)
			flash("UPDATED...")
			return redirect(url_for('hod.hod_manage_batch'))

		if 'submit' in request.form:
			course=request.form['course']
			syear=request.form['syear']
			eyear=request.form['eyear']
			
			q="INSERT INTO `batches`(`course_id`,`start_year`,`end_year`) VALUES('%s','%s','%s')"%(course,syear,eyear)
			insert(q)
			flash("ADDED...")
			return redirect(url_for('hod.hod_manage_batch'))
		return render_template("hod_manage_batch.html",data=data)
	else:
		return redirect(url_for("public.login"))

@hod.route('/hod_add_teacher',methods=['get','post'])
def hod_add_teacher():
	if not session.get("lid") is None:
		data={}
		q="SELECT * FROM `teachers`"
		data['teachers']=select(q)
		hod=session['hod']
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
			return redirect(url_for('hod.hod_add_teacher'))
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
			return redirect(url_for('hod.hod_add_teacher'))

		if 'submit' in request.form:
			fname=request.form['fname']
			lname=request.form['lname']
			hname=request.form['hname']
			place=request.form['place']
			phone=request.form['phone']
			email=request.form['email']
			uname=request.form['uname']
			pwd=request.form['pwd']
			q="insert into login values(null,'%s','%s','teacher')"%(uname,pwd)
			lid=insert(q)
			q="select * from teachers where email='%s'"%(email)
			res=select(q)
			if res:
				flash("Email id is already Exist")
			else:
				q="INSERT INTO `teachers` VALUES(null,'%s','%s','%s','%s','%s','%s','%s','%s')"%(lid,hod,fname,lname,hname,place,phone,email)
				insert(q)
				print(q)
				flash("ADDED...")
			return redirect(url_for('hod.hod_add_teacher'))

		return render_template("hod_add_teacher.html",data=data)
	else:
		return redirect(url_for("public.login"))
@hod.route('/hod_search_student',methods=['get','post'])
def hod_search_student():
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
					return redirect(url_for('hod.hod_search_student'))

		if action=='course':
			if 'submit' in request.form:
				cname=request.form['cname']
				q2="SELECT * FROM `students` INNER JOIN `batches` USING(`batch_id`) INNER JOIN `courses` courses ON(`students`.`course_id`=`courses`.`course_id`) where `courses`.`course_name`='%s'"%(cname)
				res2=select(q2)
				if res2:
					data['stud1']=res2
				else:
					flash("No Results Found...")
					return redirect(url_for('hod.hod_search_student'))
		if action=='name':
			if 'submit' in request.form:
				sname=request.form['sname']
				q3="SELECT *,CONCAT(`first_name`,' ',`last_name`) AS `sname` FROM `students` INNER JOIN `batches` USING(`batch_id`) INNER JOIN `courses` courses ON(`students`.`course_id`=`courses`.`course_id`) WHERE `students`.`first_name` LIKE '%s'"%(sname)
				res3=select(q3)
				if res3:
					data['name']=res3
				else:
					flash("No Results Found...")
					return redirect(url_for('hod.hod_search_student'))



		q="SELECT * FROM `students` INNER JOIN `batches` USING(`batch_id`) INNER JOIN `courses` courses ON(`students`.`course_id`=`courses`.`course_id`)"
		data['students']=select(q)
		return render_template("hod_search_student.html",data=data)
	else:
		return redirect(url_for("public.login"))

@hod.route('/resetpassword',methods=['get','post'])
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
		return render_template('hod_reset_pwd.html',data=data)
	else:
		return redirect(url_for('public.login'))