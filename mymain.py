from flask import  Flask, render_template,request,redirect,url_for,session
import pymysql


app=Flask(__name__)
app.secret_key="super secret key"


@app.route("/")
def  welcome():
	 return render_template("welcome.html")

@app.route("/login",methods=["GET","POST"])
def login():
	if(request.method=="POST"):
		email=request.form["T1"]
		password=request.form["T2"]
		cn = pymysql.Connect(host="localhost", port=3306, db="medical_finder", passwd="", user="root",
		                     autocommit="true")
		
		sql = "select * from logindata where email='"+email+"' AND password='"+password+"'"
		cur = cn.cursor()
		cur.execute(sql)
		n=cur.rowcount
		if(n>0): #Correct email and password
			data=cur.fetchone()
			ut=data[2]
			#create session
			session["usertype"]=ut
			session["email"]=email
			#send to page
			if(ut=="admin"):
				return redirect(url_for("adminhome"))
			elif(ut=="medical"):
				return redirect(url_for("medicalhome"))
		else:
			return render_template("login.html",msg="Invalid email or password")
	else:
		return render_template("login.html")

@app.route("/logout")
def logout():
	if("usertype" in session):
		session.pop("usertype",None)
		session.pop("email",None)
		return redirect(url_for("login"))
	else:
		return redirect(url_for("login"))
@app.route("/auth_error")
def auth_error():
	return render_template("authorization_error.html")
@app.route("/adminhome",methods=["GET","POST"])
def adminhome():
	if("usertype" in session):
		ut=session["usertype"]
		if(ut=="admin"):
			return render_template("adminhome.html")
		else:
			return redirect(url_for("auth_error"))
	else:
		return redirect(url_for("auth_error"))

@app.route("/medicalhome",methods=["GET","POST"])
def medicalhome():
	if("usertype" in session):
		ut=session["usertype"]
		if(ut=="medical"):
			return render_template("medicalhome.html")
		else:
			return redirect(url_for("auth_error"))

	else:
		return redirect(url_for("auth_error"))


@app.route("/admin_reg",methods=["GET","POST"])
def adminReg():
	if ("usertype" in session):
		ut = session["usertype"]
		if (ut == "admin"):

			if (request.method == "GET"):
				return render_template("adminReg.html")
			else:
				name = request.form["a1"]
				address = request.form["a2"]
				contact = request.form["a3"]
				email = request.form["a4"]
				password = request.form["a5"]
				cn = pymysql.Connect(host="localhost", port=3306, db="medical_finder", passwd="", user="root",
									 autocommit="true")

				sql2 = "insert into adminData values('" + name + "','" + address + "','" + contact + "','" + email + "')"
				cur = cn.cursor()
				cur.execute(sql2)
				n = cur.rowcount

				if (n == 1):
					return render_template("adminReg.html", msg="saved")
				else:
					return render_template("adminReg.html", msg="not saved")

		else:
			return redirect(url_for("auth_error"))
	else:
		return redirect(url_for("auth_error"))


		

@app.route("/medical_reg",methods=["GET","POST"])
def medical_reg():
	if ("usertype" in session):
		ut = session["usertype"]
		if (ut == "admin"):
			if (request.method == "GET"):
				return render_template("MedicalReg.html")
			else:
				# receive form data
				name = request.form["t1"]
				owner = request.form["t2"]
				lno = request.form["t3"]
				address = request.form["t4"]
				landmark = request.form["t5"]
				contact = request.form["t6"]
				email = request.form["t7"]
				password = request.form["t8"]
				usertype = "medical"
				cn = pymysql.Connect(host="localhost", port=3306, db="medical_finder", passwd="", user="root",
									 autocommit="true")

				sql = "insert into medicaldata values('" + name + "','" + owner + "','" + lno + "','" + address + "','" + landmark + "','" + contact + "','" + email + "')";

				cur = cn.cursor()
				cur.execute(sql)
				n = cur.rowcount

				sql1 = "insert into logindata values('" + email + "','" + password + "','" + usertype + "')"
				cur = cn.cursor()
				cur.execute(sql1)
				n = cur.rowcount

				if (n == 1):
					return render_template("MedicalReg.html", msg="saved")
				else:
					return render_template("MedicalReg.html", msg="not saved")
		else:
			return redirect(url_for("auth_error"))
	else:
		return redirect(url_for("auth_error"))

			
@app.route("/customerReg", methods=["GET", "POST"])
def customerReg():
	if (request.method == "GET"):
	    return render_template("customerReg.html")
	else:
		
		cname=request.form["t1"]
		address=request.form["t2"]
		landmark=request.form["t3"]
		contact=request.form["t4"]
		email=request.form["t5"]
		
		
		cn = pymysql.Connect(host="localhost", port=3306, db="medical_finder", passwd="", user="root",
		                     autocommit="true")
		
		sql4 = "insert into customerinfo values( 0,'"+cname+"','"+address+"','"+landmark+"','"+contact+"','"+email+"')";
		
		cur = cn.cursor()
		cur.execute(sql4)
		n = cur.rowcount
		
		if(n==1):
			return render_template("customerReg.html",msg="your data has been saved")
		else:
			return render_template("customerReg.html", msg="your data has not been saved")
		
		
		
	


