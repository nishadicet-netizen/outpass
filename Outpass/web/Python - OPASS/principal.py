from flask import *
from database import *
import qrcode
import uuid
from public import *
principal=Blueprint('principal',__name__)

@principal.route('/principal_home')
def principal_home():
	data={}
	data['p_name']=session['p_name']
	if not session.get("lid") is None:
		return render_template("principal_home.html",data=data)
	else:
		return redirect(url_for("public.login"))
@principal.route('/principal_resetpassword',methods=['get','post'])
def principal_resetpassword():
	if not session.get('lid') is None:
		data={}	 
		if 'change' in request.form:
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
		return render_template('principal_resetpassword.html',data=data)
	else:
		return redirect(url_for('public.login'))

@principal.route('/principal_approve_teacher_leave')
def principal_approve_teacher_leave():
	
	
	if not session.get("lid") is None:
		data={}
		q="SELECT *,CONCAT(`first_name`,' ',`last_name`) AS sname FROM leave_requests INNER JOIN `teachers` ON(`leave_requests`.`requested_id`=`teachers`.`login_id`) WHERE `type`='teacher' AND leave_requests.status='hod approved teacher leave' OR leave_requests.status='principal approved teacher leave'"
		res=select(q)
		if res:
			data['leave']=res


		if 'action' in request.args:
			action=request.args['action']
			lid=request.args['lid']
		else:
			action=None

		if action=="accept":
			q="update leave_requests set status='principal approved teacher leave' where leave_id='%s'"%(lid)
			update(q)
			return redirect(url_for('principal.principal_approve_teacher_leave'))


		if action=="reject":
			q="update leave_requests set status='Rejected' where leave_id='%s'"%(lid)
			update(q)
		return render_template("principal_approve_teacher_leave.html",data=data)
		return render_template("principal_approve_teacher_leave.html",data=data)
	else:
		return redirect(url_for("public.login"))

@principal.route('/principal_approve_teacher_outpass')
def principal_approve_teacher_outpass():

	
	if not session.get("lid") is None:
		data={}
		q="SELECT *,CONCAT(`first_name`,' ',`last_name`) AS sname,out_passes.status as ss FROM `out_passes` INNER JOIN `teachers` ON(`out_passes`.`requested_id`=`teachers`.`login_id`)  WHERE `type`='teacher' AND status='hod approved teacher outpass' OR status='principal approved teacher outpass'"
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
			q="update out_passes set status='principal approved teacher outpass',qr='%s' where pass_id='%s'"%(path,pid)
			update(q)
			return redirect(url_for('principal.principal_approve_teacher_outpass'))


		if action=="reject":
			q="update out_passes set status='Rejected' where pass_id='%s'"%(pid)
			update(q)
			return redirect(url_for('principal.principal_approve_teacher_outpass'))
		return render_template("principal_approve_teacher_outpass.html",data=data)
	else:
		return redirect(url_for("public.login"))

@principal.route('/principal_add_hod',methods=['get','post'])
def principal_add_hod():
	if not session.get("lid") is None:
		data={}
		
		if 'action' in request.args:
			action=request.args['action']
			cid=request.args['cid']
		else:
			action=None
		if action=='update':
			q="select * from hod where login_id='%s'"%(cid)
			data['updatess']=select(q)
		if action=='delete':
			q="delete from hod where login_id='%s'"%(cid)
			delete(q)
			q="delete from login where login_id='%s'"%(cid)
			delete(q)
			flash("DELETED...")
			return redirect(url_for('principal.principal_add_hod'))
		if 'submits' in request.form:
			fname=request.form['fname']
			lname=request.form['lname']
			place=request.form['place']
			phone=request.form['phone']
			email=requset.form['email']
			q="update `hod` set `fname`='%s',`lname`='%s' ,`place`='%s',phone='%s',email='%s'where login_id='%s'"%(fname,lname,place,phone,email,cid)
			update(q)
			flash("UPDATED...")
			return redirect(url_for('principal.principal_add_hod'))

		if 'submit' in request.form:
			fname=request.form['fname']
			lname=request.form['lname']
			place=request.form['place']
			phone=request.form['phone']
			email=request.form['email']
			username=request.form['username']
			password=request.form['password']
			department=request.form['department']
			q="select * from hod where dept_id='%s'"%(department)
			res=select(q)
			if res:
				flash("already exist")
			else:
				q="insert into login(username,password,usertype) values('%s','%s','hod')"%(username,password)
				lid=insert(q)
				q="INSERT INTO `hod`(`login_id`,`dept_id`,`fname`,`lname`,`place`,`phone`,`email`) VALUES('%s','%s','%s','%s','%s','%s','%s')"%(lid,department,fname,lname,place,phone,email)
				print(q)
				insert(q)
				flash("ADDED...")
			return redirect(url_for('principal.principal_add_hod'))

		q="select * from department"
		res=select(q)
		data['dept']=res

		q="select * from hod inner join department using(dept_id)"
		res=select(q)
		data['hod']=res
		return render_template("principal_add_hod.html",data=data)
	else:
		return redirect(url_for("public.login"))
