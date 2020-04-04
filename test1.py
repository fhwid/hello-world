import pymysql
company = '阿里巴巴'
title = '测试标题'
href = '测试链接'
date = '测试日期'
source = '测试来源'
db = pymysql.connect(host='localhost', port=3308, user='root', password='', database='pachong', charset='utf8')
cur = db.cursor()
sql = 'INSERT INTO test (company, title, href, date, source) VALUES (%s, %s, %s, %s, %s)'
cur.execute(sql, (company, title, href, date, source))
db.commit()
cur.close()
db.close()