@app.route("/customerdetails")
def customerdetails():
	cn = pymysql.connect(
		host="localhost",
		port=3306,
		user="root",
		db="medical_finder",
		passwd="",
		autocommit=True
	)
	
	me4 = "select * from customerinfo";
	cur = cn.cursor()
	cur.execute(me4)
	n = cur.rowcount
	if (n > 0):
		data = cur.fetchall()
		return render_template("customerdetails.html", kota=data)
	else:
		return render_template("customerdetails.html", msg="no data found")
	
	
@app.route("/edit_customer" , methods=["GET","POST"])
def edit_customer():
	if(request.method == "GET"):
		return redirect(url_for("customerdetails"))
	elif(request.method == "POST"):
		e4=request.form["H1"]
		cn = pymysql.connect(
			host="localhost",
			port=3306,
			user="root",
			db="medical_finder",
			passwd="",
			autocommit=True
		)
		
		me4= "select * from customerinfo where email='"+e4+"' "
		cur= cn.cursor()
		cur.execute(me4)
		n = cur.rowcount
		if (n > 0):
			data = cur.fetchone()
			return render_template("EditCustomer.html", kota=data)
		else:
			return render_template("EditCustomer.html", msg="no data found")
		
		
@app.route("/edit_customer1" , methods=["GET" , "POST"])
def edit_customer1():
	if (request.method == "GET"):
		return redirect(url_for("customerdetails"))
	elif(request.method == "POST"):
		customer_id= request.form["h1"]
		customername= request.form["t1"]
		address= request.form["t2"]
		landmark= request.form["t3"]
		conatct=request.form["t4"]
		email=request.form["t5"]
		
		cn= pymysql.connect(
			host="localhost",
			port=3306,
			user="root",
			db="medical_finder",
			passwd="",
			autocommit=True
			
		)
		me4 = "update customerinfo set cName ='"+cName+"', address= '"+address+"',landmark= '"+landmark+"',contact='"+conatct+"' where email='"+email+"' "
		cur= cn.cursor()
		cur.execute(me4)
		n= cur.rowcount
		if(n>0):
			return render_template("EditCustomer1.html", msg="your data has been changed")
		else:
			return render_template("EditCustomer1.html",msg="error: try again")
	
	
	
	



@app.route("/medicine", methods=["GET", "POST"])
def medicine():
	if ("usertype" in session):
		ut = session["usertype"]
		if (ut == "medical"):
			if (request.method == "GET"):
				return render_template("medicine.html")
			else:

				med_name = request.form["q1"]
				comp_name = request.form["q2"]
				lno = request.form["q3"]
				med_type = request.form["q4"]
				price = request.form["q5"]

				cn = pymysql.Connect(host="localhost", port=3306, db="medical_finder", passwd="", user="root",
									 autocommit="true")

				sql3 = "insert into medicinedata values( 0,'" + med_name + "','" + comp_name + "','" + lno + "','" + med_type + "','" + price + "')";

				cur = cn.cursor()
				cur.execute(sql3)
				n = cur.rowcount

				if (n == 1):
					return render_template("medicine.html", msg="'your data has been saved")
				else:
					return render_template("medicine.html", msg="'your data has not been saved")


		else:
			return redirect(url_for("auth_error"))

	else:
		return redirect(url_for("auth_error"))

##admin.details##
@app.route("/admindetails")
def admindetails():
	if ("usertype" in session):
		ut = session["usertype"]
		if (ut == "admin"):
			cn = pymysql.connect(
				host="localhost",
				port=3306,
				db="medical_finder",
				passwd="",
				user="root",
				autocommit="true"
			)
			me1 = "select*from admindata";
			cur = cn.cursor()
			cur.execute(me1)
			n = cur.rowcount
			if (n > 0):
				data = cur.fetchall()
				return render_template("admindetails.html", kota=data)
			else:
				return render_template("admindetails.html", msg="no data found")

		else:
			return redirect(url_for("auth_error"))
	else:
		return redirect(url_for("auth_error"))


	
	
	
	
	
	
	
	
	
@app.route("/medicaldetails")
def medicaldetails():
	if ("usertype" in session):
		ut = session["usertype"]
		if (ut == "admin"):
			cn = pymysql.connect(
				host="localhost",
				port=3306,
				db="medical_finder",
				passwd="",
				user="root",
				autocommit=True
			)
			me2 = "select * from medicaldata";
			cur = cn.cursor()
			cur.execute(me2)
			n = cur.rowcount
			if (n > 0):
				data = cur.fetchall()
				return render_template("medicaldetails.html", kota=data)
			else:
				return render_template("medicaldetails.html", msg="no data found")
		else:
			return redirect(url_for("auth_error"))
	else:
		return redirect(url_for("auth_error"))

		
