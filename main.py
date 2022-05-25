
from cgitb import text
from ensurepip import bootstrap

from datetime import date
from faulthandler import disable
from operator import index
from tkinter import font, messagebox
from tkinter.tix import COLUMN
from tkinter.ttk import Separator

from ttkbootstrap import Style, ttk
from ttkbootstrap.constants import *
from tkinter import *
from tkinter import END
from functools import partial
import sqlite3
import tkinter
import ttkbootstrap as ttk
#importing xlsxwriter module for excel sheets
import xlsxwriter


#As we are using bootstrap classes so we relace Tk() for new windows with ttk.window()

root = ttk.Window(themename="appdefault")
root.title("Customer and Order Management system")

root.geometry("1000x800")
root.iconbitmap(r'Rv_LOGO_blackbg.ico')
#mainframe as the first page when the app starts.


mainframe = Frame(root)
mainframe.pack(fill = "both",expand=1)
parentlabel = ttk.Label(mainframe,text=" ",font=("Helvetica","20","bold"))
parentlabel.grid(row=0,rowspan=10, column=5,padx=15,pady=15) 
labeltitle = ttk.Label(mainframe,text="Customer and Order Management System. ",font=("Helvetica","20","bold"))
labeltitle.grid(row=20, column=10,padx=15,pady=15,ipadx=5,ipady=5)
#separator
sep = ttk.Separator(mainframe,bootstyle= "secondary")
sep.grid(row=21, column=10,ipadx=100,ipady=15)
#Details
labelcontent = ttk.Label(mainframe,text="Stadalone python based application can be used by MSME or local shops who are still maintaining customer/product records in a pen & paper environment eg. Kirana shops(groceries), Salon, Hardware shops, etc and want to move towards digital but not sure how. So, here this tool can be helpful it allows to add customer & product details and also a basic order system where the business can track thier customer purchase history and order details. It also dynamically generates CSV/Excel files for the business to maintain thier daily reports or as they need.",font=("Arial","12"),wraplength=500)
labelcontent.grid(row=28,column=5,columnspan=100)
notelabel = ttk.Label(mainframe,text=" Note: Open Source tool", font=("Arial","10"),bootstyle = "secondary" )
notelabel.grid(row=29,column=5,columnspan=100,ipady=5)
createdby = ttk.Label(mainframe,text="Developed by Abhijot Chadha.",font=("Arial","10"),bootstyle = "secondary" )
createdby.grid(row=30,column=5,columnspan=100,ipady=5)
#style = ttk.Style("appdefault")
# Only Dashboard frame needs to be declared first as this will be the first page of the app.
dashboard = Frame(root)
def dashboard_view():
    hide_all_frames()

    dashboard.pack(fill="both",expand=1,side=TOP)
    #Dashboard Reports...
    labeltitle = ttk.Label(dashboard,text="Dashboard: ",font=("Helvetica","20","bold"))
    labeltitle.grid(row=1, column=1,columnspan=2,padx=15,pady=15) 




        
    conn = sqlite3.connect('desktopapp.db')
    cur = conn.cursor()
    
    cur.execute("select count(*) from customer where is_delete = 0")
    customer_records = cur.fetchone()
    conn.commit
    cur.execute("select count(*) from product where is_delete = 0")
    product_records = cur.fetchone()
    conn.commit
    cur.execute("select count(*) from orders")
    order_records = cur.fetchone()
    conn.commit()
    todaydate = str(date.today())
    cur.execute("select count(*) from orders where order_date =:order_date",{"order_date":todaydate})
    today_order_records = cur.fetchone()
    customer_btn = ttk.Button(dashboard,text ="Total Customers: " +str(customer_records[0]),command="",bootstyle = "Primary")
    customer_btn.grid(row=1,column=4,padx=30,pady=30,ipadx=40,ipady=40)
    product_btn = ttk.Button(dashboard,text ="Total Products: " +str(product_records[0]),command="",bootstyle = "warning" )
    product_btn.grid(row=1,column=8,padx=30,pady=30,ipadx=40,ipady=40)
    order_btn = ttk.Button(dashboard,text ="Total Orders : " +str(order_records[0]),command="",bootstyle = "success" )
    order_btn.grid(row=2,column=4,padx=30,pady=30,ipadx=40,ipady=40)
    today_btn = ttk.Button(dashboard,text ="Today's Orders: " +str(today_order_records[0]),command="",bootstyle = "info" )
    today_btn.grid(row=2,column=8,padx=30,pady=30,ipadx=40,ipady=40)
    
#------------------------------------------------------------------------------------------------
#Frame Functions