@principal.route('/principal_manage_department',methods=['get','post'])
def principal_manage_department():
	if not session.get("lid") is None:
		data={}
		q="SELECT * FROM `department`"
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

@principal.route('/principal_view_student',methods=['get','post'])
def principal_view_student():
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
					return redirect(url_for('principal.principal_view_student'))

		if action=='course':
			if 'submit' in request.form:
				cname=request.form['cname']
				q2="SELECT * FROM `students` INNER JOIN `batches` USING(`batch_id`) INNER JOIN `courses` courses ON(`students`.`course_id`=`courses`.`course_id`) where `courses`.`course_name`='%s'"%(cname)
				res2=select(q2)
				if res2:
					data['stud1']=res2
				else:
					flash("No Results Found...")
					return redirect(url_for('principal.principal_view_student'))
		if action=='name':
			if 'submit' in request.form:
				sname=request.form['sname']
				q3="SELECT *,CONCAT(`first_name`,' ',`last_name`) AS `sname` FROM `students` INNER JOIN `batches` USING(`batch_id`) INNER JOIN `courses` courses ON(`students`.`course_id`=`courses`.`course_id`) WHERE `students`.`first_name` LIKE '%s'"%(sname)
				res3=select(q3)
				if res3:
					data['name']=res3
				else:
					flash("No Results Found...")
					return redirect(url_for('principal.principal_view_student'))



		q="SELECT * FROM `students` INNER JOIN `batches` USING(`batch_id`) INNER JOIN `courses` courses ON(`students`.`course_id`=`courses`.`course_id`)"
		data['students']=select(q)
		return render_template("principal_view_student.html",data=data)
	else:
		return redirect(url_for("public.login"))
@principal.route('/principal_view_department',methods=['get','post'])
def principal_view_department():
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
	return render_template("principal_view_department.html",data=data)
@principal.route('/principal_view_hod',methods=['get','post'])
def principal_view_hod():
	if not session.get("lid") is None:
		data={}
		did=request.args['did']
		q="SELECT * FROM hod where dept_id='%s'"%(did)
		data['hod']=select(q)
	return render_template("principal_view_hod.html",data=data)

@principal.route('/principal_view_teachers',methods=['get','post'])
def principal_view_teachers():
	if not session.get("lid") is None:
		data={}
		hid=request.args['hid']
		q="SELECT * FROM teachers INNER JOIN `hod` USING(hod_id) where dept_id='%s'"%(hid)
		data['teacher']=select(q)
	return render_template("principal_view_teachers.html",data=data)
@principal.route('/principal_view_department_outpass')
def pricipal_view_department_outpass():
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

		return render_template("principal_view_department_outpass.html",data=data)
	else:
		return redirect(url_for("public.login"))
@principal.route('/principal_view_department_leave',methods=['get','post'])
def principal_view_department_leave():
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


		return render_template("principal_view_department_leave.html",data=data)
	else:
		return redirect(url_for("public.login"))
