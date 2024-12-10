from tkinter import *
import time
import ttkthemes
from tkinter import ttk, messagebox, filedialog
import pymysql
import pandas
from datetime import datetime

def iexit():
    result = messagebox.askyesno('Confirm', 'Do you want to exit?')
    if result:
        root.destroy()

def export_data():
    url = filedialog.asksaveasfilename(defaultextension='.csv')
    indexing = studentTable.get_children()
    newlist = []
    for index in indexing:
        content = studentTable.item(index)
        datalist = content['values']
        newlist.append(datalist)
    table = pandas.DataFrame(newlist, columns=['Id', 'Name', 'Mobile', 'Email', 'Address', 'Gender', 'D.O.B', 'Added Date', 'Added Time'])
    table.to_csv(url, index=False)
    messagebox.showinfo('Success', 'Data is saved successfully.')

def toplevel_data(title, button_text, command):
    global idEntry, nameEntry, phoneEntry, emailEntry, addressEntry, genderEntry, dobEntry, screen
    screen = Toplevel()
    screen.title(title)
    screen.grab_set()
    screen.resizable(0, 0)

    idLabel = Label(screen, text='Id', font=('times new roman', 20, 'bold'))
    idLabel.grid(row=0, column=0, padx=30, pady=15, sticky=W)
    idEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
    idEntry.grid(row=0, column=1, pady=15, padx=10)

    nameLabel = Label(screen, text='Name', font=('times new roman', 20, 'bold'))
    nameLabel.grid(row=1, column=0, padx=30, pady=15, sticky=W)
    nameEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
    nameEntry.grid(row=1, column=1, pady=15, padx=10)

    phoneLabel = Label(screen, text='Phone', font=('times new roman', 20, 'bold'))
    phoneLabel.grid(row=2, column=0, padx=30, pady=15, sticky=W)
    phoneEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
    phoneEntry.grid(row=2, column=1, pady=15, padx=10)

    emailLabel = Label(screen, text='Email', font=('times new roman', 20, 'bold'))
    emailLabel.grid(row=3, column=0, padx=30, pady=15, sticky=W)
    emailEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
    emailEntry.grid(row=3, column=1, pady=15, padx=10)

    addressLabel = Label(screen, text='Address', font=('times new roman', 20, 'bold'))
    addressLabel.grid(row=4, column=0, padx=30, pady=15, sticky=W)
    addressEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
    addressEntry.grid(row=4, column=1, pady=15, padx=10)

    genderLabel = Label(screen, text='Gender', font=('times new roman', 20, 'bold'))
    genderLabel.grid(row=5, column=0, padx=30, pady=15, sticky=W)
    genderEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
    genderEntry.grid(row=5, column=1, pady=15, padx=10)

    dobLabel = Label(screen, text='D.O.B', font=('times new roman', 20, 'bold'))
    dobLabel.grid(row=6, column=0, padx=30, pady=15, sticky=W)
    dobEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
    dobEntry.grid(row=6, column=1, pady=15, padx=10)

    student_button = ttk.Button(screen, text=button_text, command=command)
    student_button.grid(row=7, columnspan=2, pady=15)

    if title == 'Update Student':
        indexing = studentTable.focus()  # Get the selected item
        if not indexing:  # No item is selected
            messagebox.showerror("Error", "No Student is Selected", parent=screen)
            screen.destroy()  # Close the top-level window
            return
        
        content = studentTable.item(indexing)
        listdata = content['values']
        
        # Fill the entry fields with the current student data
        idEntry.insert(0, listdata[0])
        nameEntry.insert(0, listdata[1])
        phoneEntry.insert(0, listdata[2])
        emailEntry.insert(0, listdata[3])
        addressEntry.insert(0, listdata[4])
        genderEntry.insert(0, listdata[5])
        
        dob_value = listdata[6]  # Get the D.O.B value
        
        try:
            # If the date is in the correct format, convert it to datetime and insert it into the entry field
            parsed_dob = datetime.strptime(dob_value, '%Y-%m-%d')  # Ensure the format matches
            dobEntry.insert(0, parsed_dob.strftime('%Y-%m-%d'))  # Insert the formatted date string
        except (ValueError, TypeError):
            dobEntry.insert(0, dob_value)  # Insert the original value if it's invalid
            
