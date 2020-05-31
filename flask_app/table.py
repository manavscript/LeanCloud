import sqlite3


conn=sqlite3.connect('test6.db')
print ("Opened success")

conn.execute('''CREATE TABLE IF NOT EXISTS COMPANY 
         (ID INT PRIMARY KEY     NOT NULL,
         TASK           TEXT    NOT NULL,
         DUEDATE            DATETIME     NOT NULL,
         STATUS        CHAR(50) NOT NULL);''')
print ("sucess")
conn.execute("INSERT INTO COMPANY (ID,TASK,DUEDATE,STATUS) \
      VALUES (1, 'Paul California', '2020-01-09', 'Finished' )");

conn.execute("INSERT INTO COMPANY (ID,TASK,DUEDATE,STATUS) \
      VALUES (2, 'Allen Texas', '2020-01-09', 'Finished' )");

conn.execute("INSERT INTO COMPANY (ID,TASK,DUEDATE,STATUS) \
      VALUES (3, 'Teddy Norway', '2020-01-09', 'Finished' )");

conn.execute("INSERT INTO COMPANY (ID,TASK,DUEDATE,STATUS) \
      VALUES (4, 'Mark Rich-Mond ', '2020-01-09', 'Finished' )");

conn.commit()
print ("Records created successfully")
conn.close()