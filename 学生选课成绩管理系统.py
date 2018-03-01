from flask import Flask, request, render_template, redirect, url_for
from flask.ext.bootstrap import Bootstrap
import sqlite3

app = Flask(__name__)
bootstrap=Bootstrap(app)

@app.route('/',methods=['GET','POST'])
def index():
    if request.method=='GET':
        return render_template('login.html')
    elif request.method=='POST':
        logn=request.form.get('user')
        cxn = sqlite3.connect(r'C:\ke\数据库\学生选课成绩管理系统\student.db')
        cur = cxn.cursor()
        cur.execute('select pswd from s where logn="%s"'%logn)
        true_pswd=cur.fetchall()
        cur.close()
        cxn.commit()
        cxn.close()
        if len(true_pswd) == 1 and request.form.get('passwd')==true_pswd[0][0]:
            return redirect(url_for('xk',sno=logn))
        else:
            return('用户名或密码错误')
@app.route('/xk/<sno>')
def xk(sno):
    cxn=sqlite3.connect(r'C:\ke\数据库\学生选课成绩管理系统\student.db')
    cur=cxn.cursor()
    cur.execute('select sno,sname,sex,age,sdept from s where sno="%s"' % sno)
    xxxx=cur.fetchall()[0]
    cur.execute('select cno,cname,tname from c where cno in (select cno from c except select c.cno from sc,c where sno="%s" and sc.cno=c.cno)'%sno)
    kxkc=cur.fetchall()
    cur.execute('select c.cno,cname,grade from sc,c where sno="%s" and sc.cno=c.cno and grade is not null'%sno)
    yxkccj=cur.fetchall()
    cur.execute('select * from c where cno in (select cno from sc where sno="%s")'%sno)
    yxkc=cur.fetchall()
    return render_template('xsxk.html', xxxx=xxxx, kxkc=kxkc, yxkccj=yxkccj, yxkc=yxkc, id=sno)
    cur.close()
    cxn.commit()
    cxn.close()

@app.route('/cjd/<sno>')
def cjd(sno):
    cxn = sqlite3.connect(r'C:\ke\数据库\学生选课成绩管理系统\student.db')
    cur = cxn.cursor()
    cur.execute('select c.cno,cname,grade,credit,tname from c,sc where sno="%s" and c.cno=sc.cno'%sno)
    cj=cur.fetchall()
    num=len(cj)
    cur.execute('select sname from s where sno="%s"' % sno)
    xm=cur.fetchall()[0][0]
    average = 0
    for i in cj:
        average=average+i[2]
    if(num!=0):
        average=int(average/num)
    else:
        average=0
    return render_template('cjd.html', cj=cj, xm=xm, average=average,id=sno)





if __name__ == '__main__':
    app.run()
