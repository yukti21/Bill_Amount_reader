from pdf2image import convert_from_path
import easyocr
import numpy as np

reader = easyocr.Reader(['en'])
images = convert_from_path(r"C:\Users\Mayank Subramanian\Downloads\Receipt.pdf", 500,
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
# print(amt)
