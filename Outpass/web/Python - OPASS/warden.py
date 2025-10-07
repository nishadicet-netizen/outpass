from flask import *
from database import *
import uuid

warden=Blueprint('warden',__name__)

@warden.route('/warden_home')
def warden_home():
	if not session.get("lid") is None:
		data={}
		
 		
		return render_template("warden_home.html",data=data)
	else:
		return redirect(url_for("public.login"))

@warden.route('/warden_manage_room',methods=['get','post'])
def warden_manage_room():
	if not session.get("lid") is None:
		data={}
		q="select * from hostels"
		data['hostels']=select(q)
		q="SELECT * FROM `rooms` INNER JOIN `hostels` USING(`hostel_id`)"
		data['rooms']=select(q)
		if 'action' in request.args:
			action=request.args['action']
			rid=request.args['rid']
		else:
			action=None
		if action=='update':
			q="select * from rooms inner join hostels using(hostel_id) where room_id='%s'"%(rid)
			data['updatess']=select(q)
		if action=='delete':
			q="delete from rooms where room_id='%s'"%(rid)
			delete(q)
			flash("DELETED...")
			return redirect(url_for('warden.warden_manage_room'))
		if 'submits' in request.form:
			
			room_no=request.form['room_no']
			capacity=request.form['capacity']
			q="UPDATE `rooms` SET `room_no`='%s',`capacity`='%s' where room_id='%s'"%(room_no,capacity,rid)
			update(q)
			flash("UPDATED...")
			return redirect(url_for('warden.warden_manage_room'))

		if 'submit' in request.form:
			hostel=request.form['hostel']
			room_no=request.form['room_no']
			capacity=request.form['capacity']
			q="INSERT INTO `rooms`(`room_no`,`hostel_id`,`capacity`) VALUES('%s','%s','%s')"%(room_no,hostel,capacity)
			insert(q)
			flash("ADDED...")
			return redirect(url_for('warden.warden_manage_room'))
		

		return render_template("warden_manage_room.html",data=data)
	else:
		return redirect(url_for("public.login"))



@warden.route('/warden_add_guest',methods=['get','post'])
def warden_add_guest():
	if not session.get("lid") is None:
		data={}

		q="select * from rooms"
		data['rooms']=select(q)

		if 'btn' in request.form:
			rid=request.form['room']
			guest=request.form['guest']
			noof=request.form['noof']
			date=request.form['date']

			q="insert into guest values(null,'%s','%s','%s','%s','%s','pending')"%(session['wid'],rid,guest,noof,date)
			insert(q)
			return redirect(url_for("warden.warden_add_guest"))


		q="select * from guest inner join rooms using (room_id) where warden_id='%s'"%(session['wid'])
		data['guest']=select(q)
		
		if 'action' in request.args:
			action=request.args['action']
			gid=request.args['gid']
		else:
			action=None
		
		if action=='delete':
			q="delete from guest where room_id='%s'"%(gid)
			delete(q)
			flash("DELETED...")
			return redirect(url_for('warden.warden_add_guest'))
		

		return render_template("warden_add_guest.html",data=data)
	else:
		return redirect(url_for("public.login"))



@warden.route('/warden_add_messamount',methods=['get','post'])
def warden_add_messamount():
	if not session.get("lid") is None:
		data={}
		sid=request.args['sid']

		if 'btn' in request.form:
			amount=request.form['amount']
			date=request.form['date']
			dur=request.form['dur']

			q="insert into request values(null,'%s','mess','%s','%s','%s','pending')"%(sid,amount,date,dur)
			insert(q)
			flash("Added Successfully")
			return redirect(url_for("warden.warden_home")) 

		q="select * from students inner join request using (student_id) where requested_for ='mess' and student_id='%s'"%(sid)
		data['student']=select(q)

		q="select * from guest inner join rooms using (room_id) "
		data['guest']=select(q)
		
		if 'action' in request.args:
			action=request.args['action']
			gid=request.args['gid']
		else:
			action=None
		
		if action=='delete':
			q="delete from guest where room_id='%s'"%(gid)
			delete(q)
			flash("DELETED...")
			return redirect(url_for('warden.warden_add_messamount'))
		

		return render_template("warden_add_messamount.html",data=data)
	else:
		return redirect(url_for("public.login"))



