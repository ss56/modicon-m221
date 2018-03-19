import csv
import sys
import MySQLdb

mydb = MySQLdb.connect(host='localhost',
    user='root',
    passwd='12345',
    db='modicon')
cursor = mydb.cursor()

csv_data = csv.reader(file(sys.argv[1]))
for row in csv_data:

    cursor.execute('INSERT INTO instructions(op_code, \
          instruction, output )' \
          'VALUES(%s, %s, %s)', 
          row)
#close the connection to the database.
mydb.commit()
cursor.close()

print "Done"