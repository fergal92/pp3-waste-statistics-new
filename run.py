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
        worksheet_name = input("Enter the worksheet name to update (collector-a, collector-b, or collector-c): ").strip().lower()
        if worksheet_name in ["collector-a", "collector-b", "collector-c"]:
            return worksheet_name
        else:
            print("Invalid worksheet name. Please enter collector-a, collector-b, or collector-c.\n")

def get_monthly_waste_data():
    """
    Get monthly waste figures input from user
    """

    while True:

        print("Please enter your waste data from the last month")
        print("Data should be 4 numbers separated by commas")
        print("Example: 180,80,60,40")
        print("The 1st number is C & D waste,")
        print("The 2nd number is Black bin waste,")
        print("The 3rd number is Green bin waste,")
        print("The 4th number is Brown bin waste\n")

        data_str = input("Enter your data here: ")

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

    # Ensure we are updating column H only

    # Ensure we are updating column H only
    for i, value in enumerate(data):
        worksheet_to_update.update_cell(next_empty_row + i, 8, int(value))  # Column H is 8 in 1-based index

    print(f"{worksheet_name} worksheet updated successfully\n")

def find_next_empty_row(worksheet):
    """
    Function to find the next empty cell in column H
    """
    col_h = worksheet.col_values(8)  # Column H is index 8 (1-based index)
    next_empty_index = len(col_h) + 1  # Index of the next empty cell
    return next_empty_index

def main():
    """
    Main function to run the program.
    """
    print('Welcome to Waste Data Analyzer')

    # Select worksheet
    worksheet_name = select_worksheet()

    # Get monthly waste data
    data = get_monthly_waste_data()
    waste_data = [int(num) for num in data]

    # Update the selected worksheet with the waste data
    update_worksheet(waste_data, worksheet_name)

main()