def update_data():
    try:
        # Validate inputs
        if not all([nameEntry.get(), phoneEntry.get(), emailEntry.get(), addressEntry.get(), genderEntry.get(), dobEntry.get(), idEntry.get()]):
            messagebox.showerror("Error", "All fields are mandatory.", parent=screen)
            return

        # Get the date from the entry field in dd/mm/yyyy format
        dob = dobEntry.get()

        # Validate date format (dd/mm/yyyy)
        try:
            parsed_dob = datetime.strptime(dob, "%d/%m/%Y")  # Convert to datetime object
            dob = parsed_dob.strftime("%Y-%m-%d")  # Save it in yyyy-mm-dd format for the database
        except ValueError:
            messagebox.showerror("Error", "Invalid date format. Use dd/mm/yyyy.", parent=screen)
            return

        # Get the current date for the 'date' column
        current_date = datetime.now().strftime("%Y-%m-%d")  # Current date in yyyy-mm-dd format
        current_time = datetime.now().strftime("%H:%M:%S")  # Current time in hh:mm:ss format

        # Query execution
        query = 'UPDATE student SET name=%s, mobile=%s, email=%s, address=%s, gender=%s, dob=%s, date=%s, time=%s WHERE id=%s'
        mycursor.execute(query, (
            nameEntry.get(),
            phoneEntry.get(),
            emailEntry.get(),
            addressEntry.get(),
            genderEntry.get(),
            dob,
            current_date,  # Current date for the 'date' column
            current_time,  # Current time for the 'time' column
            idEntry.get()
        ))
        con.commit()
        
        messagebox.showinfo('Success', f'Id {idEntry.get()} is updated successfully', parent=screen)
        screen.destroy()
        show_student()
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}", parent=screen)
        
def show_student():
    query = 'select * from student'
    mycursor.execute(query)
    fetched_data = mycursor.fetchall()
    studentTable.delete(*studentTable.get_children())
    for data in fetched_data:
        studentTable.insert('', END, values=data)

def delete_student():
    indexing = studentTable.focus()
    content = studentTable.item(indexing)
    content_id = content['values'][0]
    query = 'delete from student where id=%s'
    mycursor.execute(query, content_id)
    con.commit()
    messagebox.showinfo('Deleted', f'Id {content_id} is deleted successfully.')
    query = 'select * from student'
    mycursor.execute(query)
    fetched_data = mycursor.fetchall()
    studentTable.delete(*studentTable.get_children())
    for data in fetched_data:
        studentTable.insert('', END, values=data)

def search_data():
    query = "SELECT * FROM student WHERE 1=1"
    params = []
    
    if idEntry.get():
        query += " AND id=%s"
        params.append(idEntry.get())
    
    if nameEntry.get():
        query += " AND name=%s"
        params.append(nameEntry.get())
    
    if emailEntry.get():
        query += " AND email=%s"
        params.append(emailEntry.get())
    
    if phoneEntry.get():
        query += " AND mobile=%s"
        params.append(phoneEntry.get())
    
    if addressEntry.get():
        query += " AND address=%s"
        params.append(addressEntry.get())
    
    if genderEntry.get():
        query += " AND gender=%s"
        params.append(genderEntry.get())
    
    if dobEntry.get():
        dob = dobEntry.get()
        try:
            # Convert DOB to YYYY-MM-DD format for proper database matching
            formatted_dob = time.strptime(dob, "%d/%m/%Y")
            formatted_dob = time.strftime("%Y-%m-%d", formatted_dob)
            query += " AND dob=%s"
            params.append(formatted_dob)
        except ValueError:
            messagebox.showerror('Error', 'Invalid Date Format. Please use DD/MM/YYYY.', parent=screen)
            return

    try:
        mycursor.execute(query, tuple(params))
        studentTable.delete(*studentTable.get_children())
        fetched_data = mycursor.fetchall()
        
        for data in fetched_data:
            studentTable.insert('', END, values=data)
        
        if not fetched_data:
            messagebox.showinfo('No Results', 'No records found for the given search criteria', parent=screen)
    
    except Exception as e:
        messagebox.showerror('Error', f'Error occurred: {str(e)}', parent=screen)


