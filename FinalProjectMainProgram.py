import csv
from datetime import datetime

# This first function is made to read csv files and separate each line into their own separate list.
def readFile(filename):
    with open(filename, 'r', newline='') as file:
        return list(csv.reader(file))
# This function is used to write the contents from the created lists from above to a new csv file. """
def writeToFile(filename, contents):
    """Writes contents to a CSV file without headers."""
    with open(filename, 'w', newline='') as file:
        csv.writer(file).writerows(contents)

# This is a sorting function that works by checking the value of the data located in a specific column.
def sort(contents, index, reverseOrder=False):
    n = len(contents)
    for i in range(n):
        for j in range(n - i - 1):
            if (reverseOrder and contents[j][index] < contents[j + 1][index]) or \
               (not reverseOrder and contents[j][index] > contents[j + 1][index]):
                contents[j], contents[j + 1] = contents[j + 1], contents[j]
    return contents

# this is the main function that will incorporate the functions from above. 
# It is used to go through the data provided in the files and separate the needed results into separate files.

def analyze(manufacturerFilename, priceFilename, serviceDatesFilename):
    ManufacturerList = readFile(manufacturerFilename)
    PriceList = readFile(priceFilename)
    ServiceDatesList = readFile(serviceDatesFilename)
# creating dictionaries for price and service date
    prices = dict((row[0], row[1]) for row in PriceList)
    serviceDates = dict((row[0], row[1]) for row in ServiceDatesList)
    contents = [
        [
            item[0],
            item[1],
            item[2],
            prices.get(item[0], ''),
            serviceDates.get(item[0], ''),
            item[3] if len(item) > 3 else 'No'
        ]
        for item in ManufacturerList
    ]
    # writing to the full inventory file
    writeToFile('FullInventory.csv', sort(contents[:], 1))

    itemTypes = set(item[2] for item in contents)
    for itemType in itemTypes:
        writeToFile(
            f'{itemType}Inventory.csv',
            sort([item for item in contents if item[2] == itemType], 0)
        )
    # setting a formula to determine the current date. The formula will compare the current date to the service date. 
    # if the date is passed, it will write the neccessary data to the file "pastservicedate"
    today = datetime.today().strftime('%m/%d/%Y')
    pastServiceInventory = [
        item for item in contents
        if item[4] and datetime.strptime(item[4], '%m/%d/%Y') < datetime.strptime(today, '%m/%d/%Y')
    ]
    writeToFile('PastServiceDateInventory.csv', sort(pastServiceInventory, 4))
    # checking if any item is damaged. If so the data for that item will be written to the damagedinventory file.
    damagedInventory = [item for item in contents if item[5] == 'damaged']
    writeToFile('DamagedInventory.csv', sort(damagedInventory, 3, reverseOrder=True))