#Frame for add customer
def add_customer():
    
    hide_all_frames()
    #Databases
    customer_add.pack(fill="both",expand=1,side=TOP)
    
    def submit_customer():
        conn = sqlite3.connect('desktopapp.db')
        cur = conn.cursor()    
        today = str(date.today())
        if first_entry.get() and last_entry.get() is not None:
            cur.execute("INSERT INTO Customer(First_NAME,Last_Name,Email,Address,Number,is_delete,created_date) VALUES(:first_entry,:last_entry,:addr_entry,:email_entry,:number_entry,0,:created_date)",
                 {
                     'first_entry':first_entry.get(),
                     'last_entry':last_entry.get(),
                     'addr_entry':addr_entry.get(),
                     'email_entry':email_entry.get(),
                     'number_entry' :number_entry.get(),
                     'created_date':today  

                 }   
        
        
        
        
        )

                
                
        #print(first_entry.get())
        
    
        
            row_id = str(cur.lastrowid)
            message = messagebox.showinfo("Customer Added", "Customer ID: "+row_id + "Click OK to Add new Customer")
        #Connection commited
            conn.commit()
    
    
    
        #connection closed
            conn.close()
    
        else:
            message = messagebox.showinfo("Customer Added", "Please fill all the customer details and resubmit the form.")
        #removing all the text values after adding record
        print(type(first_entry))
        first_entry.delete(0,tkinter.END)
        last_entry.delete(0,END)
        addr_entry.delete(0,END)
        email_entry.delete(0,END)
        number_entry.delete(0,END)

    
    #update function
    def update_customer():
        update_record = Toplevel(root)
        
        update_record.title("Update Customer Details")
        update_record.geometry("1000x800")
        
        def search():
            conn = sqlite3.connect('desktopapp.db')
            cur = conn.cursor()
            
            cur.execute("select cust_id,First_name,Last_name,email,Address,number from customer where cust_id = :id or number like :id" ,{'id':cust_id_entry.get()})
            
            records = cur.fetchmany()
            if len(records) == 0:
                message = messagebox.showerror("Update Customer","Please enter customer ID or Number to update.")
                
            else:
                record = records[(0)]
                id = record[0]
                fname = record[1]
                lname = record[2]
                email = record[3]
                address = record[4]
                number = record[5]
                fname_label = Label(update_record,text="First Name",font=("Aerial","12")).grid(row=4,column=0,padx=5,pady=5)
                fname_entry = ttk.Entry(update_record, bootstyle="primary",)
                fname_entry.grid(row=4,column=1,padx=5,pady=5)
                lname_label = Label(update_record,text="Last Name",font=("Aerial","12")).grid(row=5,column=0,padx=5,pady=5)
                lname_entry = ttk.Entry(update_record, bootstyle="primary",)
                lname_entry.grid(row=5,column=1,padx=5,pady=5)
            
                email_label = Label(update_record,text="Email",font=("Aerial","12")).grid(row=6,column=0,padx=5,pady=5)
                email_entry = ttk.Entry(update_record, bootstyle="primary",)
                email_entry.grid(row=6,column=1,padx=5,pady=5)
            
                address_label = Label(update_record,text="Address",font=("Aerial","12")).grid(row=7,column=0,padx=5,pady=5)
                address_entry = ttk.Entry(update_record, bootstyle="primary",)
                address_entry.grid(row=7,column=1,padx=5,pady=5)
            
                number_label = Label(update_record,text="Number",font=("Aerial","12")).grid(row=8,column=0,padx=5,pady=5)
                number_entry = ttk.Entry(update_record, bootstyle="primary",)
                number_entry.grid(row=8,column=1,padx=5,pady=5)
                cust_id_entry.configure(state="readonly")
                #inserting record in entry widget
                fname_entry.insert(0,record[1])
                lname_entry.insert(0,record[2])
                email_entry.insert(0,record[3])
                address_entry.insert(0,record[4])
                number_entry.insert(0,record[5])
                conn.commit()
                conn.close()
            def submit_record():
                conn = sqlite3.connect('desktopapp.db')
                cur = conn.cursor()
                cur.execute("update customer set first_name = :fname,last_name = :lname,email =:email,address=:address,number=:number where cust_id=:id",{'fname':fname_entry.get(),'lname':lname_entry.get(),'email':email_entry.get(),'address':address_entry.get(),'number':number_entry.get(),'id':cust_id_entry.get()})
                conn.commit()
                conn.close()
                cust_id_entry.delete(0,END)
                fname_entry.delete(0,END)
                lname_entry.delete(0,END)
                email_entry.delete(0,END)
                address_entry.delete(0,END)
                number_entry.delete(0,END)
                message = messagebox.showinfo("Record Update","Click OK to update another record")
                #update_record.destroy()
            update_btn = ttk.Button(update_record,text = "Submit",command=submit_record,bootstyle="success")
            update_btn.grid(row=9,column=0,padx=5,pady=5)
            
            
            
            #print(id ,fname,lname,email,address,number)
            



        
        labeltitle = Label(update_record,text="Update Customer Details",font=("Helvetica","15","bold")).grid(row=0,column=0,padx=10,pady=20)
        id_label = Label(update_record,text="Customer Id / Mobile No",font=("Aerial","12")).grid(row=2,column=0,padx=5,pady=5)
        cust_id_entry = ttk.Entry(update_record,text = "Enter Customer Id / Mobile No",bootstyle ="primary")
        cust_id_entry.grid(row=2,column=1,padx=5,pady=5)
        search_btn = ttk.Button(update_record,text="Search",command =search ,bootstyle ="primary")
        search_btn.grid(row=2,column=3,padx=5,pady=5)
               
    

    #Firstname
    #firstname = StringVar()
    #label1 = Label(customer_add,textvariable=firstname).grid(row=0,column=0)
    labelframe = ttk.Label(customer_add,text="Add New Customer",font=("Helvetica","16","bold")).grid(row=0,column=0,padx=10,pady=20)
    firt_name_label = ttk.Label(customer_add,text="First Name",font=("Aerial","12")).grid(row=3,column=0,padx=5,pady=10)
    first_entry = ttk.Entry(customer_add,bootstyle="info")
    first_entry.grid(row=3,column=1,padx=5,pady=10,ipadx=30)
    
    #LastName
    
    last_name_label = ttk.Label(customer_add,text="Last Name",font=("Aerial","12")).grid(row=4,column=0,padx=5,pady=10)
    last_entry = ttk.Entry(customer_add,bootstyle="info")
    last_entry.grid(row=4,column=1,padx=5,pady=10,ipadx=30)
    #Address
    
    addr_label = ttk.Label(customer_add,text="Address Detail",font=("Aerial","12")).grid(row=5,column=0,padx=5,pady=10)
    addr_entry = ttk.Entry(customer_add,bootstyle="info")
    addr_entry.grid(row=5,column=1,padx=5,pady=10,ipadx=30)
    #Email
    
    email_label = ttk.Label(customer_add,text="Email",font=("Aerial","12")).grid(row=6,column=0,padx=5,pady=10)
    email_entry = ttk.Entry(customer_add,bootstyle="info")
    email_entry.grid(row=6,column=1,padx=5,pady=10,ipadx=30)
    #Number
    
    number_label = ttk.Label(customer_add,text="Mobile Number",font=("Aerial","12")).grid(row=7,column=0,padx=5,pady=10)
    number_entry = ttk.Entry(customer_add,bootstyle="info")
    number_entry.grid(row=7,column=1,padx=5,pady=10,ipadx=30)
    #Submit record
    submit_btn = ttk.Button(customer_add,text = "Add New Customer",command=submit_customer,bootstyle="success")
    submit_btn.grid(row=9,column=0,padx=5,pady=10)
    #update button
    update_btn = ttk.Button(customer_add,text = "Update",command= update_customer, bootstyle = "primary")
    update_btn.grid(row=9,column=1,padx=5,pady=5,ipadx=10)
   