@warden.route('/warden_add_roomamount',methods=['get','post'])
def warden_add_roomamount():
	if not session.get("lid") is None:
		data={}
		sid=request.args['sid']

		if 'btn' in request.form:
			amount=request.form['amount']
			date=request.form['date']
			dur=request.form['dur']

			q="insert into request values(null,'%s','room','%s','%s','%s','pending')"%(sid,amount,date,dur)
			insert(q)
			flash("Added Successfully")
			return redirect(url_for("warden.warden_home"))

		q="select * from students inner join request using (student_id) where requested_for ='room' and student_id='%s'"%(sid)
		data['student']=select(q)


		q="select * from guest inner join rooms using (room_id) "
		data['guest']=select(q)
		
		if 'action' in request.args:
			action=request.args['action']
			gid=request.args['gid']
		else:
			action=None
		
		if action=='delete':
			q="delete from guest where room_id='%s'"%(gid)
			delete(q)
			flash("DELETED...")
			return redirect(url_for('warden.warden_add_roomamount'))
		

		return render_template("warden_add_roomamount.html",data=data)
	else:
		return redirect(url_for("public.login"))


@warden.route('/warden_enroll_student_to_hostel',methods=['get','post'])
def warden_enroll_student_to_hostel():
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
				q1="SELECT * FROM `students` INNER JOIN `batches` USING(`batch_id`) INNER JOIN `courses` courses ON(`students`.`course_id`=`courses`.`course_id`) where `batches`.`start_year`='%s' AND `batches`.`end_year`='%s' and hostel='yes'"%(syear,eyear)
				res1=select(q1)
				if res1:
					data['stud']=res1
				else:
					flash("No Results Found...")
					return redirect(url_for('warden.warden_enroll_student_to_hostel'))


		if action=='course':
			if 'submit' in request.form:
				cname=request.form['cname']
				q2="SELECT * FROM `students` INNER JOIN `batches` USING(`batch_id`) INNER JOIN `courses` courses ON(`students`.`course_id`=`courses`.`course_id`) where `courses`.`course_name`='%s' and hostel='yes'"%(cname)
				res2=select(q2)
				if res2:
					data['stud1']=res2
				else:
					flash("No Results Found...")
					return redirect(url_for('warden.warden_enroll_student_to_hostel'))

		if action=='name':
			if 'submit' in request.form:
				sname="%"+request.form['sname']+"%"
				q3="SELECT *,CONCAT(`first_name`,' ',`last_name`) AS `sname` FROM `students` INNER JOIN `batches` USING(`batch_id`) INNER JOIN `courses` ON(`students`.`course_id`=`courses`.`course_id`) WHERE `students`.`first_name` and hostel='yes' LIKE '%s'"%(sname)
				print(q3)
				res3=select(q3)
				if res3:
					data['name']=res3
				else:
					flash("No Results Found...")
					return redirect(url_for('warden.warden_enroll_student_to_hostel'))



		q="SELECT * FROM `students` INNER JOIN `batches` USING(`batch_id`) INNER JOIN `courses` courses ON(`students`.`course_id`=`courses`.`course_id`) WHERE hostel='yes'"
		data['students']=select(q)

		return render_template("warden_enroll_student_to_hostel.html",data=data)
	else:
		return redirect(url_for("public.login"))


