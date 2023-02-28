'''
This program uses inventory.txt as an input an allows the user:
view all inventory, capture shoes, restock, search shoe, calculate total value of a product, and
display the product with the highest quantity.
'''


from tabulate import tabulate


# It creates Shoe class
class Shoe:

    def __init__(self, country, code, product, cost, quantity):
        self.country = country
        self.code = code
        self.product = product
        self.cost = cost
        self.quantity = quantity

    def get_cost(self):
        return self.cost

    def get_quantity(self):
        return self.quantity

    def __str__(self):
        return f'{self.product}, {self.country}, {self.product}, {self.cost}, {self.quantity}'


# shoe_list will be used to store a list of objects of Shoe.
shoe_list = []


''' Below function opens and reads inventory.txt, split each line, 
creates Shoe objects(except first line, header) and append the objects into the shoe_list.'''


def read_shoes_data():
    try:
        with open('inventory.txt', 'r') as f1:
            for line in f1:
                split_line = line.split(",")
                if split_line[0] != "Country":
                    split_line = Shoe(split_line[0], split_line[1], split_line[2], int(split_line[3]),
                                      int(split_line[4]))
                    shoe_list.append(split_line)

    # If the file not found it creates the file(with try-except function)
    except FileNotFoundError:
        with open('inventory.txt', 'w') as f1:
            return True


'''Below function requests data about a shoe and creates a shoe object.
It adds the object to the shoe list and to inventory.txt '''


def capture_shoes():
    
    try:
        country = input("Please enter country of shoes:")
        code = input("Please enter code of shoes:")
        product = input("Please enter product name:")
        cost = int(input("Please enter cost of product:"))
        quantity = int(input("Please enter quantity of shoes:"))
        shoe_new = Shoe(country, code, product, cost, quantity)  # Creates new objects according to the entered data.
        shoe_list.append(shoe_new)

        try:
            with open("inventory.txt", "r+") as f1:
                f1.seek(0, 2)
                f1.write(f"{shoe_new.country},{shoe_new.code},{shoe_new.product},{int(shoe_new.cost)},{int(shoe_new.quantity)}")

        # if inventory.txt not found below except function runs
        except FileNotFoundError:
            with open("inventory.txt", "w") as f1:
                return True

    # If the user enter invalid input try-except function runs for the ValueError
    except ValueError:
        print("You entered invalid number, please try again...")


''' Below function display shoes list as a table with tabulate module.'''


def view_all():
    
    shoe_list_str = [["Country", "Code", "Product", "Cost", "Quantity"]]

    # It iterates over the shoes list and gets details and adds the details in shoe_list_str list.
    for shoe in shoe_list:
        shoe_str = [shoe.country, shoe.code, shoe.product, shoe.cost, shoe.quantity]
        shoe_list_str.append(shoe_str)
        

    ''' It displays the data as a table with index. Index starts with 1 and ends with the number of len(shoe_list).
    First line of the list will be headers.'''

    print(tabulate(shoe_list_str, headers='firstrow', tablefmt='fancy_grid', intfmt=',',
                   showindex=range(1, len(shoe_list) + 1)))


''' Below function finds the shoe object with the lowest quantity and asks the user if they
    want to increase this quantity of shoes and then updates it in the list and in the text file.'''