#------------------------------------------------------------------------------------------------
#Frame for view customers
def view_customer():
    #To destroy frame
    
    hide_all_frames()
    customer_view.pack(fill="both",expand=1,side=TOP)
    
    def view_record():
        global query_table 
        conn = sqlite3.connect('desktopapp.db')
        cur = conn.cursor()
        cur.execute("select * from customer where is_delete = 0")
        records = cur.fetchall()
        id =''
        fname =''
        lname = ''
        email = ''
        address = ''
        number = ''
        rows = 4
        index = 1
        for record in records:
            
            lableidx = Label(customer_view,text =index).grid(row=rows,column=0)
            id = str(record[0])
            query_table = Label(customer_view,text=id).grid(row=rows,column=1) 
            fname = str(record[1]) 
            query_table = Label(customer_view,text=fname).grid(row=rows,column=2)
            lname = str(record[2]) 
            query_table = Label(customer_view,text=lname).grid(row=rows,column=3)
            email = str(record[3]) 
            query_table = Label(customer_view,text=email).grid(row=rows,column=4)
            address = str(record[4])
            query_table = Label(customer_view,text=address).grid(row=rows,column=5) 
            number = str(record[5]) 
            query_table = Label(customer_view,text=number).grid(row=rows,column=6)
            sep = ttk.Separator(customer_view,bootstyle = "warning")
            sep.grid(row = rows+1,ipadx=10,padx=0,pady=0)
            rows = rows+2
            index  = index+1
            
        #table using labels
        lableindex = Label(customer_view,text = "Sr No").grid(row=3,column=0)
        tabel_custid = Label(customer_view,text="Customer ID").grid(row=3,column=1)
        tabel_fname = Label(customer_view,text="First Name").grid(row=3,column=2)
        tabel_lname = Label(customer_view,text="Last Name").grid(row=3,column=3)
        tabel_email = Label(customer_view,text="Address").grid(row=3,column=4)
        tabel_adress = Label(customer_view,text="Email").grid(row=3,column=5)
        tabel_number = Label(customer_view,text="Number").grid(row=3,column=6)
        
        
        
        conn.commit()
        conn.close()    
        
        #function to search customer by id
    def view_by_id():
        view_customer_by_id =Toplevel(root)
        view_customer_by_id.title("Search Customers By ID ")
        view_customer_by_id.geometry("1000x800")

        conn = sqlite3.connect('desktopapp.db')
        cur = conn.cursor()
        cust_id = int(view_entry.get())
        cur.execute("select * from customer where Cust_Id = :id and is_delete = 0 ",{'id':cust_id})
        records = cur.fetchmany()
        id =''
        fname =''
        lname = ''
        email = ''
        address = ''
        number = ''
        
        for record in records:
            
            id = str(record[0])
            fname = str(record[1])
            lname = str(record[2])
            email = str(record[3])
            address = str(record[4])
            number = str(record[5])   
            
            query_table = Label(view_customer_by_id,text=id)
            query_table.grid(row=4,column=0) 
            query_table = Label(view_customer_by_id,text=fname)
            query_table.grid(row=4,column=1)
            query_table = Label(view_customer_by_id,text=lname)
            query_table.grid(row=4,column=2)
            query_table = Label(view_customer_by_id,text=email)
            query_table.grid(row=4,column=3)
            query_table = Label(view_customer_by_id,text=address)
            query_table.grid(row=4,column=4) 
            query_table = Label(view_customer_by_id,text=number)
            query_table.grid(row=4,column=5)
            sep = ttk.Separator(view_customer_by_id,bootstyle = "warning")
            sep.grid(row = 5,ipadx=10,padx=0,pady=0)
            

        labelframe = Label(view_customer_by_id,text="View Customer record: ",font=("Helvetica","15","bold")).grid(row=0,column=0,padx=10,pady=20)    
        tabel_custid = Label(view_customer_by_id,text="Customer ID").grid(row=3,column=0)
        tabel_fname = Label(view_customer_by_id,text="First Name").grid(row=3,column=1)
        tabel_lname = Label(view_customer_by_id,text="Last Name").grid(row=3,column=2)
        tabel_email = Label(view_customer_by_id,text="Email").grid(row=3,column=3)
        tabel_adress = Label(view_customer_by_id,text="Address").grid(row=3,column=4)
        tabel_number = Label(view_customer_by_id,text="Number").grid(row=3,column=5)
        view_entry.delete(0,END)

        print(records)
        conn.commit()
        conn.close()

    #delete function
    def delete_customer():
        
        conn = sqlite3.connect('desktopapp.db')
        cur = conn.cursor()
        cust_id = int(view_entry.get())
        cur.execute("update customer set is_delete = 1 where cust_id=:id",{'id':cust_id})
        message = messagebox.showinfo("Record Deleted","Click OK to continue.")
        view_entry.delete(0,END)
        conn.commit()
        conn.close()

    def download_customer():
        #Create a New workbook object
        todaydate = str(date.today())
        workbook = xlsxwriter.Workbook('Customers_Report_'+todaydate+'.xlsx')
        # The workbook object is then used to add new
        # worksheet via the add_worksheet() method.
        worksheet = workbook.add_worksheet()
        bold = workbook.add_format({'bold': True})

        # use the worksheet object to write the data
        # data via the write() method note 
        # Note: Throughout XlsxWriter, rows and columns are zero indexed. 
        # The first cell in a worksheet, A1 is (0, 0), B1 is (0, 1), A2 is (1, 0), B2 is (1, 1)
        worksheet.write('A1','Index No',bold)
        worksheet.write('B1','Customer ID',bold)
        worksheet.write('C1','First Name',bold)
        worksheet.write('D1','Last Name',bold)
        worksheet.write('E1','Email',bold)
        worksheet.write('F1','Address',bold)
        worksheet.write('G1','Mobile No',bold)
        worksheet.write('H1','Joined On',bold)
        worksheet.autofilter('B1:H1')
        #Open Database and pull all customer records
        conn = sqlite3.connect('desktopapp.db')
        cur = conn.cursor()
        cur.execute("select * from customer where is_delete = 0")
        records = cur.fetchall()
        row = 1
        column = 0
        index = 1
        for record in records:
            worksheet.write(row,column,index)
            worksheet.write(row,column+1,str(record[0]))
            worksheet.write(row,column+2,str(record[1]))
            worksheet.write(row,column+3,str(record[2]))
            worksheet.write(row,column+4,str(record[3]))
            worksheet.write(row,column+5,str(record[4]))
            worksheet.write(row,column+6,str(record[5]))
            worksheet.write(row,column+7,str(record[8]))
            row +=1
            index +=1
        conn.commit()
        conn.close
        #close the excel file
        workbook.close()

    labelframe = Label(customer_add,text="View Customer records: ",font=("Helvetica","15","bold")).grid(row=0,column=0,padx=5,pady=20)
    view_all = Button(customer_view,text="View All records",command=view_record)
    view_all.grid(row=1,column=0,padx=5,pady=20)
    view_entry = Entry(customer_view)
    view_entry.grid(row=1,column=1,padx=5,pady=20)
    view_byid = Button(customer_view,text="Search by ID",command=view_by_id)
    view_byid.grid(row=1,column=2,padx=5,pady=20)
    delete_btn = ttk.Button(customer_view,text = "Delete",command = delete_customer, bootstyle = "danger")
    delete_btn.grid(row=1,column=3,padx=5,pady=20)         
    download_btn = ttk.Button(customer_view,text = "Download CSV",command = download_customer, bootstyle = "success")
    download_btn.grid(row=1,column=4,padx=5,pady=20)    
