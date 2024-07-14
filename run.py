from dateutil import parser

import gspread
from google.oauth2.service_account import Credentials
from tabulate import tabulate
from pprint import pprint
from simple_term_menu import TerminalMenu
import time


# Scope definition
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]
# Get API google sheet working
CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open("waste_data")

# Function to select worksheet
def select_worksheet():
    """
    Function that selects a collector worksheet using a terminal menu
    """
    options = ["collector-a", "collector-b", "collector-c", "Back to Main Menu"]
    terminal_menu = TerminalMenu(options)
    menu_entry_index = terminal_menu.show()
    selection = options[menu_entry_index]

    if selection in ["collector-a", "collector-b", "collector-c"]:
        return selection
    else:
        return None

def get_integer_input(prompt):
    """
    Get integer input from the user using a terminal menu.
    """
    while True:
        try:
            value = int(input(prompt))
            if value < 0:
                print("Please enter a positive integer.")
            elif value > 400:
                print("Please enter a value less than or equal to 400 tonnes.")
            else:
                return value
        except ValueError:
            print("Invalid input. Please enter a positive integer.")

def get_monthly_waste_data():
    """
    Get monthly waste figures input from user using terminal menu
    """
    print("Please enter the weight of the following waste types in Tonnes")
    print("Values must be poistive and less than or equal to 400")
    prompts = [
        "Enter C & D waste: ",
        "Enter Black bin waste: ",
        "Enter Green bin waste: ",
        "Enter Brown bin waste: "
    ]

    data = []
    for prompt in prompts:
        data.append(get_integer_input(prompt))

    return data

def validate_data(values):
    """
    Check if all values are positive integers and exactly 4 values are provided
    """
    try:
        # Check if all values are positive integers
        if not all(isinstance(value, int) and value >= 0 for value in values):
            raise ValueError("All values must be positive integers.")
        # Check if exactly 4 values are provided
        # if len(values) != 4:
        #     raise ValueError(
        #         f"Exactly 4 values required, you provided {len(values)}"
        #     )
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")
        return False

    return True

def update_worksheet(data, worksheet_name):
    """
    Receives a list of integers to be inserted into a worksheet
    Update the relevant worksheet with the data to be provided
    Data should be entered into column H
    """
    print(f"Updating {worksheet_name} worksheet...\n")
    worksheet_to_update = SHEET.worksheet(worksheet_name)
    next_empty_row = find_next_empty_row(worksheet_to_update)

    if next_empty_row is None:
        print(f"Cannot enter data: {worksheet_name} worksheet is full.\nYou have entered all the data for this year.")
        return

    # Ensure we are updating column C only
    for i, value in enumerate(data):
        cell = f'C{next_empty_row + i}'
        worksheet_to_update.update_acell(cell, value)

    print(f"{worksheet_name} worksheet updated successfully\n")

def find_next_empty_row(worksheet):
    """
    Function to find the next empty cell in column C
    """
    col_c = worksheet.col_values(3)  # Column C is index 3 (1-based index)
    next_empty_row = len(col_c) + 1  # Index of the next empty cell

    if next_empty_row > 49:
        return None # No empty rows available within the limit
        
    return next_empty_row

def display_worksheet(worksheet_name):
    """
    Fetch and display the current data of the selected worksheet.
    """
    worksheet = SHEET.worksheet(worksheet_name)
    data = worksheet.get_all_values()
    
    print(f"\nCurrent data in {worksheet_name} worksheet:")
    print(tabulate(data, headers="firstrow", tablefmt="grid"))
    print("\n")

def data_entry():
    """
    Function to handle data entry
    """
    while True:
    # Select worksheet
        worksheet_name = select_worksheet()
        if worksheet_name is None:
                return  # Exit data entry

        # Get monthly waste data
        data = get_monthly_waste_data()
        if data is None:
                return  # Exit data entry

        waste_data = [int(num) for num in data]

        # Update the selected worksheet with the waste data
        update_worksheet(waste_data, worksheet_name)
        # Display the current worksheet data
        display_worksheet(worksheet_name)

def validate_all_data_entered(worksheet):
    """
    Validate that all data for the 2023 year has been entered in the worksheet.
    """
    data_range = worksheet.range('A1:C49')
    for cell in data_range:
        if cell.value == '':
            return False
    return True

def calculate_profit_for_sheet(worksheet_name):
    """
    Calculate the profit for a specific collector worksheet.
    The tonnes collected per waste type will be multiplied by the corresponding 
    price per tonne in the prices worksheet.
    """
    print(f"Calculating the profit for the worksheet {worksheet_name}. This may take a while...\n")

    worksheet = SHEET.worksheet(worksheet_name)

    if not validate_all_data_entered(worksheet):
        print(f"Cannot calculate profit: Not all data for the 2023 year has been entered in {worksheet_name}.\n")
        return

    # Get prices data from the 'prices' worksheet
    prices_sheet = SHEET.worksheet('prices')
    prices_data = prices_sheet.get_all_values()
    prices = {
        "C & D": float(prices_data[1][1]),
        "Black bin": float(prices_data[2][1]),
        "Green bin": float(prices_data[3][1]),
        "Brown bin": float(prices_data[4][1])
    }

    worksheet = SHEET.worksheet(worksheet_name)
    waste_data = worksheet.col_values(3)[1:]  # Skip header
    if not waste_data:
        print(f"No waste data found in {worksheet_name}.")
        return
    waste_data = [float(val) for val in waste_data if val]
    profits = []

    total_waste = 0
    for idx, waste in enumerate(waste_data):
        total_waste += waste
        if idx % 4 == 0:
            profit = waste * prices["C & D"]
        elif idx % 4 == 1:
            profit = waste * prices["Black bin"]
        elif idx % 4 == 2:
            profit = waste * prices["Green bin"]
        elif idx % 4 == 3:
            profit = waste * prices["Brown bin"]
        profits.append(profit)

    total_profit = sum(profits)

    # Update the profit column (D)
    for i, profit in enumerate(profits):
        cell = f'D{i + 2}'
        worksheet.update_acell(cell, profit)
        time.sleep(1)  # Add a delay to prevent exceeding rate limits

    # Update total waste and total profit in cells C50 and D50
    worksheet.update_acell('C50', total_waste)
    worksheet.update_acell('D50', total_profit)

    print(f"Profit calculation for {worksheet_name} completed successfully.")

    # display the updated worksheet
    display_worksheet(worksheet_name)

    print("Please select another sheet to calculate profit for or choose to return to main menu\n")

def calculate_profit():
    """
    Function to calculate the profit for a selected collector worksheet.
    """
    while True:
        worksheet_name = select_worksheet()
        if worksheet_name is None:
            return  # Exit profit calculation
    
        calculate_profit_for_sheet(worksheet_name)

def main():
    """
    Main function to run the program
    """

    print('Welcome to Waste Data Analyzer')
    print('This program can allow the user to input the waste collected into a database')
    print('When the waste data is up to date for the year the user can then run calculate the profit and have it displayed to them in table format\n')
    print('When the data has been entered succesfully, you can run the profit report for 2023\n')
    

    options = ["Data Entry", "Calculate Profit", "Exit"]
    terminal_menu = TerminalMenu(options)
    
    while True:
        menu_entry_index = terminal_menu.show()
        selection = options[menu_entry_index]

        if selection == "Data Entry":
            data_entry()
        elif selection == "Calculate Profit":
            calculate_profit()
        elif selection == "Exit":
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.\n")

if __name__ == "__main__":
    main()