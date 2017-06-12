from flask import *
app = Flask(__name__)



@app.route("/")
def dashboard():
    return render_template('dashboard.html')

@app.route("/booking")
def booking():
    return render_template('booking.html')

@app.route("/car")
def car():
    return render_template('car.html')


@app.route("/profile")
def profile():
    print request.path
    return render_template('profile.html')

@app.route("/report")
def report():
    return render_template('report.html')

@app.route("/invoice")
def invoice():
    print Request.path
    return render_template('invoice.html')
    
@app.route("/register")
def register():
	print Request.path
	return render_template('register.html')
    
@app.route("/login")
def login():
		print Request.path
		return render_template('login.html')
    

if __name__ == "__main__":
    app.run(debug=True)
