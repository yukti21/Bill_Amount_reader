from tkinter import *
from tkinter import messagebox
import pandas as pd
import sqlite3
from tkinter.filedialog import askopenfile
import time
import prediction


f = ('Times', 14)
ws = Tk()
ws.title('BillAnalyser')
ws.geometry('700x600')
ws.config(bg='#0B5A81')

countries = []
variable = StringVar()
world = open('BILLS.txt', 'r')
for country in world:
    country = country.rstrip('\n')
    countries.append(country)
variable.set(countries[11])

def table():
    df = pd.read_csv('BILL2.csv')
    sum1=0
    mon= variable.get()
    n_rows = df.shape[0]
    n_cols = df.shape[1]
    column_names = df.columns
    for j, col in enumerate(column_names):
        text = Text(right_frame, width=16, height=1, bg = "#9BC2E6")
        text.grid(row=19,column=j)
        text.insert(INSERT, col)
    for i in range(n_rows):
        for j in range(n_cols):
            if df.loc[i][2]==mon:
                sum1=sum1+df.loc[i][1]
                text = Text(right_frame, width=16, height=1)
                text.grid(row=20+i,column=j)
                text.insert(INSERT, df.loc[i][j])
    amount = Label(right_frame, text = sum1)
    amount.grid(row=4, column=1, pady=10, padx=20)
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
    text="Select Month",
    bg='#CCCCCC',
    font=f
).grid(row=0, column=0, sticky=W, pady=10)

Label(
    right_frame,
    text="Total Expense",
    bg='#CCCCCC',
    font=f
).grid(row=4, column=0, sticky=W, pady=10)

Label(
    right_frame,
    text="Next Month Expense",
    bg='#CCCCCC',
    font=f
    ).grid(row=5, column=0, sticky=W, pady=10)
pred = Label(right_frame, text = prediction.d)
pred.grid(row=5, column=1, pady=10, padx=20)

register_country = OptionMenu(
    right_frame,
    variable,
    *countries)

register_country.config(
    width=15,
    font=('Times', 12)
)

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


register_btn = Button(
    right_frame,
    width=15,
    text='Search',
    font=f,
    relief=SOLID,
    cursor='hand2',
    command=table
)

import matplotlib.pyplot as plt



df = pd.read_excel(r"C:\Users\Mayank Subramanian\Downloads\grocery_dataset_eg.xlsx")
df.drop(['MONTH'],axis=1,inplace=True)
x = list(df.iloc[:, 0])
y = list(df.iloc[:, 1])

def graph():
    X = x[-12:]
    Y = y[-12:]
    plt.bar(X, Y, color='g')
    plt.title("Cost Trend")
    plt.xlabel("Months")
    plt.ylabel("Expenses")

    # Show the plot
    plt.show()



button = Button(right_frame, text = "Plot it", command = graph)


df = pd.read_excel(r"C:\Users\Mayank Subramanian\Downloads\grocery_dataset_eg.xlsx")



##amount = Label(right_frame, text=df["Amount"][5])
##amount.grid(row=4, column=1, pady=10, padx=20)
register_country.grid(row=0, column=1, pady=10, padx=20)
register_btn.grid(row=2, column=1, pady=10, padx=20)
right_frame.place(x=50, y=50)
button.grid(row = 60, column=1, pady=10, padx=20)
ws.mainloop()