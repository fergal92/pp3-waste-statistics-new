import gspread
from google.oauth2.service_account import Credentials
from tabulate import tabulate
from pprint import pprint

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
    Function that selects a collector worksheet
    """
    while True:
        worksheet_name = input("Enter the worksheet name to update (collector-a, collector-b, or collector-c): or 'exit' to quit:").strip().lower()
        if worksheet_name in ["collector-a", "collector-b", "collector-c"]:
            return worksheet_name
        elif worksheet_name == "exit":
            return None
        else:
            print("Invalid worksheet name. Please enter collector-a, collector-b, or collector-c.\n")

def get_monthly_waste_data():
    """
    Get monthly waste figures input from user
    """

    while True:

        print("Please enter your waste data from the last month or exit to quit")
        print("Data should be 4 numbers separated by commas")
        print("Example: 180,80,60,40")
        print("The 1st number is C & D waste,")
        print("The 2nd number is Black bin waste,")
        print("The 3rd number is Green bin waste,")
        print("The 4th number is Brown bin waste\n")

        data_str = input("Enter your data here: ")

        if data_str.lower() == "exit":
            return None

        data = data_str.split(",")
        

        if validate_data(data):
            print('Data is valid')
            break

    return data

def validate_data(values):
    """
    Inside the try, converts all string values to integers. Raises ValueError if string cannot be converted into int, or if there aren't exatly 4 values
    """

    try:
        # Convert each value to integer
        [int(value) for value in values]
        # Check if exactly 4 values are provided
        if len(values) !=4:
            raise ValueError(
                f"Exactly 4 values required, you provided {len(values)}"
            )
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

def data_analysis():
    """
    Function to handle data analysis
    """
    print("Data analysis functionality is a work in progress")

def profit_report():
    """
    Function to populate the profit columns in the collector worksheets
    The tonnes collected per waste type will be multiplied by the corresponding 
    price per tonne in the prices worksheet
    """

def main():
    """
    Main function to run the program.
    """
    print('Welcome to Waste Data Analyzer')

    while True:
        print("Please select an option:")
        print("1. Data Entry")
        print("2. Data Analysis")
        print("3. Exit")
        choice = input("Enter 1, 2 or 3: ").strip()
    
        if choice == '1':
            data_entry()
            break
        elif choice == '2':
            data_analysis()
        elif choice == '3':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please enter 1, 2 or 3.\n")

main()