@app.route("/edit_medical",methods=["GET","POST"])
def edit_medicals():
	if ("usertype" in session):
		ut = session["usertype"]
		if (ut == "admin"):
			if (request.method == "GET"):
				return redirect(url_for("medicaldetails"))
			elif (request.method == "POST"):
				e1 = request.form["H1"]  # grab key email from post request
				cn = pymysql.connect(
					host="localhost",
					port=3306,
					db="medical_finder",
					passwd="",
					user="root",
					autocommit=True
				)
				me2 = "select * from medicaldata where email='" + e1 + "'";
				cur = cn.cursor()
				cur.execute(me2)
				n = cur.rowcount
				if (n > 0):
					data = cur.fetchone()
					return render_template("EditMedical.html", kota=data)
				else:
					return render_template("EditMedical.html", msg="no data found")

		else:
			return redirect(url_for("auth_error"))
	else:
		return redirect(url_for("auth_error"))

@app.route("/edit_medical1",methods=["GET","POST"])
def edit_medical():
	if ("usertype" in session):
		ut = session["usertype"]
		if (ut == "admin"):
			if (request.method == "GET"):
				return redirect(url_for("medicaldetails"))
			elif (request.method == "POST"):
				name = request.form["t1"]
				owner = request.form["t2"]
				lno = request.form["t3"]
				address = request.form["t4"]
				landmark = request.form["t5"]
				contact = request.form["t6"]
				email = request.form["t7"]
				cn = pymysql.connect(
					host="localhost",
					port=3306,
					db="medical_finder",
					passwd="",
					user="root",
					autocommit=True
				)
				me2 = "update medicaldata set name='" + name + "',owner='" + owner + "',lno='" + lno + "',address='" + address + "',landmark='" + landmark + "',contact='" + contact + "'where email='" + email + "'  ";
				cur = cn.cursor()
				cur.execute(me2)
				n = cur.rowcount
				if (n > 0):
					data = cur.fetchone()
					return render_template("EditMedical1.html", msg="Data changes are saved successfully")
				else:
					return render_template("EditMedical1.html", msg="Error  :  Try again")

		else:
			return redirect(url_for("auth_error"))
	else:
		return redirect(url_for("auth_error"))

	 
		
		
		
		
		
		
		
		
@app.route("/medicinedetails")
def medicinedetails():
	if ("usertype" in session):
		ut = session["usertype"]
		if (ut == "medical"):
			cn = pymysql.connect(
				host="localhost",
				port=3306,
				db="medical_finder",
				passwd="",
				user="root",
				autocommit=True
			)
			me3 = "select * from medicinedata";
			cur = cn.cursor()
			cur.execute(me3)
			n = cur.rowcount
			if (n > 0):
				data = cur.fetchall()
				return render_template("medicinedetails.html", kota=data)
			else:
				return render_template("medicinedetails.html", msg="no data found")

		else:
			return redirect(url_for("auth_error"))

	else:
		return redirect(url_for("auth_error"))

@app.route("/edit_medicine",methods=["GET","POST"])
def edit_medicine():
	if ("usertype" in session):
		ut = session["usertype"]
		if (ut == "medical"):
			if (request.method == "GET"):
				return redirect(url_for("medicinedetails"))
			elif (request.method == "POST"):
				e3 = request.form["H1"]
				cn = pymysql.connect(host="localhost",
									 port=3306,
									 user="root",
									 passwd="",
									 db="medical_finder",
									 autocommit=True)

				me3 = "select * from medicinedata where med_id='" + e3 + "'"
				cur = cn.cursor()
				cur.execute(me3)
				n = cur.rowcount
				if (n > 0):
					data = cur.fetchone()
					return render_template("EditMedicine.html", kota=data)
				else:
					return render_template("EditMedicine.html", msg="Data Not Found")
		else:
			return redirect(url_for("auth_error"))

	else:
		return redirect(url_for("auth_error"))


@app.route("/edit_medicine1",methods=["GET","POST"])
def edit_medicine1():
	if ("usertype" in session):
		ut = session["usertype"]
		if (ut == "medical"):
			if (request.method == "GET"):
				return redirect(url_for("medicinedetails"))
			elif (request.method == "POST"):
				med_id = request.form["H1"]
				med_name = request.form["q1"]
				cname = request.form["q2"]
				lno = request.form["q3"]
				med_type = request.form["q4"]
				price = request.form["q5"]

				cn = pymysql.connect(host="localhost",
									 port=3306,
									 user="root",
									 passwd="",
									 db="medical_finder",
									 autocommit=True)
				me3 = "update medicinedata set med_name='" + med_name + "', comp_name='" + cname + "', lno='" + lno + "', med_type='" + med_type + "',unit_price='" + price + "' where med_id=" + med_id
				print(me3)
				cur = cn.cursor()
				cur.execute(me3)
				n = cur.rowcount
				if (n > 0):
					return render_template("EditMedicine1.html", msg="Data Changes Are Saved Successfully")
				else:
					return render_template("EditMedicine1.html", msg="ERROR : Try Agian")

		else:
			return redirect(url_for("auth_error"))

	else:
		return redirect(url_for("auth_error"))













if __name__ == "__main__":
	app.run(debug=True)