#------------------------------------------------------------------------------------------------
#frame add for product
def add_product():
    hide_all_frames()

    def submit_product():
        #Databases
        if name_entry.get() and description_entry.get() and prod_price_entry.get() is not None:
            conn = sqlite3.connect('desktopapp.db')
            cur = conn.cursor()
            cur.execute("INSERT INTO Product(Name,Description,Price,Quantity,is_delete) VALUES(:name_entry,:description_entry,:prod_price_entry,:quantity_entry,0)",
            {
             'name_entry':name_entry.get(),
             'description_entry':description_entry.get(),
             'prod_price_entry':prod_price_entry.get(),
             'quantity_entry':quantity_entry.get()

            }
        
        
        )
            row_id = str(cur.lastrowid)
            message = messagebox.showinfo("Product Added", "Product ID: "+row_id + "Click OK to Add new Product")
            conn.commit()
            conn.close()

            name_entry.delete(0,END)
            description_entry.delete(0,END)
            prod_price_entry.delete(0,END)
            quantity_entry.delete(0,END)
        else:
            
            message = messagebox.showerror("Add Product","Please enter Product Name, Description and Price.")
                
    def update_product():
        update_record = Toplevel(root)
        
        update_record.title("Update Customer Details")
        update_record.geometry("1000x800")
        def search():
             conn = sqlite3.connect('desktopapp.db')
             cur = conn.cursor()
             cur.execute("SELECT product_id, name, description,price,quantity from product where product_id = :product_id",
             {
                 "product_id":product_id_entry.get(),

             })
             records = cur.fetchmany()
             if len(records) == 0:
                message = messagebox.showerror("Update Product","Please enter Product ID to update.")
             else:   
                record = records[(0)]
                id = record[0]
                name = record[1]
                description = record[2]
                price = record[3]
                quantity = record[4]
                name_label = Label(update_record,text="Product Name",font=("Aerial","12")).grid(row=4,column=0,padx=5,pady=5)
                name_entry = ttk.Entry(update_record, bootstyle="primary",)
                name_entry.grid(row=4,column=1,padx=5,pady=5)

                description_label = Label(update_record,text="Description",font=("Aerial","12")).grid(row=5,column=0,padx=5,pady=5)
                description_entry = ttk.Entry(update_record, bootstyle="primary",)
                description_entry.grid(row=5,column=1,padx=5,pady=5)

                prod_price_label = Label(update_record,text="Price",font=("Aerial","12")).grid(row=6,column=0,padx=5,pady=5)
                prod_price_entry = ttk.Entry(update_record, bootstyle="primary",)
                prod_price_entry.grid(row=6,column=1,padx=5,pady=5) 

                quantity_label = Label(update_record,text="Quantity",font=("Aerial","12")).grid(row=7,column=0,padx=5,pady=5)
                quantity_entry = ttk.Entry(update_record, bootstyle="primary",)
                quantity_entry.grid(row=7,column=1,padx=5,pady=5)
                product_id_entry.configure(state="readonly")
                #inserting record in entry widget
                name_entry.insert(0,record[1])
                description_entry.insert(0,record[2])
                prod_price_entry.insert(0,record[3])
                quantity_entry.insert(0,record[4])
             
                conn.commit()
                conn.close()

             def submit_record():
                conn = sqlite3.connect('desktopapp.db')
                cur = conn.cursor()
                cur.execute("update Product set name = :name,description = :description,price =:prod_price,quantity =:quantity where product_id=:product_id",
                {'name':name_entry.get(),'description':description_entry.get(),'prod_price':prod_price_entry.get(),'quantity':quantity_entry.get(),'product_id':product_id_entry.get()})

                conn.commit()
                conn.close()
                product_id_entry.delete(0,END)
                name_entry.delete(0,END)
                description_entry.delete(0,END)
                prod_price_entry.delete(0,END)
                quantity_entry.delete(0,END)
                
                message = messagebox.showinfo("Record Update","Click OK to update another record")
                update_record.destroy()
             update_btn = ttk.Button(update_record,text = "Submit",command=submit_record,bootstyle="success")
             update_btn.grid(row=9,column=0,padx=5,pady=5)
        
        labeltitle = Label(update_record,text="Update Product Details",font=("Helvetica","15","bold")).grid(row=0,column=0,padx=10,pady=20)
        id_label = Label(update_record,text="Product Id",font=("Aerial","12")).grid(row=2,column=0,padx=5,pady=5)
        product_id_entry = ttk.Entry(update_record,text = "Enter Product Id",bootstyle ="primary")
        product_id_entry.grid(row=2,column=1,padx=5,pady=5)
        search_btn = ttk.Button(update_record,text="Search",command =search ,bootstyle ="primary")
        search_btn.grid(row=2,column=3,padx=5,pady=5)

    product_add.pack(fill="both",expand=1)
    #Product Name
    labelframe = Label(product_add,text="Add New Product: ",font=("Helvetica","15","bold")).grid(row=0,column=0,padx=5,pady=20)
    name_label = Label(product_add,text="Product Name",font=("Aerial","12")).grid(row=3,column=0,padx=5,pady=10)
    name_entry = ttk.Entry(product_add,bootstyle="info")
    name_entry.grid(row=3,column=1,padx=5,pady=10,ipadx=30)
    #Description
    
    description_label = Label(product_add,text="Product Description",font=("Aerial","12")).grid(row=4,column=0,padx=5,pady=10)
    description_entry = ttk.Entry(product_add,bootstyle="info")
    description_entry.grid(row=4,column=1,padx=5,pady=10,ipadx=30)
    #Price
    
    prod_price_label = Label(product_add,text="Price Detail",font=("Aerial","12")).grid(row=5,column=0,padx=5,pady=10)
    prod_price_entry = ttk.Entry(product_add,bootstyle="info")
    prod_price_entry.grid(row=5,column=1,padx=5,pady=10,ipadx=30)
    #Quantity
    
    quantity_label = Label(product_add,text="Enter total quantity",font=("Aerial","12")).grid(row=6,column=0,padx=5,pady=10)
    quantity_entry = ttk.Entry(product_add,bootstyle="info")
    quantity_entry.grid(row=6,column=1,padx=5,pady=10,ipadx=30)
    #SubmitBtn
    submit_btn = ttk.Button(product_add,text = "Add New Product", command = submit_product,bootstyle ="primary")
    submit_btn.grid(row=7,column=0,padx=5,pady=10,ipadx=10)
    #Update Btn
    update_btn = ttk.Button(product_add,text = "Update",command= update_product, bootstyle = "primary")
    update_btn.grid(row=7,column=1,padx=2,pady=2,ipadx=10)
