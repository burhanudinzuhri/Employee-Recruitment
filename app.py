from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL, MySQLdb
import bcrypt 
from model import load, predict_data


# flask dir
app = Flask(__name__)
app.secret_key = "Internship1"

# connect database
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'hr_data_2'
mysql = MySQL(app)

# load model dan scaler
load()

# function display card employee candidate joined
def card_view_joined():
    cursor = mysql.connection.cursor()
    cursor.execute('''SELECT * FROM employees WHERE Status = "Joined" ''')
    count_joined = str(cursor.rowcount)
    return count_joined

# function display card employee candidate not joined
def card_view_not_joined():
    cursor = mysql.connection.cursor()
    cursor.execute('''SELECT * FROM employees WHERE Status = "Not Joined" ''')
    card_view_not_joined = str(cursor.rowcount)
    return card_view_not_joined

# function display employee candidate male joined
def view_male_joined():
    cursor = mysql.connection.cursor()
    cursor.execute('''SELECT * FROM employees WHERE Gender = "Male" AND Status = "Joined" ''')
    count_male_joined = str(cursor.rowcount)
    return count_male_joined

# function display employee candidate male not joined
def view_male_not_joined():
    cursor = mysql.connection.cursor()
    cursor.execute('''SELECT * FROM employees WHERE Gender = "Male" AND Status = "Not Joined" ''')
    count_male_not_joined = str(cursor.rowcount)
    return count_male_not_joined

# function display employee candidate female joined
def view_female_joined():
    cursor = mysql.connection.cursor()
    cursor.execute('''SELECT * FROM employees WHERE Gender = "Female" AND Status = "Joined" ''')
    count_female_joined = str(cursor.rowcount)
    return count_female_joined

# function display employee candidate female not joined
def view_female_not_joined():
    cursor = mysql.connection.cursor()
    cursor.execute('''SELECT * FROM employees WHERE Gender = "Female" AND Status = "Not Joined" ''')
    count_female_not_joined = str(cursor.rowcount)
    return count_female_not_joined

# function display employee candidate agency joined
def view_agency_joined():
    cursor = mysql.connection.cursor()
    cursor.execute('''SELECT * FROM employees WHERE Candidate_Source = "Agency" AND Status = "Joined" ''')
    count_agency_joined = str(cursor.rowcount)
    return count_agency_joined

# function display employee candidate agency not joined
def view_agency_not_joined():
    cursor = mysql.connection.cursor()
    cursor.execute('''SELECT * FROM employees WHERE Candidate_Source = "Agency" AND Status = "Not Joined" ''')
    count_agency_not_joined = str(cursor.rowcount)
    return count_agency_not_joined

# function display employee candidate direct joined
def view_direct_joined():
    cursor = mysql.connection.cursor()
    cursor.execute('''SELECT * FROM employees WHERE Candidate_Source = "Direct" AND Status = "Joined" ''')
    count_direct_joined = str(cursor.rowcount)
    return count_direct_joined

# function display employee candidate direct not joined
def view_direct_not_joined():
    cursor = mysql.connection.cursor()
    cursor.execute('''SELECT * FROM employees WHERE Candidate_Source = "Direct" AND Status = "Not Joined" ''')
    count_direct_not_joined = str(cursor.rowcount)
    return count_direct_not_joined

# function display employee candidate referral joined
def view_referral_joined():
    cursor = mysql.connection.cursor()
    cursor.execute('''SELECT * FROM employees WHERE Candidate_Source = "Employee Referral" AND Status = "Joined" ''')
    count_referral_joined = str(cursor.rowcount)
    return count_referral_joined

# function display employee candidate referral not joined
def view_referral_not_joined():
    cursor = mysql.connection.cursor()
    cursor.execute('''SELECT * FROM employees WHERE Candidate_Source = "Employee Referral" AND Status = "Not Joined" ''')
    count_referral_not_joined = str(cursor.rowcount)
    return count_referral_not_joined

# route login function
@app.route('/login', methods=['POST'])
def login(): 
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password'].encode('utf-8')
        curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        curl.execute("SELECT * FROM users WHERE username=%s",(username,))
        user = curl.fetchone()
        curl.close()
        if user is not None and len(user) > 0 :
            if bcrypt.hashpw(password, user['password'].encode('utf-8')) == user['password'].encode('utf-8'):
                session['username'] = user ['username']
                session['email'] = user['email']
                return redirect(url_for('home'))
            else :
                flash("Gagal, Email dan Password Tidak Cocok")
                return redirect(url_for('validation'))
        else :
            flash("Gagal, User Tidak Ditemukan")
            return redirect(url_for('validation'))
    else: 
        return render_template("validation.html")