def re_stock():
    
    quantity_dict = {}
    shoe_list_str = []

    # It iterates over the shoes list and gets details and adds the all details in shoe_list_str list.
    for shoe in shoe_list:
        shoe_str = [shoe.country, shoe.code, shoe.product, shoe.cost, shoe.quantity]
        shoe_list_str.append(shoe_str)

        # It adds product as a key and quantity as a value to the quantity_dict dictionary.
        quantity_dict[shoe.product] = int(shoe.quantity)

    # It finds min quantity and product from quantity_dict
    min_product = min(quantity_dict.items(), key=lambda x: x[1])
    
    print(f"\n{min_product[0]} has the lowest stock with the quantity of {min_product[1]}.")

    try:
        # It requests new quantity, if the user enter a non integer input, try-except runs for ValueError

        new_quantity = int(input(f'''If you want to increase the stock level of {min_product[0]}, 
enter the new amount to revise it or -1 to return main menu\n'''))

        # to go main menu
        if new_quantity == -1:
            pass

        # If entered new quantity is less than or equals to the current stock, it doesn't change anything.
        elif new_quantity < min_product[1]:
            print("You entered a number less than stock level! Try again...")

        elif new_quantity == min_product[1]:
            pass

        # If entered new quantity is greater than min stock level, it opens inventory.txt and revises the quantity.
        elif new_quantity > min_product[1]:
            
            try:
                with open("inventory.txt", "r+") as f1:
                    f1.seek(0)
                    f1.write("Country,Code,Product,Cost,Quantity\n")

                    # It iterates over shoe_list_str to find the product which is same as min_product[0] from quantity_dict.
                    for shoe_str in shoe_list_str:
                        if shoe_str[2] == min_product[0]:
                            shoe_str[4] = new_quantity  # revise the quantity

                        # It writes data from shoe_list_str list to the inventory.txt
                        f1.write(f"{shoe_str[0]},{shoe_str[1]},{shoe_str[2]},{shoe_str[3]},{shoe_str[4]}\n")

            except FileNotFoundError:
                with open("inventory.txt", "w") as f1:
                    return True

            # It revises shoe_list
            for shoe in shoe_list:
                if shoe.product == min_product[0]:
                    shoe.quantity = new_quantity
    except ValueError:
        print("You entered invalid number! Please try again...")


# Below function requests shoe code and searches for the shoe from the list using the code and display the object.

def search_shoe():

    shoe_code_search = input("Please enter the shoe code to display:")
    shoe_searched = [["Country", "Code", "Product", "Cost", "Quantity"]]

    for shoe in shoe_list:
        if shoe.code.strip() == shoe_code_search:
            shoe_searched.append([shoe.country, shoe.code, shoe.product, shoe.cost, shoe.quantity])
            print(tabulate(shoe_searched, headers='firstrow', tablefmt='fancy_grid', intfmt=','))


''' This function calculates the total value for each item (value = cost * quantity), and 
displays the data as a table with tabulate function'''

def value_per_item():

    # It adds title into the shoe_value_list
    shoe_value_list = [["Code", "Product", "Total value of the product"]]

    # Below loop calculates total values and append into the shoe_value_list.
    for shoe in shoe_list:
        shoe_value = [shoe.code, shoe.product, shoe.cost * shoe.quantity]
        shoe_value_list.append(shoe_value)

    # Displays total values
    print(tabulate(shoe_value_list, headers='firstrow', tablefmt='fancy_grid', intfmt=',',
                   showindex=range(1, len(shoe_list) + 1)))


# Below function finds the product with the highest quantity and displays it should be on sale.

def highest_qty():
    
    quantity_dict = {}
    shoe_list_str = []

    # It iterates over the shoes list and gets details and adds the all details in shoe_list_str list.
    for shoe in shoe_list:
        shoe_str = [shoe.country, shoe.code, shoe.product, shoe.cost, shoe.quantity]
        shoe_list_str.append(shoe_str)

        # It adds product as a key and quantity as a value to the quantity_dict dictionary.
        quantity_dict[shoe.product] = int(shoe.quantity)

    # It finds max quantity and product from quantity_dict
    max_product = max(quantity_dict.items(), key=lambda x: x[1])

    print(f'''\n{max_product[0]} has the highest stock with the quantity of {max_product[1]}.
This product should be on sale.\n''')


# it calls read_shoes_data() function to read the data from inventory.txt and adds shoe_list
read_shoes_data()


# Below menu requests user to enter an option until enter 'q' with while loop.

while True:
    
    menu = input('''\nPlease select one of the following options below:
    1  -  view all inventory
    2  -  capture shoes
    3  -  restock
    4  -  search shoe
    5  -  calculate total value of a product
    6  -  display the product with the highest quantity 
    0  -  quit''').lower()

    # view all inventory
    if menu == "1":
        view_all()

    # capture shoes
    elif menu == "2":
        capture_shoes()

    # restock
    elif menu == "3":
        re_stock()

    # search shoe
    elif menu == "4":
        search_shoe()

    # calculate total value of a product
    elif menu == "5":
        value_per_item()

    # display the product with the highest quantity
    elif menu == "6":
        highest_qty()

    # quit
    elif menu == "0":
        break

    else:
        print("You enter invalid option. Please try again...")