@warden.route('/warden_assign_hostel',methods=['get','post'])
def warden_assign_hostel():
	if not session.get("lid") is None:
		data={}
		hid=session['hid']
		print(hid)
		data['hid']=hid
		sid=request.args['sid']
		q="SELECT * FROM `rooms` INNER JOIN `hostels` USING(`hostel_id`) WHERE `hostel_id`='%s'"%(sid)
		res=select(q)
		print(res)
		data['rooms']=res
		

		q="SELECT *,concat(first_name,' ',last_name) as sname FROM `student_rooms` INNER JOIN `students` USING(`student_id`) INNER JOIN `rooms` USING(`room_id`) INNER JOIN `hostels` USING(`hostel_id`) WHERE `hostel_id`='%s'"%(hid)
		data['assigned']=select(q)
		if 'submit' in request.form:
			room=request.form['room']
			q="INSERT INTO `student_rooms`(`student_id`,`room_id`,`assigned_date`,`status`) VALUES('%s','%s',curdate(),'assigned')"%(sid,room)
			insert(q)
			flash("Room Assigned...")
			return redirect(url_for('warden.warden_assign_hostel',sid=sid))

		return render_template("warden_assign_hostel.html",data=data)
	else:
		return redirect(url_for("public.login"))

@warden.route('/warden_view_outpass_request')
def warden_view_outpass_request():
	if not session.get("lid") is None:
		data={}
		q="SELECT *,CONCAT(`first_name`,' ',`last_name`) AS sname FROM `out_passes` INNER JOIN `students` ON(`out_passes`.`requested_id`=`students`.`login_id`) WHERE `type`='hostel' and out_passes.status!='cancelled' ORDER BY `out_passes`.`request_date` desc"
		data['outpass']=select(q)  
		if 'action' in request.args:
			action=request.args['action']
			pid=request.args['pid']
		else:
			action=None
		if action=='accept':
			q="update out_passes set status='accepted' where pass_id='%s'"%(pid)     
			update(q)
			flash("ACCEPTED...")
			return redirect(url_for('warden.warden_view_outpass_request'))
		if action=='reject':
			q="update out_passes set status='rejected' where pass_id='%s'"%(pid)
			update(q)
			flash("REJECTED...")
			return redirect(url_for('warden.warden_view_outpass_request'))
		

		return render_template("warden_view_outpass_request.html",data=data)
	else:
		return redirect(url_for("public.login"))

@warden.route('/warden_view_approved_leave_request')
def warden_view_approved_leave_request():
	if not session.get("lid") is None:
		data={}
		hid=session['hid']
		q="SELECT *,leave_requests.status as l_status FROM `leave_requests` INNER JOIN `students` ON(`leave_requests`.`requested_id`=`students`.`login_id`) INNER JOIN `student_rooms` USING(`student_id`) INNER JOIN `rooms` USING(`room_id`) INNER JOIN `hostels` USING(`hostel_id`) WHERE `hostel_id`='%s' and leave_requests.status='accepted' ORDER BY leave_requests.date_time desc "%(hid)
		data['leave']=select(q)
		

		return render_template("warden_view_approved_leave_request.html",data=data)
	else:
		return redirect(url_for("public.login"))


@warden.route('/warden_view_latecoming')
def warden_view_latecoming():
	if not session.get("lid") is None:
		hid=session['hid']
		data={}
		q="SELECT * FROM `late_coming` INNER JOIN `students` USING(`student_id`) INNER JOIN `student_rooms` USING(`student_id`) INNER JOIN `rooms` USING(`room_id`) INNER JOIN hostels USING(`hostel_id`) WHERE `hostel_id`='%s' ORDER BY late_coming.date_time DESC "%(hid)
		data['late']=select(q)
		

		return render_template("warden_view_latecoming.html",data=data)
	else:
		return redirect(url_for("public.login"))

	
@warden.route('/warden_view_payment')
def warden_view_payment():
	if not session.get("lid") is None:
		rid=request.args['rid']
		data={}
		q="select * from payment where request_id='%s'"%(rid)
		data['outpass']=select(q)
		

		return render_template("warden_view_payment.html",data=data)
	else:
		return redirect(url_for("public.login"))