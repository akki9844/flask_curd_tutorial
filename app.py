from flask import Flask, render_template, request, redirect, url_for, flash
# import psycopg2  # pip install psycopg2
# import psycopg2.extras
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = "cairocoders-ednalan"
#
# DB_HOST = "localhost"
# DB_NAME = "css"
# DB_USER = "root"
# DB_PASS = "root"
# conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)


app.config['MYSQL_HOST']="localhost"
app.config['MYSQL_USER']="root"
app.config['MYSQL_PASSWORD']="root"
app.config['MYSQL_DB']="css"

mysql=MySQL(app)

@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    # cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    s = "SELECT * FROM students"
    cur.execute(s)  # Execute the SQL
    list_users = cur.fetchall()
    return render_template('index.html', list_users=list_users)


@app.route('/add_student', methods=['POST'])
def add_student():
    cur = mysql.connection.cursor()
    # cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        email = request.form['email']
        cur.execute("INSERT INTO students (fname, lname, email) VALUES (%s,%s,%s)", (fname, lname, email))
        # conn.commit()
        mysql.connection.commit()
        flash('Student Added successfully')
        return redirect(url_for('Index'))


@app.route('/edit/<id>', methods=['POST', 'GET'])
def get_employee(id):
    cur = mysql.connection.cursor()
    # cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    cur.execute('SELECT * FROM students WHERE id = %s', (id))
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('edit.html', student=data[0])


@app.route('/update/<id>', methods=['POST'])
def update_student(id):
    if request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        email = request.form['email']

        cur = mysql.connection.cursor()
        # cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("""
            UPDATE students
            SET fname = %s,
                lname = %s,
                email = %s
            WHERE id = %s
        """, (fname, lname, email, id))
        flash('Student Updated Successfully')
        # conn.commit()
        mysql.connection.commit()
        return redirect(url_for('Index'))


@app.route('/delete/<string:id>', methods=['POST', 'GET'])
def delete_student(id):
    cur = mysql.connection.cursor()
    # cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    cur.execute('DELETE FROM students WHERE id = {0}'.format(id))
    # conn.commit()
    mysql.connection.commit()
    flash('Student Removed Successfully')
    return redirect(url_for('Index'))


if __name__ == "__main__":
    app.run(debug=True)
