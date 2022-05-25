
import sqlite3

conn = sqlite3.connect('desktopapp.db')
cur = conn.cursor()
cur.execute('''CREATE TABLE Customer
         (Cust_Id INTEGER PRIMARY KEY AUTOINCREMENT     NOT NULL,
         First_NAME           text    NOT NULL,
         Last_Name            text     NOT NULL,
         Email   Nvarchar(100)  ,
         Address        CHAR(50),
         Number INTEGER,
         is_active boolean,
         is_delete boolean,
         created_date text );''')

cur.execute('''CREATE TABLE Product
      (Product_Id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
      Name text Not null,
      Description text not null,
      Price real not null,
      Quantity INTEGER,
      is_active boolean,
      is_delete boolean,
      created_date text,
      Cust_Id INTEGER,
      foreign key (Cust_Id) references Customer(Cust_Id) );''')




cur.execute('''CREATE TABLE GSTMASTER
      (GST_Id INTEGER primary key autoincrement not null,
      Name text not null,
      Percent real not null,
      is_active boolean,
      is_deleted boolean );''')


cur.execute('''CREATE TABLE ORDERS
      (Order_Id INTEGER primary key autoincrement not null,
      Quantity INTEGER not null,
      Order_price real not null,
      Gst_price real not null,
      Discount INTEGER,
      Order_date text,
      Cust_Id INTEGER,
      Product_Id INTEGER,
      GST_Id INTEGER,
      foreign key (Cust_Id) references Customer(Cust_Id),
      foreign key (Product_Id) references Product(Product_Id),
      foreign key (GST_Id) references GSTMASTER (GST_Id));''')


conn.commit()
cur.close()


print("Table created successfully")

""" 

conn.execute("INSERT INTEGERO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
      VALUES (1, 'Paul', 32, 'California', 20000.00 )");

conn.execute("INSERT INTEGERO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
      VALUES (2, 'Allen', 25, 'Texas', 15000.00 )");

conn.execute("INSERT INTEGERO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
      VALUES (3, 'Teddy', 23, 'Norway', 20000.00 )");

conn.execute("INSERT INTEGERO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
      VALUES (4, 'Mark', 25, 'Rich-Mond ', 65000.00 )");

conn.commit()
prINTEGER("Records created successfully") 

 """

""" cursor = conn.execute("SELECT id, name, address, salary from COMPANY")
for row in cursor:
   prINTEGER("ID = ", row[0])
   prINTEGER("NAME = ", row[1])
   prINTEGER("ADDRESS = ", row[2])
   prINTEGER("SALARY = ", row[3], "\n")

prINTEGER("Operation done successfully")
 """

