#pip install mysql-connector-python
import mysql.connector

outfile = open("2.txt",'w')
outfile.write("contact_id,smartid" + '\n')
cnx = mysql.connector.connect(user='root', password='xxxxx',
               host='192.168.246.2',
               database='test')

cursor = cnx.cursor()
query = ("select * from table")

cursor.execute(query)
#写文件 具体操作看数据
for i in cursor:
    outfile.write(str(i).strip('(').strip(')') + '\n')
cursor.close()
cnx.close()
outfile.close()
