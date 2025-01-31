import csv
import requests
import os
import json
from dotenv import load_dotenv


# environment variables from .env file
load_dotenv()

# API key from the environment
STEDI_API_KEY = os.getenv("STEDI_API_KEY")

# Check if the API key is loaded correctly
if not STEDI_API_KEY:
    print("API key not found in .env file.")
    exit(1)

# Setting url and params for stedi eligibility checK
url = "https://healthcare.us.stedi.com/2024-04-01/change/medicalnetwork/eligibility/v3"
headers = {
    "Content-type": "application/json",
    "Authorization": STEDI_API_KEY
}


def make_request(controlNum, tradingPartnerServiceId, organizationName, npi, dateOfBirth, firstName, lastName, memberId):
    # payload for the API request
    payload = {
        "controlNumber": str(controlNum),
        "tradingPartnerServiceId": tradingPartnerServiceId,
        #setting as default for now
        "encounter": {"serviceTypeCodes": ["30"]},
        "provider": {
            "organizationName": organizationName,
            "npi": npi
        },
        "subscriber": {
            "dateOfBirth": dateOfBirth,
            "firstName": firstName,
            "lastName": lastName,
            "memberId": memberId
        }
    }

    response = requests.post(url, json=payload, headers=headers)
    
    response_dir = "response"

    # saving response by name and controlNum 
    file_name = f"{response_dir}/{firstName}_{lastName}_{controlNum}.json"
    with open(file_name, "w") as json_file:
        json.dump(response.json(), json_file, indent=4)
    
    if response.status_code == 200:
        print(f"Success for member {memberId}: Response saved to {file_name}")
    else:
        print(f"Error for member {memberId}: {response.status_code}, {response.text}")
        

def generate_control_num(start=1): 
    while True:
        yield start
        start +=1

def read_csv_and_make_requests(csv_file, output_file="updated_stedi.csv", num_rows=5):
    num_generator = generate_control_num()

    rows_to_write = []  # List to hold modified rows

    with open(csv_file, mode='r', newline='', encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        #logging file names
        print(reader.fieldnames) 
        # Prepare the fieldnames (headers), adding 'controlNum'
        fieldnames = reader.fieldnames + ['controlNum']

        for i, row in enumerate(reader):
            if i >= num_rows:  # Stop running after processing `num_rows` records
                break
            
            # create controlNum and add to column for record
            controlNum = next(num_generator)
            row['controlNum'] = controlNum

            # extracting request params from stedi.csv
            tradingPartnerServiceId = row["tradingPartnerServiceId"]
        
            #serviceTypeCodes = row["serviceTypeCodes"].split(',')  # use when column is filled out. use 30 for now (active coverage and benefits stedi default)
            organizationName = row["organizationName"]
            npi = row["npi"]
            dateOfBirth = row["dateOfBirth"]
            firstName = row["firstName"]
            lastName = row["lastName"]
            memberId = row["memberId"]

            # Call the function to make the API request
            make_request(controlNum, tradingPartnerServiceId, organizationName, npi, dateOfBirth, firstName, lastName, memberId)

            # Add the modified row to the list of rows to write back to CSV
            rows_to_write.append(row)

    # Write the modified rows to the output CSV file
    with open(output_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()  # Write the headers
        writer.writerows(rows_to_write)  # Write all the modified rows


csv_file = r"D:\Repos\pa-tool\data\stedi.csv"  # Absolute path on Windows

read_csv_and_make_requests(csv_file)