#------------------------------------------------------------------------------------------------
#frame view for product
def view_product():
    hide_all_frames()
    product_view.pack(fill="both",expand=1)
    
    def view_record():
        conn = sqlite3.connect('desktopapp.db')
        cur = conn.cursor()
        cur.execute("select * from product where is_delete = 0")
        records = cur.fetchall()
        id =''
        name =''
        description = ''
        price = ''
        quantity = ''
        
        rows = 4
        
        for record in records:
        
            id = str(record[0])
            query_table = Label(product_view,text=id).grid(row=rows,column=0) 
            name = str(record[1]) 
            query_table = Label(product_view,text=name).grid(row=rows,column=1)
            description = str(record[2]) 
            query_table = Label(product_view,text=description).grid(row=rows,column=2)
            price = str(record[3]) 
            query_table = Label(product_view,text=price).grid(row=rows,column=3)
            quantity = str(record[4])
            query_table = Label(product_view,text=quantity).grid(row=rows,column=4) 
            sep = ttk.Separator(product_view,bootstyle = "warning")
            sep.grid(row = rows+1,ipadx=10,padx=0,pady=0)
            rows = rows+2
            
        #table using labels
        tabel_prodid = Label(product_view,text="Product ID").grid(row=3,column=0)
        tabel_name = Label(product_view,text="Name").grid(row=3,column=1)
        tabel_description = Label(product_view,text="Description").grid(row=3,column=2)
        tabel_price = Label(product_view,text="Price").grid(row=3,column=3)
        tabel_quantity = Label(product_view,text="Quantity").grid(row=3,column=4)
        

        
        
        conn.commit()
        conn.close()    
        #function to search customer by id
    def view_by_id():
        view_product_by_id =Toplevel(root)
        view_product_by_id.title("Search Products By ID ")
        view_product_by_id.geometry("1000x800")
        global query_table
        
        conn = sqlite3.connect('desktopapp.db')
        cur = conn.cursor()
        prod_id = int(view_entry.get())
        cur.execute("select * from product where product_Id = :id and is_delete = 0",{'id':prod_id})
        records = cur.fetchmany()
        id =''
        name =''
        description = ''
        price = ''
        quantity = ''
        
        for record in records:
            id = str(record[0])
            name = str(record[1])
            description = str(record[2])
            price = str(record[3])
            quantity = str(record[4])
              
            
            query_table = Label(view_product_by_id,text=id)
            query_table.grid(row=4,column=0) 
            query_table = Label(view_product_by_id,text=name)
            query_table.grid(row=4,column=1)
            query_table = Label(view_product_by_id,text=description)
            query_table.grid(row=4,column=2)
            query_table = Label(view_product_by_id,text=price)
            query_table.grid(row=4,column=3)
            query_table = Label(view_product_by_id,text=quantity)
            query_table.grid(row=4,column=4) 
            sep = ttk.Separator(view_product_by_id,bootstyle = "warning")
            sep.grid(row = 5,ipadx=10,padx=0,pady=0)
            
            

        labelframe = Label(view_product_by_id,text="View Product: ",font=("Helvetica","15","bold")).grid(row=0,column=0,padx=10,pady=20) 
        tabel_custid = Label(view_product_by_id,text="Product ID").grid(row=3,column=0)
        tabel_name = Label(view_product_by_id,text="Name").grid(row=3,column=1)
        tabel_description = Label(view_product_by_id,text="Description").grid(row=3,column=2)
        tabel_price = Label(view_product_by_id,text="Price").grid(row=3,column=3)
        tabel_quantity = Label(view_product_by_id,text="Quantity").grid(row=3,column=4)
        
        view_entry.delete(0,END)

        print(records)
        conn.commit()
        conn.close()
    def delete_product():
        
        conn = sqlite3.connect('desktopapp.db')
        cur = conn.cursor()
        product_id = int(view_entry.get())
        cur.execute("update product set is_delete = 1 where product_id=:id",{'id':product_id})
        message = messagebox.showinfo("Record Deleted","Click OK to continue.")
        view_entry.delete(0,END)
        conn.commit()
        conn.close()
    
    def download_product():
        #Create a New workbook object
        todaydate = str(date.today())
        workbook = xlsxwriter.Workbook('Products_Report'+todaydate+'_.xlsx')
        # The workbook object is then used to add new
        # worksheet via the add_worksheet() method.
        worksheet = workbook.add_worksheet()
        # use the worksheet object to write the data
        # data via the write() method note 
        # Note: Throughout XlsxWriter, rows and columns are zero indexed. 
        # The first cell in a worksheet, A1 is (0, 0), B1 is (0, 1), A2 is (1, 0), B2 is (1, 1)
        bold = workbook.add_format({'bold': True})
        worksheet.write('A1','Index No',bold)
        worksheet.write('B1','Product ID',bold)
        worksheet.write('C1','Name',bold)
        worksheet.write('D1','Description',bold)
        worksheet.write('E1','Price',bold)
        worksheet.write('F1','Quantity',bold)
        worksheet.autofilter('B1:F1')
        #Open Database and pull all customer records
        conn = sqlite3.connect('desktopapp.db')
        cur = conn.cursor()
        cur.execute("select * from product where is_delete = 0")
        records = cur.fetchall()
        row = 1
        column = 0
        index = 1
        for record in records:
            worksheet.write(row,column,index)
            worksheet.write(row,column+1,str(record[0]))
            worksheet.write(row,column+2,str(record[1]))
            worksheet.write(row,column+3,str(record[2]))
            worksheet.write(row,column+4,str(record[3]))
            worksheet.write(row,column+5,str(record[4]))
            
            row +=1
            index +=1
        #close the excel file
        workbook.close()


    labelframe = Label(customer_add,text="View Product records: ",font=("Helvetica","15","bold")).grid(row=0,column=0,padx=10,pady=20)
    view_all = Button(product_view,text="View All records",command=view_record).grid(row=1,column=0,padx=5,pady=20)
    view_entry = Entry(product_view)
    view_entry.grid(row=1,column=1,padx=5,pady=20)
    view_byid = Button(product_view,text="Search by ID",command=view_by_id).grid(row=1,column=2,padx=5,pady=20)
    delete_btn = ttk.Button(product_view,text = "Delete",command = delete_product, bootstyle = "danger")
    delete_btn.grid(row=1,column=3,padx=5,pady=20)
    download_btn = ttk.Button(product_view,text = "Download CSV",command = download_product, bootstyle = "success")
    download_btn.grid(row=1,column=4,padx=5,pady=20)            
