import sqlite3
connection=sqlite3.connect("customer1.db")
c=connection.cursor()

connection.execute(""" CREATE TABLE customer1
   (id int,
    first_name text,
    last_name text,
    email text
    )


""")  

c.execute('''INSERT INTO customer1 VALUES ('1','Chaya', 'Kunder', 'chaya@gmail.com')''')
c.execute('''INSERT INTO customer1 VALUES ('2','Diya', 'Kunder', 'diya@gmail.com')''')
c.execute('''INSERT INTO customer1 VALUES ('3','Prachi', 'Suvarna', 'prachi@gmail.com')''')
many_customer=[('4','wes','brown','wes@code.com'),
               ('5','raju','kumar','raju@code.com')]
c.execute("""UPDATE customer1 SET first_name='Rajani'
           WHERE last_name='Kunder'
           """) 
#c.execute("DELETE FROM customer1 WHERE rowid=3")  
c.execute("SELECT rowid,*FROM customer1")            

c.executemany("INSERT INTO customer1 values (?,?,?,?)",many_customer)    
# print("Data Inserted in the table: ")
c.execute('''SELECT * FROM customer1''')
#c.execute("DROP TABLE customer1")
# for row in data:
#     print(row)
# c.fetchone()
# c.fetchmany(2)
# c.fetchone()
# c.fetchone()
# c.fetchone()[2]
# print(c.fetchmany(3)[1])
items=c.fetchall()
# print(items)
print("ID"+"\tNAME"+"\t\tEMAIL")

for item in items:
  print(str(item[0])+"\t"+item[1]+" "+item[2]+"\t"+item[3])


connection.commit()                             #commit our connection
connection.close()