# route register function
@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password'].encode('utf-8')
        hash_password = bcrypt.hashpw(password, bcrypt.gensalt())
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (username,email,password) VALUES (%s,%s,%s)" ,(username, email, hash_password)) 
        mysql.connection.commit()
        session['username'] = request.form['username']
        session['email'] = request.form['email']
        return redirect(url_for('validation'))

# route logout function
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('validation')) 

# route validation page
@app.route('/validation')
def validation():
    return render_template('validation.html')

# route index page
@app.route('/')
def home():
    if 'username' in session:
        count_joined = card_view_joined()
        count_not_joined = card_view_not_joined()
        count_male_joined = view_male_joined()
        count_male_not_joined = view_male_not_joined()
        count_female_joined = view_female_joined()
        count_female_not_joined = view_female_not_joined()
        count_agency_joined = view_agency_joined()
        count_agency_not_joined = view_agency_not_joined()
        count_direct_joined = view_direct_joined()
        count_direct_not_joined = view_direct_not_joined()
        count_referral_joined = view_referral_joined()
        count_referral_not_joined = view_referral_not_joined()
        return render_template('index.html', count_joined=count_joined, count_not_joined=count_not_joined, count_male_joined=count_male_joined, count_male_not_joined=count_male_not_joined, count_female_joined=count_female_joined, count_female_not_joined=count_female_not_joined,  count_agency_joined=count_agency_joined, count_agency_not_joined=count_agency_not_joined, count_direct_joined=count_direct_joined, count_direct_not_joined=count_direct_not_joined, count_referral_joined=count_referral_joined, count_referral_not_joined=count_referral_not_joined)
    else:
        return redirect(url_for('validation'))

# route employee candidate
@app.route('/employee')
def employee():
    if 'username' in session:
        cursor = mysql.connection.cursor() #connect database 
        cursor.execute('''SELECT * FROM employees ORDER BY id DESC LIMIT 50''')
        employee=cursor.fetchall()
        cursor.close()
        booleans=['Yes', 'No']
        offered_band =	{
            "E0": "Software Engineer",
            "E1": "Senior Software Engineer",
            "E2": "Team Leader",
            "E3": "Project Manager"
            }
        gender=['Male', 'Female']
        candidate_source =	{
            "Agency": "Agency",
            "Direct": "Direct",
            "Employee Referral": "Employee Referral"
            }
        lob =	{
            "AXON": "Autonomous eXtended On-Officer Network",
            "BFSI": "Banking Financial Services and Insurance",
            "CSMP": "Consultant Site Management Plan",
            "EAS": "Electronic Subcontracting",
            "ERS": "Equipment Reutilization Solutions",
            "ETS": "Educational Testing Service",
            "Healthcare": "Healthcare",
            "INFRA": "Infrastructure Finance",
            "MMS": "Maintenance Management Solutions",
            }
        location =	{
            "Ahmedabad": "Ahmedabad",
            "Bangalore": "Bangalore",
            "Chennai": "Chennai",
            "Cochin": "Cochin",
            "Gurgaon": "Gurgaon",
            "Hyderabad": "Hyderabad",
            "Kolkata": "Kolkata",
            "Mumbai": "Mumbai",
            "Noida": "Noida",
            "Pune": "Pune",
            "Others": "Others"
            }
        return render_template('employee.html', employee=employee, data_att=[booleans, offered_band, gender, candidate_source, lob, location])
    else:
        return redirect(url_for('validation'))
    
# route employee candidate joined
@app.route('/employee_joined')
def employee_joined():
    if 'username' in session:
        cursor = mysql.connection.cursor() #connect database 
        cursor.execute('''SELECT * FROM employees WHERE Status = "Joined" ORDER BY id DESC LIMIT 50''')
        employee_joined = cursor.fetchall() 
        cursor.close()
        return render_template('employee_joined.html', employee_joined=employee_joined)
    else:
        return redirect(url_for('validation'))

# route employee candidate not joined
@app.route('/employee_not_joined')
def employee_not_joined():
    if 'username' in session:
        cursor = mysql.connection.cursor() #connect database 
        cursor.execute('''SELECT * FROM employees WHERE Status = "Not Joined" ORDER BY id DESC LIMIT 50''')
        employee_not_joined = cursor.fetchall()
        cursor.close()
        return render_template('employee_not_joined.html', employee_not_joined=employee_not_joined)
    else:
        return redirect(url_for('validation'))
    
