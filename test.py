import sqlite3
cxn=sqlite3.connect(r'C:\ke\数据库\学生选课成绩管理系统\student.db')
cur=cxn.cursor()
str='select * from s where sno="%s"'%'s1'
print(str)
cur.execute(str)
print(cur.fetchall())
cur.close()
cxn.commit()
cxn.close()