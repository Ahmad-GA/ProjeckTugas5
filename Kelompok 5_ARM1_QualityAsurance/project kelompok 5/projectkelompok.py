from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL, MySQLdb
import bcrypt
import random
import datetime
import time
from flask import Markup
from flask import Flask

app = Flask(__name__)
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Jenengmu28'
app.config['MYSQL_DB'] = 'db_bengkelweb'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)


# Home
@app.route('/')
def home():
    return render_template("home1.html")

# End Home

# About
@app.route('/about')
def about():
    return render_template("about.html")
# End About

# Login User
@app.route('/login1', methods=["GET", "POST"])
def login1():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password'].encode('utf-8')
        hash_password = bcrypt.hashpw(password, bcrypt.gensalt())

        curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        curl.execute("SELECT * FROM user_managemen WHERE email=%s", (email,))
        user = curl.fetchone()
        curl.close()

        if len(user) > 0:
            if bcrypt.hashpw(password, user["password"].encode('utf-8')) == user["password"].encode('utf-8'):
                session['name'] = user['name']
                session['email'] = user['email']
                return render_template("home2.html")
            else:
                return "Error password and email not match"
        else:
            return "Error user not found"
    else:
        return render_template("login1.html")
# End Login User

# Login Admin
@app.route('/login2', methods=["GET", "POST"])
def login2():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password'].encode('utf-8')
        hash_password = bcrypt.hashpw(password, bcrypt.gensalt())

        curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        curl.execute("SELECT * FROM user_managemen WHERE email=%s", (email,))
        user = curl.fetchone()
        curl.close()

        if len(user) > 0:
            if bcrypt.hashpw(password, user["password"].encode('utf-8')) == user["password"].encode('utf-8'):
                session['name'] = user['name']
                session['email'] = user['email']
                return render_template("home1.html")
            else:
                return "Error password and email not match"
        else:
            return "Error user not found"
    else:
        return render_template("login2.html")
# End Login Admin

# Register

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    else:
        name = request.form['name']
        email = request.form['email']
        password = request.form['password'].encode('utf-8')
        password = bcrypt.hashpw(password, bcrypt.gensalt())
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO user_managemen (name, email, password) VALUES (%s,%s,%s)",
                    (name, email, password))
        mysql.connection.commit()
        session['name'] = request.form['name']
        session['email'] = request.form['email']
        return redirect(url_for('home'))

# End Register

# Logout

@app.route('/logout1', methods=["GET", "POST"])
def logout():
    session.clear()
    return render_template("home1.html")

# End Logout


# User Management
@app.route('/user_managemen')
def user_managemen():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM user_managemen")
    rv = cur.fetchall()
    cur.close()
    return render_template('user_managemen.html', user_managemens=rv)


@app.route('/simpan-user_managemen', methods=["POST"])
def saveuser_managemen():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO user_managemen (name, email, password) VALUES (%s, %s, %s)", (name, email, password))
    mysql.connection.commit()
    return redirect(url_for('user_managemen'))


@app.route('/update-user_management', methods=["POST"])
def updateuser_managemen():
    id_data = request.form['id']
    nama = request.form['name']
    email = request.form['email']
    password = request.form['password']
    cur = mysql.connection.cursor()
    cur.execute("UPDATE user_managemen SET name=%s, email=%s, password=%s WHERE id=%s", (nama ,email,password,id_data,))
    mysql.connection.commit()
    return redirect(url_for('user_managemen'))

@app.route('/hapus-user_managemen/<string:id_data>', methods=["GET"])
def hapususer_managemen(id_data):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM user_managemen WHERE id=%s", (id_data,))
    mysql.connection.commit()
    return redirect(url_for('user_managemen'))
# End User Management


# Sparepart1
@app.route('/sparepart')
def sparepart():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM sparepart")
    list_part = cur.fetchall()
    cur.execute("SELECT status, count(status) as count_status FROM sparepart GROUP BY status")
    status_count = cur.fetchall()

    chart_labels = []
    chart_data = []
    for st in status_count:
        chart_labels.append(str(st['status']))
        chart_data.append(st['count_status'])

    print(chart_labels)

    return render_template('sparepart1.html', list_part = list_part, chart_data = chart_data, chart_labels = chart_labels)

@app.route('/add_sparepart', methods=["POST"])
def add_sparepart():
    n = request.form['btnradio']
    converted_num = int(n)
    for i in range(converted_num):
        
        numbering = str(i)
        nama =  numbering
        letters = ['OK', 'REJECT']
        random_index1 = random.choices(letters)
        letter = ['TROMOL', 'KOPLING', 'SHOCK', 'RANTAI']
        random_index = random.choices(letter)
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO sparepart (nama_part, status) VALUES (%s, %s)", (random_index, random_index1))
        mysql.connection.commit()
        time.sleep(10)
    return redirect(url_for('sparepart'))   

@app.route('/edit_sparepart/<Id>', methods = ['POST', 'GET'])
def edit_sparepart(Id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM sparepart WHERE Id=%s', (Id))
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('_sparepart.html', data = data[0])


@app.route('/update_sparepart/<Id>', methods=['POST'])
def update_sparepart(Id):
    if request.form['btnradio'] == 'OK':
        cur = mysql.connection.cursor()
        letterz = ['OK']
        cur.execute(" UPDATE sparepart SET status = %s WHERE Id=%s ", (letterz, Id))
        mysql.connection.commit()
        return redirect(url_for('sparepart'))
    if request.form['btnradio'] == 'REJECT':
        cur = mysql.connection.cursor()
        letterz = ['REJECT']
        cur.execute(" UPDATE sparepart SET status = %s WHERE Id=%s", (letterz, Id))
        mysql.connection.commit()
        return redirect(url_for('sparepart'))

@app.route('/delete_sparepart/<string:id_data>', methods=["GET"])
def delete_sparepart(id_data):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM sparepart WHERE Id=%s", (id_data,))
    mysql.connection.commit()
    return redirect(url_for('sparepart'))

@app.route("/add_chart")
def chart():
    cur = mysql.connection.cursor()
    data_1 = cur.execute('SELECT * FROM sparepart WHERE Id = OK', (id))
    ok_data = data['data_1'].count()
    data_2 = cur.execute('SELECT * FROM sparepart WHERE Id = REJECT', (id))
    reject_data = data['data_2'].count()
    labels = ["OK","REJECT"]
    values = int([ok_data, reject_data])
    return render_template('chart.html', values=values, labels=labels)


# Snd Sparepart1

# Sparepart2
@app.route('/sparepart2')
def sparepart2():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM sparepart")
    list_part = cur.fetchall()
    cur.execute("SELECT status, count(status) as count_status FROM sparepart GROUP BY status")
    status_count = cur.fetchall()

    chart_labels = []
    chart_data = []
    for st in status_count:
        chart_labels.append(str(st['status']))
        chart_data.append(st['count_status'])

    print(chart_labels)

    return render_template('sparepart2.html', list_part = list_part, chart_data = chart_data, chart_labels = chart_labels)

# End Sparepart2

if __name__ == '__main__':
    app.secret_key = "^A%DJAJU^JJ123"
    app.run(debug=True)