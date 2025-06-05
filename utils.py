import os, pymysql
from dotenv import load_dotenv
load_dotenv()  # take environment variables from.env

db_user = os.getenv("USER")
db_password = os.getenv("PASSWORD")
db_host = os.getenv("HOST")
db_name = os.getenv("NAME")

connection = pymysql.connect(host=db_host,
                             user=db_user,
                             password=db_password,
                             database=db_name,
                             cursorclass=pymysql.cursors.DictCursor)

with connection:
    with connection.cursor() as cursor:
        # Create a new record
        sql = "SELECT brand FROM t_shirts limit 3"
        cursor.execute(sql)
        result =cursor.fetchall()
        print(result)
    # connection is not autocommit by default. So you must commit to save
    # your changes.
    connection.commit()


def update_stock(host, user, password, name) -> None:
    while True:
        brand = input("Enter the brand of the t-shirt you want to restock: ")
        brand.upper()
        if brand in {'ADIDAS', 'NIKE', 'PUMA', 'VAN HUESEN'}:
            break
        else:
            print("Invalid brand. Please choose from Adidas, Nike, Puma, or Van Huesen.\n")

    while True:
        color = input("Enter the color of the t-shirt you want to restock: ")
        color.upper()
        if brand in {'BLACK', 'BLUE', 'RED'}:
            break
        else:
            print("Invalid color. Please choose from Black, Blue, or Red.\n")
    
    while True:
        size = input("Enter the size of the tshirt: ")
        size=size.upper
        if size in {'XS','S','M', 'L'}:
            break
        else:
            print("Invalid size. Please choose from XS, S, M, or L.\n")
    
    while True:
        restock_amount = input("Enter the number of tshirts you are restocking: ")
        try:
            restock_amount = int(restock_amount)
            break
        except:
            print("Invalid input. Please enter a number.\n")

    connection = pymysql.connect(host=host,
                             user=user,
                             password=password,
                             database=name,
                             cursorclass=pymysql.cursors.DictCursor)
    # with connection.cursor() as cursor:
    #     sql = "UPDATE t_shirts SET stock_quantity = {stock_amount} WHERE brand = {brand} AND size = {size} AND color ={color}"
    #     cursor.execute(sql)
    #     connection.commit()
update_stock(host=db_host,user=db_user,password=db_password, name=db_name)