# route add employee candidate data
@app.route('/employee/add', methods=['POST'])
def tambahemployee():    
        name = request.form['name']
        doj_extended = request.form['doj_extended']
        duration_to_accept_the_offer = request.form['duration_to_accept_the_offer']
        notice_period = request.form['notice_period']
        offered_band = request.form['offered_band']
        percent_hike_expected_in_ctc = request.form['percent_hike_expected_in_ctc']
        percent_hike_offered_in_ctc = request.form['percent_hike_offered_in_ctc']
        percent_difference_ctc = request.form['percent_difference_ctc']
        joining_bonus = request.form['joining_bonus']
        candidate_relocate_actual = request.form['candidate_relocate_actual']
        gender = request.form['gender']
        candidate_source = request.form['candidate_source']
        rex_in_yrs = request.form['rex_in_yrs']
        lob = request.form['lob']
        location = request.form['location']
        age = request.form['age']
        data_input = [doj_extended, duration_to_accept_the_offer, notice_period, offered_band, percent_hike_expected_in_ctc, percent_hike_offered_in_ctc, percent_difference_ctc, joining_bonus, candidate_relocate_actual, gender, candidate_source, rex_in_yrs, lob, location, age]
        status = predict_data(data_input)
        cursor = mysql.connection.cursor()
        cursor.execute('''INSERT INTO employees (Name, DOJ_Extended, Duration_to_accept_offer, Notice_period, Offered_band, Pecent_hike_expected_in_CTC, Percent_hike_offered_in_CTC, Percent_difference_CTC, Joining_Bonus, Candidate_relocate_actual, Gender, Candidate_Source, Rex_in_Yrs, LOB, Location, Age, Status, proba)
                       VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''',
                       (name, doj_extended, duration_to_accept_the_offer, notice_period, offered_band, percent_hike_expected_in_ctc, percent_hike_offered_in_ctc, percent_difference_ctc, joining_bonus, candidate_relocate_actual, gender, candidate_source, rex_in_yrs, lob, location, age, status[0], status[1]))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('employee'))

# route edit employee candidate data
@app.route('/employee/edit/<int:id>', methods=['GET', 'POST'])
def editemployee(id):     
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        cursor.execute(''' SELECT * FROM employees WHERE ID = %s''', (id, ))
        employee = cursor.fetchone()
        cursor.close()
        return redirect(url_for('employee'))
    else:
        name = request.form['name']
        doj_extended = request.form['doj_extended']
        duration_to_accept_the_offer = request.form['duration_to_accept_the_offer']
        notice_period = request.form['notice_period']
        offered_band = request.form['offered_band']
        percent_hike_expected_in_ctc = request.form['percent_hike_expected_in_ctc']
        percent_hike_offered_in_ctc = request.form['percent_hike_offered_in_ctc']
        percent_difference_ctc = request.form['percent_difference_ctc']
        joining_bonus = request.form['joining_bonus']
        candidate_relocate_actual = request.form['candidate_relocate_actual']
        gender = request.form['gender']
        candidate_source = request.form['candidate_source']
        rex_in_yrs = request.form['rex_in_yrs']
        lob = request.form['lob']
        location = request.form['location']
        age = request.form['age']
        data_input = [doj_extended, duration_to_accept_the_offer, notice_period, offered_band, percent_hike_expected_in_ctc, percent_hike_offered_in_ctc, percent_difference_ctc, joining_bonus, candidate_relocate_actual, gender, candidate_source, rex_in_yrs, lob, location, age]
        status = predict_data(data_input)
        cursor = mysql.connection.cursor()
        cursor.execute('''UPDATE employees SET Name = %s, DOJ_Extended = %s, Duration_to_accept_offer = %s, Notice_period = %s, Offered_band = %s, Pecent_hike_expected_in_CTC = %s, Percent_hike_offered_in_CTC = %s, Percent_difference_CTC = %s, Joining_Bonus = %s, Candidate_relocate_actual = %s, Gender = %s, Candidate_Source = %s, Rex_in_Yrs = %s, LOB = %s, Location = %s, Age = %s, Status = %s, proba= %s WHERE ID = %s
        ''',(name, doj_extended, duration_to_accept_the_offer, notice_period, offered_band, percent_hike_expected_in_ctc, percent_hike_offered_in_ctc, percent_difference_ctc, joining_bonus, candidate_relocate_actual, gender, candidate_source, rex_in_yrs, lob, location, age, status[0], status[1],id))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('employee'))
    
# route delete employee candidate data
@app.route('/employee/delete/<int:id>', methods=['GET'])
def deleteemployee(id):     
    cursor = mysql.connection.cursor()
    cursor.execute(''' DELETE FROM employees WHERE ID = %s''', (id, ))
    mysql.connection.commit()
    cursor.close()
    return redirect(url_for('employee'))

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)