from tkinter import Tk, Button, Scrollbar, Listbox, StringVar, W, ttk, messagebox
#from the mysql configuration library import the dbConfiguration module
from mysql_config import dbConfig
#communication between python app and DB server
import mysql.connector as pyo

# double asterisk passes arguments to dbconfig 
con = pyo.connect(**dbConfig)
#cursor object allows executes statements 
cursor = con.cursor()

class Jobdb:
    def __init__(self):
        self.con = pyo.connect(**dbConfig)
        self.cursor = con.cursor()
        print("You have connected to the database")
        print(con)
    # method will close connection -> destroy object(connection)
    def __del__(self):
        self.con.close()
    #view method to contact and execute a SQL query to select from the table
    def view(self):
        self.cursor.execute("SELECT * FROM jobs")
        rows = self.cursor.fetchall()
        return rows
    #insert method for inserting new data into a table 
    def insert(self, job_title, job_url, job_date, job_description, job_stage, job_accepted):
        sql=("INSERT INTO jobs(job_title, job_url, job_date, job_desc, job_stage, job_accepted) VALUES(%s,%s,%s,%s,%s,%s)")
        values =[job_title, job_url, job_date, job_description, job_stage, job_accepted]
        self.cursor.execute(sql,values)
        self.con.commit()
        messagebox.showinfo(title="Job Database", message="New Job added to database")
    
    #updating exsisting tables in the DB
    def update(self, job_ID, job_title, job_url, job_date, job_description, job_stage, job_accepted):
        tsql = 'UPDATE jobs SET job_title = %s, job_date = %s, job_descr = %s, job_stage = %s, job_accepted =%s WHERE job_ID=%s'
        self.cursor.execute(tsql, [self, job_title, job_url, job_date, job_description, job_stage, job_accepted, job_ID])
        #self.connection to DB
        self.con.commit()
        messagebox.showinfo(title="Jobs Database", message="Updated the job into the database")

    def delete(self, job_ID):
        delquery = 'DELETE FROM jobs WHERE job_ID = %s'
        self.cursor.execute(delquery, [job_ID])
        self.con.commit()
        messagebox.showinfo(title="Jobs Database", message="Job Deleted")

# setting class Jobdb() equal to variable db 
db = Jobdb()

def get_selected_row():
    global selected_tuple
    index = list_box.curselection()[0]
    selected_tuple = list_box.get(index)
    title_entry.delete(0, 'end')
    title_entry.insert('end', selected_tuple[1])
    url_entry.delete(0, 'end')
    url_entry.insert('end', selected_tuple[2])
    desc_entry.delete(0, 'end')
    desc_entry.insert('end', selected_tuple[3])
    stage_entry.delete(0, 'end')
    stage_entry.insert('end', selected_tuple[4])
    accepted_entry.delete(0, 'end')
    accepted_entry.insert('end', selected_tuple[5])

def view_records():
    list_box.delete(0, 'end')
    for row in db.view():
        list_box.insert('end', row)
    
def add_job():
    db.insert(title_text.get(), url_text.get(), date_text.get(), desc_text.get(), stage_text.get(), accepted_text.get())
    list_box.delete(0, 'end')
    list_box.insert('end', (title_text.get(), url_text.get(), date_text.get(), desc_text.get(), stage_text.get(), accepted_text.get()))
    title_entry.delete(0, "end")
    url_entry.delete(0, "end")
    desc_entry.delete(0, "end")
    stage_entry.delete(0, "end")
    accepted_entry.delete(0, "end")
    con.commit()
    
def delete_records():
    db.delete(selected_tuple[0])
    con.commit()

def clear_screen():
    list_box.delete(0,'end')
    title_entry.delete(0, 'end')
    url_entry.delete(0, 'end')
    desc_entry.delete(0, 'end')
    stage_entry.delete(0, 'end')
    accepted_entry.delete(0, 'end')

def update_records():
    db.update(selected_tuple[0], title_text.get(), url_text.get(), date_text.get(), desc_text.get(), stage_text.get(), accepted_text.get())
    title_entry.delete(0, "end")
    url_entry.delete(0, "end")
    desc_entry.delete(0, "end")
    stage_entry.delete(0, "end")
    accepted_entry.delete(0, "end")
    con.commit()

def on_closing():
    dd = Jobdb
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()
        del dd
            
