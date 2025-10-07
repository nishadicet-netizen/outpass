from flask import *
from public import *
from database import *
import uuid

security=Blueprint('security',__name__)

@security.route('/security_home')
def security_home():
	if not session.get("lid") is None:
		return render_template("security_home.html")
	else:
		return redirect(url_for("public.login"))


@security.route('/report_latecoming',methods=['get','post'])
def report_latecoming():
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
					flash('No Results Found...')
					return redirect(url_for('admin.admin_search_student'))

		if action=='course':
			if 'submit' in request.form:
				cname=request.form['cname']
				q2="SELECT * FROM `students` INNER JOIN `batches` USING(`batch_id`) INNER JOIN `courses` courses ON(`students`.`course_id`=`courses`.`course_id`) where `courses`.`course_name`='%s'"%(cname)
				res2=select(q2)
				if res2:
					data['stud1']=res2
				else:
					flash('No Results Found...')
					return redirect(url_for('admin.admin_search_student'))
		if action=='name':
			if 'submit' in request.form:
				sname=request.form['sname']
				q3="SELECT *,CONCAT(`first_name`,' ',`last_name`) AS `sname` FROM `students` INNER JOIN `batches` USING(`batch_id`) INNER JOIN `courses` courses ON(`students`.`course_id`=`courses`.`course_id`) WHERE `students`.`first_name` LIKE '%s'"%(sname)
				res3=select(q3)
				if res3:
					data['name']=res3
				else:
					flash('No Results Found...')
					return redirect(url_for('admin.admin_search_student'))
				
			

		return render_template("report_latecoming.html",data=data)
	else:
		return redirect(url_for("public.login"))


@security.route('/security_report_latecoming',methods=['get','post'])
def security_report_latecoming():
	if not session.get("lid") is None:
		data={}
		sid=request.args['sid']
		if 'submit' in request.form:
			lateby=request.form['lateby']
			message=request.form['message']
			q="INSERT INTO `late_coming`(`student_id`,`date_time`,`late_by`) VALUES('%s',now(),'%s')"%(sid,lateby)
			insert(q)
			q1="SELECT `warden_id` FROM `wardens` WHERE `hostel_id`='%s'"%(session['hid'])
			res1=select(q1)
			wid=res1[0]['warden_id']
			q="INSERT INTO `messages`(`guard_id`,`student_id`,`reciever_id`,`reciever_type`,`message`,`date_time`) values('%s','%s','%s','warden','%s',now())"%(session['gid'],sid,wid,message)
			insert(q)
			flash('Success...')

		return render_template("security_report_latecoming.html",data=data)
	else:
		return redirect(url_for("public.login"))