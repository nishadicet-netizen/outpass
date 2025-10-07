
@public.route('/login',methods=['get','post'])
def login():
	session.clear()
	if 'forgotpassword' in request.form:	
		return redirect(url_for('public.forgotpassword'))

	if 'submit' in request.form:
		uname=request.form['uname']
		pwd=request.form['pwd']
		q="select * from login where username='%s' and password='%s'"%(uname,pwd)
		res=select(q)

		if res:
			session['lid']=res[0]['login_id']
			if res[0]['usertype']=='admin':
				flash("login successfully")
				return redirect(url_for('admin.admin_home'))
			
			elif res[0]['usertype']=='teacher':
				q1="select * from teachers where login_id='%s'"%(session['lid'])
				res1=select(q1) 
				print(res1)
				if res1:

					session['tid']=res1[0]['teacher_id']
					q="select *,concat(first_name,' ',last_name) as `t_name` from teachers where teacher_id='%s'"%(session['tid'])
					res=select(q)
					session['t_name']=res[0]['t_name']


					q="SELECT teacher_id,hod_id,dept_id FROM `teachers` INNER JOIN `hod` USING(hod_id) INNER JOIN `department` USING(dept_id) where teacher_id='%s'"%(session['tid'])
					r=select(q)
					print(q)
					if r:
						session['dept_id']=r[0]['dept_id'] 

					flash("login successfully")
					return redirect(url_for('teacher.teacher_home'))
			elif res[0]['usertype']=='principal':
				q1="select * from principal where login_id='%s'"%(session['lid'])
				res1=select(q1)
				print(res1)
				if res1:

					session['pid']=res1[0]['principal_id']
					q="select *,concat(fname,' ',lname) as `p_name` from principal where principal_id='%s'"%(session['pid'])
					res=select(q)
					session['p_name']=res[0]['p_name']
					flash("login successfully")
					return redirect(url_for('principal.principal_home'))
			elif res[0]['usertype']=='hod':
				q1="select * from hod where login_id='%s'"%(session['lid'])
				res1=select(q1)
				print(res1)
				if res1:

					session['hod']=res1[0]['hod_id']
					session['dept_id']=res1[0]['dept_id']
					q="select *,concat(fname,' ',lname) as `h_name` from hod where hod_id='%s'"%(session['hod'])
					res=select(q)
					session['h_name']=res[0]['h_name']
					flash("login successfully")
					return redirect(url_for('hod.hod_home'))


			elif res[0]['usertype']=='student':
				q1="SELECT *,CONCAT(`first_name`,' ',`last_name`)AS `name` FROM `students` INNER JOIN `batches` USING(`batch_id`) INNER JOIN `courses` ON `students`.`course_id`=`courses`.`course_id` WHERE login_id='%s'"%(session['lid'])
				res1=select(q1)
				session['sname']=res1[0]['name']
				if res1:
					flash('Welcome'+session['sname'])

					session['sid']=res1[0]['student_id']
					session['sname']=res1[0]['name']
					session['syear']=res1[0]['start_year']
					session['eyear']=res1[0]['end_year']
					session['cname']=res1[0]['course_name']
					session['hname']=res1[0]['house_name']
					session['place']=res1[0]['place']
					session['pmail']=res1[0]['parent_email']
					session['phone']=res1[0]['phone']
					session['email']=res1[0]['email']
					flash("login successfully")
					return redirect(url_for('student.student_home'))
			elif res[0]['usertype']=='warden':
				q1="select * from wardens where login_id='%s'"%(session['lid'])
				res1=select(q1)
				print(res1)
				if res1:

					session['wid']=res1[0]['warden_id']
					q="select *,concat(first_name,' ',last_name) as `w_name` from wardens where warden_id='%s'"%(session['wid'])
					res=select(q)
					session['w_name']=res[0]['w_name']
					session['hid']=res[0]['hostel_id']
					print(session['hid'])
					flash("login successfully")
					return redirect(url_for('warden.warden_home',))
			elif res[0]['usertype']=='guard':
				q1="select * from security_guards where login_id='%s'"%(session['lid'])
				res1=select(q1)
				print(res1)
				if res1:

					session['gid']=res1[0]['guard_id']
					q="select *,concat(first_name,' ',last_name) as `g_name` from security_guards where guard_id='%s'"%(session['gid'])
					res=select(q)
					session['g_name']=res[0]['g_name']
					# session['hid']=res[0]['hostel_id']
					# print(session['hid'])
					flash("login successfully")
					return redirect(url_for('security.security_home'))
		else:
			flash('Invalid username & password')

	return render_template('login.html')




@public.route('/forgotpassword',methods=['get','post'])
def forgotpassword():
	data={}
	if 'next' in request.form:
		ph=request.form['ph']
		uname=request.form['uname']
		q="SELECT email,username FROM login INNER JOIN `principal` USING(login_id) WHERE username='%s' AND email='%s' UNION SELECT email,username FROM login INNER JOIN `hod` USING(login_id) WHERE username='%s' AND email='%s' "%(uname,ph,uname,ph)
		print(q)
		res=select(q)
		print(res)
		if res:
			print(res)
			session['uname']=res[0]['username']
			return redirect(url_for('public.enterotp'))
	return render_template("forgotpassword.html",data=data)



@public.route('/enterotp',methods=['get','post'])
def enterotp():
	data={}
	uname=session['uname']
	data['chp']=uname
	

	if 'update' in request.form:
		uname=request.form['uname']
		p=request.form['pwd']
		cp=request.form['pwds']
		if p==cp:
			print("+++++++++++")
			q="update login set password='%s' where username='%s'"%(p,uname)
			update(q)
			flash("UPDATED SUCCESSFULLY")
			return redirect(url_for('public.login'))
		else:
			flash("PASSWORD MISMATCH")
			data['chp']=uname
	return render_template("enterotp.html",data=data)