#------------------------------------------------------------------------------------------------
#frame add for orders
def add_order():
    hide_all_frames()
    
        
    
    
    def checkout_order():
        CheckoutOrder = Toplevel(root)
        
        CheckoutOrder.title("Search Customers By ID ")
        CheckoutOrder.geometry("1000x800")
        if product_id_entry.get() and cust_id_entry.get() is not None:
           
            conn = sqlite3.connect('desktopapp.db')
            cur = conn.cursor()
            cur.execute("select product_id,name,price from product where product_Id = :product_id",{'product_id':product_id_entry.get()})
            product_obj = cur.fetchmany()
            price = product_obj[0]
            per_price = price[2]
            if quantity_entry.get() == '':
                total_price = float(per_price)
            else:
                total_price = float(per_price) * float(quantity_entry.get())    
        


            cur.execute("select cust_id,first_name,last_name,number from customer where cust_Id = :cust_id",{'cust_id':cust_id_entry.get()})
            customer_obj = cur.fetchmany()
            #print(product_obj)
            #print(customer_obj)
            #print(per_price)
            customer = customer_obj[0]
        #print(total_price)
            conn.commit()
            conn.close()
        
            #Create Reciept
            full_name = customer[1] + " " +customer[2]
            name_label = Label(CheckoutOrder,text="Customer Name",font=("Helvetica","15","bold"))
            name_label.grid(row=10,column=1,padx=2,pady=2)
            full_name_label =Label(CheckoutOrder,text=full_name,font=("Helvetica","15","bold"))
            full_name_label.grid(row=10,column=2,padx=2,pady=2)
            number_label =Label(CheckoutOrder,text="Mobile Number",font=("Helvetica","15","bold"))
            number_label.grid(row=11,column=1,padx=2,pady=2)
            mobile_label= Label(CheckoutOrder,text=customer[3],font=("Helvetica","15","bold"))
            mobile_label.grid(row=11,column=2,padx=2,pady=2)
            quantity_label=Label(CheckoutOrder,text="Order Quantity",font=("Helvetica","15","bold"))
            quantity_label.grid(row=12,column=1,padx=2,pady=2)
            entered_quantity_label=Label(CheckoutOrder,text=quantity_entry.get(),font=("Helvetica","15","bold"))
            entered_quantity_label.grid(row=12,column=2,padx=2,pady=2)
            price_label =Label(CheckoutOrder,text="Total Price",font=("Helvetica","15","bold"))
            price_label.grid(row=13,column=1,padx=2,pady=2)
            total_price_label = Label(CheckoutOrder,text=total_price,font=("Helvetica","15","bold"))
            total_price_label.grid(row=13,column=2,padx=2,pady=2)
              
            def submit_order(price):
            #Databases
                print("Total",price)
                conn = sqlite3.connect('desktopapp.db')
                cur = conn.cursor()
                todaydate = str(date.today())
                cur.execute("INSERT INTO Orders(Quantity,Order_price,cust_id,product_id,gst_price,order_date) VALUES(:quantity_entry,:order_price,:cust_id_entry,:product_id_entry,:gst_price,:order_date)",
                {
                'quantity_entry':quantity_entry.get(),
                'order_price':price,
                'cust_id_entry':cust_id_entry.get(),
                'product_id_entry':product_id_entry.get(),
                'gst_price':price,
                'order_date':todaydate

                }
        
        
            )
            
            
            #message_label = Label(order_add,text ="Order Confirmed")
            #message_label.grid(row=12,column=1)
            #returned ID to message box
                row_id = str(cur.lastrowid)
                message = messagebox.showinfo("Order Confirmed", "Order ID: "+row_id + "Click OK to Add new order.")
                conn.commit()
                conn.close()
                CheckoutOrder.destroy()
        
                quantity_entry.delete(0,END)
                #order_price_entry.delete(0,END)
                cust_id_entry.delete(0,END)
                product_id_entry.delete(0,END)
              
            labelframe = Label(CheckoutOrder,text="Add New Order: ",font=("Helvetica","15","bold")).grid(row=0,column=0,padx=10,pady=20)
            submit_btn = ttk.Button(CheckoutOrder,text = "Comfirm Order", command = partial(submit_order,total_price),bootstyle="primary")
            submit_btn.grid(row = 15,column=1,padx=10,pady=20)
            def cancel_order(): 
            #call remove_receipt_labels to clear receipt
                remove_receipt_labels()
                quantity_entry.delete(0,END)
                #order_price_entry.delete(0,END)
                cust_id_entry.delete(0,END)
                product_id_entry.delete(0,END)
                CheckoutOrder.destroy()
        
            cancel_btn = ttk.Button(CheckoutOrder,text="Cancel Order",command=cancel_order,bootstyle="danger")
            cancel_btn.grid(row=15,column=2,padx=2,pady=2)
        
            def remove_receipt_labels():
                name_label.config(text="")
                full_name_label.config(text="")
                number_label.config(text="")
                mobile_label.config(text="")
                quantity_label.config(text="")
                entered_quantity_label.config(text="")
                price_label.config(text="")
                total_price_label.config(text="")
                submit_btn.config(state="disabled")
        else:
            
            message = messagebox.showerror("Add Order","Please enter customer ID and product ID to add new order.")
            CheckoutOrder.destroy()
   



       
    

    def clear_order():

        quantity_entry.delete(0,END)
        #order_price_entry.delete(0,END)
        cust_id_entry.delete(0,END)
        product_id_entry.delete(0,END)
    

    order_add.pack(fill="both",expand=1)
    labelframe = Label(order_add,text="Add New Order",font=("Helvetica","15","bold")).grid(row=0,column=0,padx=10,pady=20)
    cust_label = Label(order_add,text="Enter Customer ID",font=("Aerial","12")).grid(row=3,column=0,padx=5,pady=10)
    cust_id_entry = ttk.Entry(order_add,bootstyle="info")
    cust_id_entry.grid(row=3,column=1,padx=5,pady=10,ipadx=30)
   
    
    product_id_label = Label(order_add,text="Enter Product ID",font=("Aerial","12")).grid(row=3,column=2,padx=5,pady=10)
    product_id_entry = ttk.Entry(order_add,bootstyle="info")
    product_id_entry.grid(row=3,column=3,padx=5,pady=10,ipadx=30)
    """ order_price_entry = Label(order_add,text="Order total Price").grid(row=1,column=2)
    order_price_entry = Entry(order_add)
    order_price_entry.grid(row=1,column=3) """
   
    
    quantity_entry = Label(order_add,text="Enter Quantity",font=("Aerial","12")).grid(row=5,column=0,padx=5,pady=10)
    quantity_entry = ttk.Entry(order_add,bootstyle="info")
    quantity_entry.grid(row=5,column=1,padx=5,pady=10,ipadx=30)
   
    
    
    #SubmitBtn
    checkout_btn = ttk.Button(order_add,text = "Checkout Button", command = checkout_order,bootstyle="success")
    checkout_btn.grid(row=7,column=0,padx=5,pady=10,ipadx=10)
    cancel_btn = ttk.Button(order_add,text="Clear Order",bootstyle="danger",command=clear_order)
    cancel_btn.grid(row=7,column=1,padx=5,pady=10,ipadx=10)
  