def add_data():
    if idEntry.get() == '' or nameEntry.get() == '' or phoneEntry.get() == '' or emailEntry.get() == '' or addressEntry.get() == '' or genderEntry.get() == '' or dobEntry.get() == '':
        messagebox.showerror('Error', 'All Fields are Required', parent=screen)
    else:
        currentdate = time.strftime('%Y-%m-%d')  # Correct format for 'date' column (YYYY-MM-DD)
        currenttime = time.strftime('%H:%M:%S')
        
        # Convert DOB format from DD/MM/YYYY to YYYY-MM-DD
        try:
            dob = datetime.strptime(dobEntry.get(), "%d/%m/%Y").strftime("%Y-%m-%d")
        except ValueError:
            messagebox.showerror('Error', 'Invalid Date Format for DOB. Please use DD/MM/YYYY.', parent=screen)
            return
        
        try:
            # Check if the ID already exists
            mycursor.execute("SELECT COUNT(*) FROM student WHERE id = %s", (idEntry.get(),))
            result = mycursor.fetchone()
            if result[0] > 0:
                messagebox.showerror('Error', 'ID already exists. Please use a different ID.', parent=screen)
                return

            # Use the corrected format for both DOB and currentdate (YYYY-MM-DD)
            query = 'insert into student (id, name, mobile, email, address, gender, dob, date, time) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            mycursor.execute(query, (idEntry.get(), nameEntry.get(), phoneEntry.get(), emailEntry.get(), addressEntry.get(), genderEntry.get(), dob, currentdate, currenttime))
            con.commit()
            
            result = messagebox.askyesno('Confirm', 'Data Added Successfully. Do you want to clean the form?', parent=screen)
            if result:
                idEntry.delete(0, END)
                nameEntry.delete(0, END)
                phoneEntry.delete(0, END)
                emailEntry.delete(0, END)
                addressEntry.delete(0, END)
                genderEntry.delete(0, END)
                dobEntry.delete(0, END)
            else:
                pass

        except Exception as e:
            messagebox.showerror('Error', f'Error occurred: {str(e)}', parent=screen)
        return

def connect_database():
    def connect():
        global mycursor, con
        try:
            con = pymysql.connect(host=hostEntry.get(), user=usernameEntry.get(), password=passwordEntry.get())
            mycursor = con.cursor()
        except:
            messagebox.showerror('Error', 'Invalid Details', parent=connectWindow)
            return

        try:
            query = 'create database studentmanagementsystem'
            mycursor.execute(query)
            query = 'use studentmanagementsystem'
            mycursor.execute(query)
            query = 'create table student(id int not null primary key,name varchar(50),mobile long,email varchar(50),address varchar(100),gender varchar(20),dob date,date date,time time)'
            mycursor.execute(query)
        except:
            query = 'use studentmanagementsystem'
            mycursor.execute(query)
        messagebox.showinfo('Success', 'Database Connection is Successful', parent=connectWindow)
        connectWindow.destroy()

        addstudentButton.config(state=NORMAL)
        searchstudentButton.config(state=NORMAL)
        updatestudentButton.config(state=NORMAL)
        showstudentButton.config(state=NORMAL)
        exportstudentButton.config(state=NORMAL)
        deletestudentButton.config(state=NORMAL)

    connectWindow = Toplevel()
    connectWindow.grab_set()
    connectWindow.geometry('470x250+730+230')
    connectWindow.title('Database Connection')
    connectWindow.resizable(0, 0)

    hostnameLabel = Label(connectWindow, text='Host Name', font=('arial', 20, 'bold'))
    hostnameLabel.grid(row=0, column=0, padx=20)
    hostEntry = Entry(connectWindow, font=('roman', 15, 'bold'), bd=2)
    hostEntry.grid(row=0, column=1, padx=40, pady=20)

    usernameLabel = Label(connectWindow, text='User Name', font=('arial', 20, 'bold'))
    usernameLabel.grid(row=1, column=0, padx=20)
    usernameEntry = Entry(connectWindow, font=('roman', 15, 'bold'), bd=2)
    usernameEntry.grid(row=1, column=1, padx=40, pady=20)

    passwordLabel = Label(connectWindow, text='Password', font=('arial', 20, 'bold'))
    passwordLabel.grid(row=2, column=0, padx=20)
    passwordEntry = Entry(connectWindow, font=('roman', 15, 'bold'), bd=2)
    passwordEntry.grid(row=2, column=1, padx=40, pady=20)

    connectButton = ttk.Button(connectWindow, text='CONNECT', command=connect)
    connectButton.grid(row=3, columnspan=2)

count = 0
text = ''

def slider():
    global text, count
    if count == len(s):
        count = 0
        text = ''
    text = text + s[count]  # S
    sliderLabel.config(text=text)
    count += 1
    sliderLabel.after(300, slider)

def clock():
    global date, currenttime
    date = time.strftime('%d/%m/%Y')
    currenttime = time.strftime(('%H:%M:%S'))
    datetimeLabel.config(text=f' Date: {date}\nTime: {currenttime}')
    datetimeLabel.after(1000, clock)

