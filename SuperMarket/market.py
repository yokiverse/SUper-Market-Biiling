import pandas as pd
import smtplib
from datetime import datetime
import mysql.connector

# Connect to MySQL database
def connect_to_db():
    return mysql.connector.connect(
        host="localhost",  # e.g., "localhost"
        user="root",  # e.g., "root"
        password="root123",  # e.g., "password"
        database="supermarket"  # e.g., "shopping_system"
    )

def create_table_if_not_exists(conn):
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS purchases (
        id INT AUTO_INCREMENT PRIMARY KEY,
        email VARCHAR(255),
        total_cost FLOAT,
        purchased_items TEXT,
        purchase_time DATETIME
    )
    """)
    conn.commit()
    cursor.close()

def insert_purchase(conn, email, total_cost, purchased_items, purchase_time):
    cursor = conn.cursor()
    query = "INSERT INTO purchases (email, total_cost, purchased_items, purchase_time) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (email, total_cost, purchased_items, purchase_time))
    conn.commit()
    cursor.close()

def available_stock(df):
    print("Available stock names:")
    for stock_name in df['stock name']:
        print(stock_name)

def purchase_product(df, conn):
    total_cost = 0
    gst = 0.8
    bill_items = []
    while True:
        enter_product = input("Enter the name of the product you want to buy (or 'exit' to exit): ")
        if enter_product.lower() == 'exit':
            print("\nBill is Printing")
            break
        if enter_product in df['stock name'].values:
            product_details = df[df['stock name'] == enter_product]
            while True:
                try:
                    how_many = int(input(f"How many {enter_product} do you want to buy? "))
                    if how_many <= 0:
                        print("Please enter a valid quantity greater than zero.")
                    elif how_many > product_details['available quantity'].values[0]:
                        print(f"Sorry, we only have {product_details['available quantity'].values[0]} units available.")
                    else:
                        original_index = product_details.index[0]
                        df.at[original_index, 'available quantity'] -= how_many
                        cost_per_unit = product_details['product price'].values[0]
                        total_product_cost = how_many * cost_per_unit
                        gst_amount = total_product_cost * gst
                        total_product_cost_with_gst = total_product_cost + gst_amount
                        total_cost += total_product_cost_with_gst
                        bill_items.append({"Product": enter_product,
                                           "Quantity": how_many,
                                           "Price per unit": cost_per_unit,
                                           "GST Amount": gst_amount,
                                           "QuantityTotal cost": total_product_cost_with_gst})
                        print(f"You can buy {how_many} {enter_product} at ${cost_per_unit:.2f} each.")
                        print(f"Total cost for {how_many} {enter_product} (incl. GST): ${total_product_cost_with_gst:.2f}")
                        break
                except ValueError:
                    print("Invalid input. Please enter a valid number.")
        else:
            print(f"Product '{enter_product}' not found. Please enter a valid product name.")
    if bill_items:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print("\nBill")
        print(f"Date and Time: {current_time}")
        purchased_items_summary = ""
        for item in bill_items:
            purchased_items_summary += f"{item['Quantity']} {item['Product']} at ${item['Price per unit']:.2f} each. Total (incl. GST): ${item['QuantityTotal cost']:.2f}\n"
            purchased_items_summary += f"  GST Amount: ${item['GST Amount']:.2f}\n"
            print(purchased_items_summary)
        print(f"\nTotal Bill Amount (incl. GST): ${total_cost:.2f}")
        df.to_csv('stock.csv', index=False)
        print("Stock file updated.")
        enter_mail = input("Enter email id to get bill (or 'exit' to exit): ")
        if enter_mail.lower() != 'exit':
            send_mail(enter_mail, bill_items, total_cost, current_time)
            insert_purchase(conn, enter_mail, total_cost, purchased_items_summary, current_time)
            print("Purchase information saved to database.")
        else:
            print("No email provided, purchase information not saved to database.")
    else:
        print("No items purchased. Exiting...")
    print("Thank you for shopping with us!")


def send_mail(enter_mail, bill_items, total_cost, current_time):
    try:
        smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
        smtp_server.starttls()
        smtp_server.login('yokeshraja01@gmail.com', 'ntyb emqv svnt exdq')
        subject = 'Your Purchase Bill'
        head = f"\nDate and Time: {current_time}\n"
        head += "\nBill Summary\n"
        for item in bill_items:
            head += f"{item['Quantity']} {item['Product']} at ${item['Price per unit']:.2f} each. Total: ${item['QuantityTotal cost']:.2f}\n"
            head += f"  GST Amount: ${item['GST Amount']:.2f}\n"
        head += f"\nTotal Bill Amount (incl. GST): ${total_cost:.2f}"
        message = f"Subject: {subject}\n\n{head}"
        smtp_server.sendmail('yokeshraja01@gmail.com', enter_mail, message)
        smtp_server.quit()
        print(f"Bill sent successfully to {enter_mail}")
    except Exception as e:
        print(f"Failed to send email. Error: {str(e)}")

def main():
    df = pd.read_csv('stock.csv')
    available_stock(df)
    conn = connect_to_db()  # Connect to the database
    create_table_if_not_exists(conn)  # Create the purchases table if it doesn't exist
    while True:
        purchase_product(df, conn)
        next_customer = input("Do you want to continue with another customer? (yes/no): ")
        if next_customer.lower() != 'yes':
            break
    conn.close()  # Close the database connection
    print("Thank you for using our shopping system!")

if __name__ == "__main__":
    main()