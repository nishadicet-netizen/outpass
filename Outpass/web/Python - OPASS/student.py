from flask import *
from database import *
import uuid
from public import *

student=Blueprint('student',__name__)

@student.route('/student_home')
def student_home():
	if not session.get("lid") is None:
		

		return render_template("student_home.html")
	else:
		return redirect(url_for("public.login"))

@student.route('/student_request_for_leave',methods=['get','post'])
def student_request_for_leave():
	if not session.get("lid") is None:
		data={}
		q="SELECT * FROM `leave_requests` WHERE `requested_id`='%s' AND `type`='student'"%(session['lid'])
		data['leave']=select(q)
		if 'action' in request.args:
			action=request.args['action']
			lid=request.args['lid']
		else:
			action=None
		if action=='cancel':
			q="update leave_requests set status='cancelled' where leave_id='%s'"%(lid)
			update(q)
			flash("Request Cancelled...")
			return redirect(url_for('student.student_request_for_leave'))
		if 'submit' in request.form:
			reason=request.form['reason']
			date=request.form['date']
			duration=request.form['duration']
			q="INSERT INTO `leave_requests`(`requested_id`,`type`,`reason`,`date`,`duration`,`date_time`,`status`) VALUES('%s','student','%s','%s','%s',now(),'pending')"%(session['lid'],reason,date,duration)
			insert(q)
			flash("Your Request Has Been Sent...Wait For The Response")
			return redirect(url_for('student.student_request_for_leave'))
		

		return render_template("student_request_for_leave.html",data=data)
	else:
		return redirect(url_for("public.login"))


@student.route('/student_request_for_outpass',methods=['get','post'])
def student_request_for_outpass():
	if not session.get("lid") is None:
		data={}
		q="SELECT * FROM `out_passes` WHERE `requested_id`='%s' AND `type`='class' or type='hostel' ORDER BY `out_passes`.`request_date` desc "%(session['lid'])
		data['opass']=select(q)
		if 'action' in request.args:
			action=request.args['action']
			pid=request.args['pid']
		else:
			action=None
		if action=='cancel':
			q="update out_passes set status='cancelled' where pass_id='%s'"%(pid)
			update(q)
			flash("Request Cancelled...")
			return redirect(url_for('student.student_request_for_outpass'))
		if 'submit' in request.form:
			reason=request.form['reason']
			date=request.form['date']
			time=request.form['time']
			
			q="INSERT INTO `out_passes`(`requested_id`,`type`,`request_date`,`request_time`,`reason`,`status`) VALUES('%s','class','%s','%s','%s','pending')"%(session['lid'],date,time,reason)
			insert(q)
			flash("Your Request Has Been Sent...Wait For The Response")
			return redirect(url_for('student.student_request_for_outpass'))
		if 'submits' in request.form:
			reason=request.form['reason']
			date=request.form['date']
			time=request.form['time']
			
			q1="INSERT INTO `out_passes`(`requested_id`,`type`,`request_date`,`request_time`,`reason`,`status`) VALUES('%s','hostel','%s','%s','%s','pending')"%(session['lid'],date,time,reason)
			insert(q1)
			flash("Your Request Has Been Sent...Wait For The Response")
			return redirect(url_for('student.student_request_for_outpass'))
		

		return render_template("student_request_for_outpass.html",data=data)
	else:
		return redirect(url_for("public.login"))
		