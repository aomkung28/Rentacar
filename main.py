from flask import *
app = Flask(__name__)



@app.route("/")
def dashboard():
    return render_template('dashboard.html')

@app.route("/booking")
def booking():
    return render_template('booking.html')


if __name__ == "__main__":
    app.run(debug=True)