# GUI Part
root = ttkthemes.ThemedTk()
root.get_themes()
root.set_theme('radiance')
root.geometry('1174x680+0+0')
root.title('Student Management System')
root.resizable(0, 0)

datetimeLabel = Label(root, text='hello', font=('times new roman', 18, 'bold'))
datetimeLabel.place(x=5, y=5)
clock()

s = 'Student Management System'  # s[count]=S, when the count is 0
sliderLabel = Label(root, font=('arial', 28, 'italic bold'), width=30)
sliderLabel.place(x=200, y=0)
slider()

connectButton = ttk.Button(root, text='Connect Database', command=connect_database)
connectButton.place(x=980, y=0)

leftFrame = Frame(root)
leftFrame.place(x=50, y=80, width=300, height=600)

logo_image = PhotoImage(file='student.png')
logo_label = Label(leftFrame, image=logo_image)
logo_label.grid(row=0, column=0)

addstudentButton = ttk.Button(leftFrame, text='Add Student', width=25, state=DISABLED, command=lambda: toplevel_data('Add Student', 'ADD', add_data))
addstudentButton.grid(row=1, column=0, pady=20)

searchstudentButton = ttk.Button(leftFrame, text='Search Student', width=25, state=DISABLED, command=lambda: toplevel_data('Search Student', 'SEARCH', search_data))
searchstudentButton.grid(row=2, column=0, pady=20)

deletestudentButton = ttk.Button(leftFrame, text='Delete Student', width=25, state=DISABLED, command=delete_student)
deletestudentButton.grid(row=3, column=0, pady=20)

updatestudentButton = ttk.Button(leftFrame, text='Update Student', width=25, state=DISABLED, command=lambda: toplevel_data('Update Student', 'UPDATE', update_data))
updatestudentButton.grid(row=4, column=0, pady=20)

showstudentButton = ttk.Button(leftFrame, text='Show Student', width=25, state=DISABLED, command=show_student)
showstudentButton.grid(row=5, column=0, pady=20)

exportstudentButton = ttk.Button(leftFrame, text='Export Data', width=25, state=DISABLED, command=export_data)
exportstudentButton.grid(row=6, column=0, pady=20)

exitButton = ttk.Button(leftFrame, text='Exit', width=25, command=iexit)
exitButton.grid(row=7, column=0, pady=20)

rightFrame = Frame(root)
rightFrame.place(x=350, y=80, width=820, height=600)

scrollBarX = Scrollbar(rightFrame, orient=HORIZONTAL)
scrollBarY = Scrollbar(rightFrame, orient=VERTICAL)

studentTable = ttk.Treeview(rightFrame, columns=('Id', 'Name', 'Mobile', 'Email', 'Address', 'Gender', 'D.O.B', 'Added Date', 'Added Time'), xscrollcommand=scrollBarX.set, yscrollcommand=scrollBarY.set)
scrollBarX.config(command=studentTable.xview)
scrollBarY.config(command=studentTable.yview)
scrollBarX.pack(side=BOTTOM, fill=X)
scrollBarY.pack(side=RIGHT, fill=Y)
studentTable.pack(fill=BOTH, expand=1)

studentTable.heading('Id', text='Id')
studentTable.heading('Name', text='Name')
studentTable.heading('Mobile', text='Mobile')
studentTable.heading('Email', text='Email Address')
studentTable.heading('Address', text='Address')
studentTable.heading('Gender', text='Gender')
studentTable.heading('D.O.B', text='D.O.B')
studentTable.heading('Added Date', text='Added Date')
studentTable.heading('Added Time', text='Added Time')

studentTable.column('Id', width=50, anchor=CENTER)
studentTable.column('Name', width=300, anchor=CENTER)
studentTable.column('Mobile', width=300, anchor=CENTER)
studentTable.column('Email', width=200, anchor=CENTER)
studentTable.column('Address', width=300, anchor=CENTER)
studentTable.column('Gender', width=100, anchor=CENTER)
studentTable.column('D.O.B', width=200, anchor=CENTER)
studentTable.column('Added Date', width=200, anchor=CENTER)
studentTable.column('Added Time', width=200, anchor=CENTER)

style = ttk.Style()
style.configure('Treeview', rowheight=40, font=('arial', 12, 'bold'), background='white', fieldbackground='white')
style.configure('Treeview.Heading', font=('arial', 14, 'bold'), foreground='red')
studentTable.config(show='headings')

root.mainloop()