import MySQLdb
db = MySQLdb.connect(host='localhost', user='root', passwd='1234', db='book_management')
db.autocommit(True)
cursor = db.cursor()
insert = "INSERT INTO management VALUES('2007','JErry')"
cursor.execute(insert)
create = "CREATE TABLE account()"
create = "CREATE TABLE account()"
create = "CREATE TABLE account(a_no VARCHAR(10))"
cursor.execute(create)
create = "CREATE TABLE fruit(id int PRIMARY KEY, name varchar(10), cost int)"
cursor.execute(create)
select = "select id, name from fruit"
cursor.execute(select)
temp = cursor.fetchall()
temp