#frame view for orders
def view_order():
    hide_all_frames()
    order_view.pack(fill="both",expand=1)
    def view_record():
        conn = sqlite3.connect('desktopapp.db')
        cur = conn.cursor()
        #cur.execute("select * from orders")
        #joining multiple tables for fetching order details.
        cur.execute("select Orders.Order_Id, Customer.First_NAME,Customer.Last_Name,Customer.Number,Product.Name,orders.Quantity,ORDERS.Order_price,ORDERS.Gst_price,ORDERS.Order_date from ORDERS left join Customer on Customer.Cust_Id = ORDERS.Cust_Id left JOIN Product on Product.Product_Id = ORDERS.Product_Id order by Order_Id")
        orders = cur.fetchall()
        id = ''
        f_name = ''
        l_name = ''
        number = ''
        p_name = ''
        qty = ''
        price =''
        gst_price = ''
        date = ''
        rows = 4
        for order in orders:
            id = str(order[0])
            query_table = Label(order_view,text=id).grid(row=rows,column=0) 
            f_name = str(order[1])
            query_table = Label(order_view,text=f_name).grid(row=rows,column=1)
            l_name = str(order[2])
            query_table = Label(order_view,text=l_name).grid(row=rows,column=2)
            number = str(order[3])
            query_table = Label(order_view,text=number).grid(row=rows,column=3)
            p_name = str(order[4])
            query_table = Label(order_view,text=p_name).grid(row=rows,column=4)
            qty = str(order[5])
            query_table = Label(order_view,text=qty).grid(row=rows,column=5)
            price = str(order[6])
            query_table = Label(order_view,text=price).grid(row=rows,column=6)
            gst_price = str(order[7])
            query_table = Label(order_view,text=gst_price).grid(row=rows,column=7)
            date = str(order[8])
            query_table = Label(order_view,text=date).grid(row=rows,column=8)
            sep = ttk.Separator(order_view,bootstyle = "warning")
            sep.grid(row = rows+1,ipadx=10,padx=0,pady=0)
            
            rows = rows+2
        #table using labels
        tabel_id = Label(order_view,text="Order ID").grid(row=3,column=0)
        tabel_fname = Label(order_view,text="Firt Name").grid(row=3,column=1)
        tabel_lname = Label(order_view,text="Last Name").grid(row=3,column=2)
        tabel_number = Label(order_view,text="Contact").grid(row=3,column=3)
        tabel_pname = Label(order_view,text="Product Name").grid(row=3,column=4)
        tabel_qty = Label(order_view,text="Quantity").grid(row=3,column=5)
        tabel_price = Label(order_view,text="Price").grid(row=3,column=6)
        tabel_gst_price = Label(order_view,text="GST Price").grid(row=3,column=7)
        tabel_date = Label(order_view,text="Order Date").grid(row=3,column=8)

        conn.commit()
        conn.close()

    def view_by_id():
        view_order_by_id =Toplevel(root)
        view_order_by_id.title("Search Orders By ID ")
        view_order_by_id.geometry("1000x800")

        conn = sqlite3.connect('desktopapp.db')
        cur = conn.cursor()
        order_id = int(view_entry.get())
        cur.execute("select Orders.Order_Id, Customer.First_NAME,Customer.Last_Name,Customer.Number,Product.Name,orders.Quantity,ORDERS.Order_price,ORDERS.Gst_price,ORDERS.Order_date from ORDERS left join Customer on Customer.Cust_Id = ORDERS.Cust_Id left JOIN Product on Product.Product_Id = ORDERS.Product_Id where orders.order_id =:id order by Order_Id",{'id':order_id})
        orders = cur.fetchmany()
        id = ''
        f_name = ''
        l_name = ''
        number = ''
        p_name = ''
        qty = ''
        price =''
        gst_price = ''
        date = ''
        rows = 4
        for order in orders:
            id = str(order[0])
            query_table = Label(view_order_by_id,text=id).grid(row=rows,column=0) 
            f_name = str(order[1])
            query_table = Label(view_order_by_id,text=f_name).grid(row=rows,column=1)
            l_name = str(order[2])
            query_table = Label(view_order_by_id,text=l_name).grid(row=rows,column=2)
            number = str(order[3])
            query_table = Label(view_order_by_id,text=number).grid(row=rows,column=3)
            p_name = str(order[4])
            query_table = Label(view_order_by_id,text=p_name).grid(row=rows,column=4)
            qty = str(order[5])
            query_table = Label(view_order_by_id,text=qty).grid(row=rows,column=5)
            price = str(order[6])
            query_table = Label(view_order_by_id,text=price).grid(row=rows,column=6)
            gst_price = str(order[7])
            query_table = Label(view_order_by_id,text=gst_price).grid(row=rows,column=7)
            date = str(order[8])
            query_table = Label(view_order_by_id,text=date).grid(row=rows,column=8)
            sep = ttk.Separator(view_order_by_id,bootstyle = "warning")
            sep.grid(row = rows+1,ipadx=10,padx=0,pady=0)
            
            
        #table using labels
        tabel_id = Label(view_order_by_id,text="Order ID").grid(row=3,column=0)
        tabel_fname = Label(view_order_by_id,text="Firt Name").grid(row=3,column=1)
        tabel_lname = Label(view_order_by_id,text="Last Name").grid(row=3,column=2)
        tabel_number = Label(view_order_by_id,text="Contact").grid(row=3,column=3)
        tabel_pname = Label(view_order_by_id,text="Product Name").grid(row=3,column=4)
        tabel_qty = Label(view_order_by_id,text="Quantity").grid(row=3,column=5)
        tabel_price = Label(view_order_by_id,text="Price").grid(row=3,column=6)
        tabel_gst_price = Label(view_order_by_id,text="GST Price").grid(row=3,column=7)
        tabel_date = Label(view_order_by_id,text="Order Date").grid(row=3,column=8)

        view_entry.delete(0,END)

        print(orders)
        conn.commit()
        conn.close()
        labelframe = Label(view_order_by_id,text="View Order by ID: ",font=("Helvetica","15","bold")).grid(row=0,column=0,padx=10,pady=20)    

    def download_order():
        #Create a New workbook object
        todaydate = str(date.today())
        workbook = xlsxwriter.Workbook('Orders_Report_'+todaydate+'.xlsx')
        # The workbook object is then used to add new
        # worksheet via the add_worksheet() method.
        worksheet = workbook.add_worksheet()
        # use the worksheet object to write the data
        # data via the write() method note 
        # Note: Throughout XlsxWriter, rows and columns are zero indexed. 
        # The first cell in a worksheet, A1 is (0, 0), B1 is (0, 1), A2 is (1, 0), B2 is (1, 1)
        bold = workbook.add_format({'bold': True})
        worksheet.write('A1','Index No',bold)
        worksheet.write('B1','Order ID',bold)
        worksheet.write('C1','First Name',bold)
        worksheet.write('D1','Last Name',bold)
        worksheet.write('E1','Mobile No',bold)
        worksheet.write('F1','Product Name',bold)
        worksheet.write('G1','Quantity',bold)
        worksheet.write('H1','Price',bold)
        worksheet.write('I1','GST Price',bold)
        worksheet.write('J1','Order Date',bold)
        worksheet.autofilter('B1:J1')
        #Open Database and pull all customer records
        conn = sqlite3.connect('desktopapp.db')
        cur = conn.cursor()
        cur.execute("select Orders.Order_Id, Customer.First_NAME,Customer.Last_Name,Customer.Number,Product.Name,orders.Quantity,ORDERS.Order_price,ORDERS.Gst_price,ORDERS.Order_date from ORDERS left join Customer on Customer.Cust_Id = ORDERS.Cust_Id left JOIN Product on Product.Product_Id = ORDERS.Product_Id order by Order_Id")
        records = cur.fetchall()
        row = 1
        column = 0
        index = 1
        for record in records:
            worksheet.write(row,column,index)
            worksheet.write(row,column+1,str(record[0]))
            worksheet.write(row,column+2,str(record[1]))
            worksheet.write(row,column+3,str(record[2]))
            worksheet.write(row,column+4,str(record[3]))
            worksheet.write(row,column+5,str(record[4]))
            worksheet.write(row,column+6,str(record[5]))
            worksheet.write(row,column+7,str(record[6]))
            worksheet.write(row,column+8,str(record[7]))
            worksheet.write(row,column+9,str(record[8]))
            
            row +=1
            index +=1
        conn.commit()
        conn.close
        #close the excel file
        workbook.close()


    labelframe = Label(order_view,text="View Orders: ",font=("Helvetica","15","bold")).grid(row=0,column=0,padx=5,pady=20)
    view_all = Button(order_view,text="View All records",command=view_record).grid(row=1,column=0,padx=5,pady=20)
    view_entry = Entry(order_view)
    view_entry.grid(row=1,column=1,padx=5,pady=20)
    view_byid = Button(order_view,text="Search by ID",command=view_by_id).grid(row=1,column=2,padx=5,pady=20)
    download_btn = ttk.Button(order_view,text = "Download CSV",command = download_order, bootstyle = "success")
    download_btn.grid(row=1,column=3,padx=5,pady=20)
    #filters pending
    # along with pagination
                
    


