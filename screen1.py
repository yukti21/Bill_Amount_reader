from tkinter import *
from tkinter import messagebox
import sqlite3
from tkinter.filedialog import askopenfile
import time
#import ocr
from pdf2image import convert_from_path
import easyocr
import numpy as np
f = ('Times', 14)

con = sqlite3.connect('bill.db')
cur = con.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS record(
                    expense text, 
                    amount number,  
                    month text
                )
            ''')
con.commit()

ws = Tk()
ws.title('BillAnalyser')
ws.geometry('540x400')
ws.config(bg='#0B5A81')

def nextPage():
    ws.destroy()
    import screen2

def uploadFiles():
    pb1 = Progressbar(
        master,
        orient=HORIZONTAL,
        length=300,
        mode='determinate'
    )
    pb1.grid(row=4, columnspan=3, pady=20)
    for i in range(5):
        ws.update_idletasks()
        pb1['value'] += 20
        time.sleep(1)
    pb1.destroy()
    Label(master, text='File Uploaded Successfully!', foreground='green').grid(row=6, columnspan=3, pady=10)


def open_file():
    file_path = askopenfile(mode='r', filetypes=[('All Files', '*.*')])
    if file_path is not None:
        pass
    #print(file_path.name)
    reader = easyocr.Reader(['en'])
    images = convert_from_path(f'{file_path.name}', 500,
                               poppler_path=r"C:\Users\Mayank Subramanian\Downloads\poppler-0.68.0_x86\poppler-0.68.0\bin")
    bounds = reader.readtext(np.array(images[0]))
    amount = []
    for i in range(len(bounds)):
        if (bounds[i][1] == 'TOTAL AMOUNT' or bounds[i][1] == 'Bill Amount' or bounds[i][1] == 'Amount Payable' or
                bounds[i][1] == 'AMOUNT' or bounds[i][1] == 'TOTAL' or bounds[i][1] == 'Total Amount (S)'):
            s = ""
            for m in bounds[i + 1][1]:
                if m.isdigit() or m == '.':
                    s = s + m
            if s[0] == '.':
                s = s[1:]
            amount.append(float(s))
    amt = float(s)
    amount = Label(right_frame, text=amt)
    amount.grid(row=3, column=2, pady=10, padx=20)

def insert_record():
    check_counter = 0
    warn = ""
    if expense.get() == "":
        warn = "Expense can't be empty"
    else:
        check_counter += 1

    if amount.get() == "":
        warn = "Amount can't be empty"
    else:
        check_counter += 1

    if variable.get() == "":
        warn = "Select Country"
    else:
        check_counter += 1

    if check_counter == 3:
        try:
            con = sqlite3.connect('bill.db')
            cur = con.cursor()
            cur.execute("INSERT INTO record VALUES (:expense, :amount, :month)", {
                'expense': expense.get(),
                'amount': amount.get(),
                'month': variable.get()

            })
            con.commit()
            messagebox.showinfo('confirmation', 'Record Saved')

        except Exception as ep:
            messagebox.showerror('', ep)
    else:
        messagebox.showerror('Error', warn)


countries = []
variable = StringVar()
world = open('BILLS.txt', 'r')
for country in world:
    country = country.rstrip('\n')
    countries.append(country)
variable.set(countries[11])

# widgets

right_frame = Frame(
    ws,
    bd=2,
    bg='#CCCCCC',
    relief=SOLID,
    padx=10,
    pady=10
)

Label(
    right_frame,
    text="Enter Expense",
    bg='#CCCCCC',
    font=f
).grid(row=0, column=0, sticky=W, pady=10)

Label(
    right_frame,
    text="Amount",
    bg='#CCCCCC',
    font=f
).grid(row=2, column=0, sticky=W, pady=10)

#amount = Label(right_frame, text = ocr.amt)
#amount.grid(row=3, column=2, pady=10, padx=20)

Label(
    right_frame,
    text="Select Month",
    bg='#CCCCCC',
    font=f
).grid(row=4, column=0, sticky=W, pady=10)

expense = Entry(
    right_frame,
    font=f
)

amount1 = Entry(
    right_frame,
    font=f
)

uploadbtn = Button(
    right_frame,
    text='Choose File',
    command=lambda: open_file()
)
register_country = OptionMenu(
    right_frame,
    variable,
    *countries)

register_country.config(
    width=15,
    font=('Times', 12)
)

register_btn = Button(
    right_frame,
    width=15,
    text='Register',
    font=f,
    relief=SOLID,
    cursor='hand2',
    #command=insert_record
)

nextpg_btn = Button(
    right_frame,
    width=6,
    text='>>>>>',
    font=f,
    relief=SOLID,
    cursor='hand2',
    command=nextPage
)

# widgets placement


expense.grid(row=0, column=1, pady=10, padx=20)
amount1.grid(row=2, column=1, pady=10, padx=20)
uploadbtn.grid(row=3, column=1, pady=10, padx=20)
register_country.grid(row=4, column=1, pady=10, padx=20)
register_btn.grid(row=7, column=1, pady=10, padx=20)
nextpg_btn.grid(row=8, column=2, pady=10, padx=20)
right_frame.place(x=50, y=50)

# infinite loop
ws.mainloop()