#create the application window 
root = Tk()

root.title("My Job Application Database")
#configure is for creating 
root.configure(background="tan")
#geometry method is to set the dimensions of the tkinter application window 
# geometry((width) x (height)
root.geometry("850x500")
root.resizable(width=False, height=False)

# Text and TextBox for Job Title
title_label = ttk.Label(root, text='Job Title',background="tan",font=("Times", 16, "bold italic"))
#title label grid: dimension where the label is displayed on the GUI 
title_label.grid(row=0, column=0, sticky=W)
#string var: from tkinter is used to monitor changes to tkinter variables and converts input captured to string(text value) 
title_text = StringVar()
# ttk.Entry -> entry widget TODO: create a validation checker 
title_entry = ttk.Entry(root,width=24, textvariable=title_text)
#position of the entry widget AKA:textbox  
title_entry.grid(row=0, column=1, sticky=W)

job_url = ttk.Label(root, text="URL", background="tan", font=("Times", 16, "bold italic"))
job_url.grid(row=1, column=0, sticky=W)
url_text = StringVar()
url_entry = ttk.Entry(root, width=24,textvariable=url_text)
url_entry.grid(row=1,column=1, sticky=W)

# Text and TextBox for Date applied
date_label = ttk.Label(root, text="Date", background="tan", font=("Times", 16, "bold italic"))
date_label.grid(row=2, column=0, sticky=W)
date_text = StringVar()
date_entry = ttk.Entry(root, width=24,textvariable=date_text)
date_entry.grid(row=2,column=1, sticky=W)

#TextBox and Text For Job Description 
desc_label = ttk.Label(root, text="Description", background="tan", font=("Times", 16, "bold italic"))
desc_label.grid(row=3, column=0, sticky=W)
desc_text = StringVar()
desc_entry = ttk.Entry(root, width=24,textvariable=desc_text)
desc_entry.grid(row=3,column=1, sticky=W)

#Text and Textbox for Interview round: Ex. round 0 applied, round 1 introduction, round 3 algorithms
stage_label = ttk.Label(root, text="Stage", background="tan", font=("Times", 16, "bold italic"))
stage_label.grid(row=4, column=0, sticky=W)
stage_text = StringVar()
stage_entry = ttk.Entry(root, width=24,textvariable=stage_text)
stage_entry.grid(row=4,column=1, sticky=W)

accepted_label = ttk.Label(root, text="Accepted", background="tan", font=("Times", 16, "bold italic"))
accepted_label.grid(row=5, column=0, sticky=W)
accepted_text = StringVar()
accepted_entry = ttk.Entry(root, width=24,textvariable=accepted_text)
accepted_entry.grid(row=5,column=1, sticky=W)

# button for adding a new user input 
add_btn = Button(root, text="Add Job", bg="grey",fg="white",font=("Times", 12, "bold italic"), command = add_job)
add_btn.grid(row=6, column=1, sticky=W)

# list box 
list_box = Listbox(root,height=20, width=60,font=("Times", 10, "bold italic"), bg="white")
list_box.place(x=340, y=20)

#scroll bar for list_box 
scroll_bar = Scrollbar(root)
scroll_bar.place(x=764, y=19.5)

list_box.config(yscrollcommand=scroll_bar.set)
scroll_bar.configure(command=list_box.yview)

modify_btn = Button(root, text="Modify Record",bg="purple",fg="white",font=("Times", 12, "bold italic"),command=update_records)
modify_btn.place(x=340, y=380)

delete_btn = Button(root, text="Delete", bg="purple", fg="white", font=("Times", 12, "bold italic"), command = delete_records) #call the class.function
delete_btn.place(x=460, y=380)

view_btn = Button(root, text="View All", bg="purple", fg="white", font=("Times", 12, "bold italic"), command = view_records)
view_btn.place(x=530, y=380)

clear_btn = Button(root, text="Clear All", bg="purple", fg="white", font=("Times", 12, "bold italic"), command = clear_screen)
clear_btn.place(x=615, y=380)

exit_btn = Button(root, text="Exit", bg="purple", fg="white", font=("Times", 12, "bold italic"), command = root.destroy)
exit_btn.place(x=700, y=380)

#this runs the entire application - mainloop has to be the last method called in a application
root.mainloop()