#------------------------------------------------------------------------------------------------

menubar = Menu(root)
#menu options
#Dashboard
dashboards = Menu(menubar,tearoff=0)
dashboards.add_command(label = 'View', command=dashboard_view )
menubar.add_cascade(label ='Dashboard', menu=dashboards)
#customer
customer = Menu(menubar,tearoff=0)
customer.add_command(label='Add',command=add_customer)
customer.add_command(label='View',command=view_customer)
menubar.add_cascade(label="Customer", menu=customer)
#Product menu
product = Menu(menubar, tearoff=0)
product.add_command(label='Add',command=add_product)
product.add_command(label='View',command=view_product)
menubar.add_cascade(label="Product", menu=product)
#Order menu
order = Menu(menubar, tearoff=0)
order.add_command(label='Add',command=add_order)
order.add_command(label='View',command=view_order)
menubar.add_cascade(label="Orders", menu=order)


#------------------------------------------------------------------------------------------------
#frames description

customer_add = Frame(root,bg="#B9C6AE")
customer_view = Frame(root,bg="#B9C6AE")
product_add = Frame(root,bg="#B9C6AE")
product_view = Frame(root,bg="#B9C6AE")
order_add = Frame(root,bg="#B9C6AE")
order_view = Frame(root,bg="#B9C6AE")
root.config(menu=menubar)
#------------------------------------------------------------------------------------------------

#Function to destroy frames while navigating menu
def hide_all_frames():
    #To clear the previous pack position hold by the frames.
    mainframe.pack_forget()
    dashboard.pack_forget()
    customer_add.pack_forget()
    customer_view.pack_forget()
    product_add.pack_forget()
    product_view.pack_forget()
    order_add.pack_forget()
    order_view.pack_forget()

    #Loop each element in frame
    for widget in mainframe.winfo_children():
        widget.destroy()
    for widget in dashboard.winfo_children():
        widget.destroy()

    for widget in customer_add.winfo_children():
        widget.destroy()

    for widget in customer_view.winfo_children():
        widget.destroy()   

    for widget in product_add.winfo_children():
        widget.destroy()

    for widget in product_view.winfo_children():
        widget.destroy()
    
    for widget in order_add.winfo_children():
        widget.destroy()   
    for widget in order_view.winfo_children():
        widget.destroy()


root.resizable(False,False)
root.mainloop()
