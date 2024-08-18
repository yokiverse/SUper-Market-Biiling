# import pandas as pd
# import csv
# import mysql.connector
# db=mysql.connector.connect(
#      host="localhost",
#      user="root",
#      password="",
#      database="supermarket"
#  )
# mycursor=db.cursor()
# sql="insert into tab(stock_name, product_price, available_quantity) values (%s,%s,%s)"
# filename = 'stock.csv'
# file = open(filename, 'a', newline='')
# writer = csv.writer(file)
# if file.tell() == 0:
#     header = ['stock name', 'product price', 'available quantity']
#     writer.writerow(header)
# while True:
#     stock_name = input("Enter stock name: ")
#     while True:
#         try:
#             product_price = float(input("Enter product price: "))
#             break
#         except ValueError:
#             print("Invalid input. Please enter a valid number.")
#     available_quantity = int(input("Enter available quantity: "))
#     writer.writerow([stock_name, product_price, available_quantity])
#     add_more = input("Do you want to add more? (yes/no): ").strip().lower()
#     if add_more != 'yes':
#         break
# file.close()
# val=(stock_name, product_price, available_quantity)
# mycursor.execute(sql,val)
# db.commit()
# print("Data has been written")
import pandas as pd
import csv
import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root123",
    database="supermarket"
)

mycursor = db.cursor()

sql = "insert into tab(stock_name, product_price, available_quantity) values (%s,%s,%s)"

filename = 'stock.csv'
file = open(filename, 'a', newline='')
writer = csv.writer(file)

if file.tell() == 0:
    header = ['stock name', 'product price', 'available quantity']
    writer.writerow(header)

values = []
while True:
    stock_name = input("Enter stock name: ")
    while True:
        try:
            product_price = float(input("Enter product price: "))
            break
        except ValueError:
            print("Invalid input. Please enter a valid number.")
    available_quantity = int(input("Enter available quantity: "))
    writer.writerow([stock_name, product_price, available_quantity])
    values.append((stock_name, product_price, available_quantity))
    add_more = input("Do you want to add more? (yes/no): ").strip().lower()
    if add_more != 'yes':
        break

file.close()

mycursor.executemany(sql, values)
db.commit()
print("Data has been written")