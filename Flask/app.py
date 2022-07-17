
from flask import Flask, render_template, request, url_for, redirect

from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'school'

mysql = MySQL(app)

#New User
@app.route('/', methods=['GET','POST'])
def addUsers():

    if request.method =='POST':
        studentdetail = request.form
        Sid= studentdetail['Sid']
        Std_name= studentdetail['Std_name']
        Department= studentdetail['Department']
        Lecture= studentdetail['Lecture']

        cur = mysql.connection.cursor()

        cur.execute("insert into studentdetail (Sid,Std_name,Department,Lecture) values (%s,%s,%s,%s)",(Sid,Std_name,Department,Lecture))

        mysql.connection.commit()
        cur.close()

        return redirect(url_for('home'))

    return render_template('addUsers.html')
#Loading Home Page

@app.route('/home')
def home():
    cur=mysql.connection.cursor()
    result=cur.execute("select * from studentdetail")
    if result > 0:
        studentdetail = cur.fetchall()
        return render_template('home.html',studentdetail=studentdetail)

#update user
@app.route('/editUsers/<string:Sid>',methods=['GET','POST'])
def editUsers(Sid):
    cur = mysql.connection.cursor()
    if request.method =='POST':
        studentdetail = request.form
        #Sid= studentdetail['Sid']
        Std_name= studentdetail['Std_name']
        Department= studentdetail['Department']
        Lecture= studentdetail['Lecture']
        cur.execute("UPDATE studentdetail SET Sid=%s,Std_name=%s,Department=%s,Lecture=%s WHERE Sid=%s",(Sid,Std_name,Department,Lecture,Sid))
        #cur.execute(sql,[Std_name,Department,Lecture,Sid])
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('home'))

    sql="select * from studentdetail where Sid=%s"
    cur.execute(sql,[Sid])
    studentdetail=cur.fetchone()
    return render_template('editUsers.html',studentdetail=studentdetail)


#Delete User
@app.route('/deleteUsers/<string:Sid>',methods=['GET','POST'])
def deleteUsers(Sid):
    cur = mysql.connection.cursor()
    cur.execute("delete from studentdetail where Sid =%s", [Sid])
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)
    