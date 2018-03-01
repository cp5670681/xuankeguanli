import os
from flask import Flask, request, render_template, redirect, url_for, flash
from flask.ext.bootstrap import Bootstrap
import sqlite3

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = os.urandom(24)
bootstrap = Bootstrap(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        logn = request.form.get('user')
        pswd=request.form.get('passwd')
        if logn=='admin' and pswd=='admin':
            return redirect(url_for('xsgl'))
        cxn = sqlite3.connect(r'C:\ke\数据库\学生选课成绩管理系统\student.db')
        cur = cxn.cursor()
        cur.execute('select pswd from s where logn="%s"' % logn)
        true_pswd = cur.fetchall()
        cur.close()
        cxn.commit()
        cxn.close()
        if len(true_pswd) == 1 and pswd == true_pswd[0][0]:
            return redirect(url_for('xk', sno=logn))
        else:
            flash('用户名或密码错误')
            return redirect(url_for('index'))


@app.route('/xk/<sno>')
def xk(sno):
    cxn = sqlite3.connect(r'C:\ke\数据库\学生选课成绩管理系统\student.db')
    cur = cxn.cursor()
    cur.execute('select sno,sname,sex,age,sdept from s where sno="%s"' % sno)
    xxxx = cur.fetchall()[0]
    cur.execute(
        'select cno,cname,tname from c where cno in (select cno from c except select c.cno from sc,c where sno="%s" and sc.cno=c.cno)' % sno)
    kxkc = cur.fetchall()
    cur.execute('select c.cno,cname,grade from sc,c where sno="%s" and sc.cno=c.cno and grade is not null' % sno)
    yxkccj = cur.fetchall()
    cur.execute('select * from c where cno in (select cno from sc where sno="%s")' % sno)
    yxkc = cur.fetchall()
    return render_template('xsxk.html', xxxx=xxxx, kxkc=kxkc, yxkccj=yxkccj, yxkc=yxkc, id=sno)
    cur.close()
    cxn.commit()
    cxn.close()


@app.route('/cjd/<sno>')
def cjd(sno):
    cxn = sqlite3.connect(r'C:\ke\数据库\学生选课成绩管理系统\student.db')
    cur = cxn.cursor()
    cur.execute('select c.cno,cname,grade,credit,tname from c,sc where sno="%s" and c.cno=sc.cno and grade is not null' % sno)
    cj = cur.fetchall()
    num = len(cj)
    cur.execute('select sname from s where sno="%s"' % sno)
    xm = cur.fetchall()[0][0]
    cur.close()
    cxn.commit()
    cxn.close()
    average = 0
    for i in cj:
        average = average + i[2]
    if (num != 0):
        average = int(average / num)
    else:
        average = 0
    return render_template('cjd.html', cj=cj, xm=xm, average=average, id=sno)


@app.route('/xk', methods=['POST'])
def xk_p():
    cxn = sqlite3.connect(r'C:\ke\数据库\学生选课成绩管理系统\student.db')
    cur = cxn.cursor()
    id = request.form.get('id')
    cno = request.form.get('xkcno')
    cur.execute(
        'select cno from c where cno in (select cno from c except select c.cno from sc,c where sno="%s" and sc.cno=c.cno)' % id)
    kxkc = cur.fetchall()
    kxkc2 = list()
    for i in kxkc:
        kxkc2.append(i[0])
    if cno not in kxkc2:
        flash('该课程不可选，选课失败')
        return redirect(url_for('xk', sno=id))
    else:
        cur.execute('insert into sc values("%s","%s",null)' % (id, cno))
        cur.close()
        cxn.commit()
        cxn.close()
        flash('选课成功')
        return redirect(url_for('xk', sno=id))


@app.route('/tk', methods=['POST'])
def tk_p():
    cxn = sqlite3.connect(r'C:\ke\数据库\学生选课成绩管理系统\student.db')
    cur = cxn.cursor()
    id = request.form.get('id')
    cno = request.form.get('tkcno')
    cur.execute('select cno from sc where sno="%s" and grade is null' % id)
    tkkc = cur.fetchall()
    tkkc2 = list()
    for i in tkkc:
        tkkc2.append(i[0])
    if cno not in tkkc2:
        flash('该课程不可退，退课失败')
        return redirect(url_for('xk', sno=id))
    else:
        cur.execute('delete from sc where sno="%s" and cno="%s" and grade is null' % (id, cno))
        cur.close()
        cxn.commit()
        cxn.close()
        flash('退课成功')
        return redirect(url_for('xk', sno=id))

@app.route('/xsgl')
def xsgl():
    cxn = sqlite3.connect(r'C:\ke\数据库\学生选课成绩管理系统\student.db')
    cur = cxn.cursor()
    cur.execute('select * from s')
    xsxx=cur.fetchall()
    cur.close()
    cxn.commit()
    cxn.close()
    return render_template('xsgl.html',xsxx=xsxx)

@app.route('/kcgl')
def kcgl():
    cxn = sqlite3.connect(r'C:\ke\数据库\学生选课成绩管理系统\student.db')
    cur = cxn.cursor()
    cur.execute('select * from c')
    kcxx=cur.fetchall()
    cur.close()
    cxn.commit()
    cxn.close()
    return render_template('kcgl.html',kcxx=kcxx)

@app.route('/add_student', methods=['POST'])
def add_student():
    cxn = sqlite3.connect(r'C:\ke\数据库\学生选课成绩管理系统\student.db')
    cur = cxn.cursor()
    try:
        cur.execute('insert into s values("%(sno)s","%(sname)s","%(sex)s","%(age)s","%(sdept)s","%(logn)s","%(pswd)s")' % request.form)
        cur.close()
        cxn.commit()
        cxn.close()
        flash("添加成功")
    except:
        flash("添加失败")
    return redirect(url_for('xsgl'))

@app.route('/del_student', methods=['POST'])
def del_student():
    cxn = sqlite3.connect(r'C:\ke\数据库\学生选课成绩管理系统\student.db')
    cur = cxn.cursor()
    try:
        cur.execute('delete from s where sno="%s"' % request.form.get('id'))
        if cur.rowcount == 0:
            flash("没有这个用户，删除失败")
            cur.close()
            cxn.commit()
            cxn.close()
            return redirect(url_for('xsgl'))
        cur.close()
        cxn.commit()
        cxn.close()
        flash("删除成功")
    except:
        flash("删除失败")
    return redirect(url_for('xsgl'))

@app.route('/add_class', methods=['POST'])
def add_class():
    cxn = sqlite3.connect(r'C:\ke\数据库\学生选课成绩管理系统\student.db')
    cur = cxn.cursor()
    try:
        cur.execute('insert into c values("%(cno)s","%(cname)s","%(credit)s","%(cdept)s","%(tname)s")' % request.form)
        cur.close()
        cxn.commit()
        cxn.close()
        flash("添加成功")
    except:
        flash("添加失败")
    return redirect(url_for('kcgl'))

@app.route('/del_class', methods=['POST'])
def del_class():
    cxn = sqlite3.connect(r'C:\ke\数据库\学生选课成绩管理系统\student.db')
    cur = cxn.cursor()
    try:
        cur.execute('delete from c where cno="%s"' % request.form.get('cno'))
        if cur.rowcount == 0:
            flash("没有这个课程，删除失败")
            cur.close()
            cxn.commit()
            cxn.close()
            return redirect(url_for('kcgl'))
        cur.close()
        cxn.commit()
        cxn.close()
        flash("删除成功")
    except:
        flash("删除失败")
    return redirect(url_for('kcgl'))


if __name__ == '__main__':
    app.run()
