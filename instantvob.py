import requests
import os
import json
from dotenv import load_dotenv

# environment variables from .env file
load_dotenv()

# API key from the environment
INSTANTVOB_API_KEY = os.getenv("INSTANTVOB_API_KEY")

# Check if the API key is loaded correctly
if not INSTANTVOB_API_KEY:
    print("API key not found in .env file.")
    exit(1)

# Setting url and params for instantvob post (minimal parameters)
url = "https://portal.instantvob.com/api/instant-vob"
headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "x-api-key": INSTANTVOB_API_KEY
}

# setting specialty id to 26 for pharmacy benefits
specialty_id = 26


def make_request(memberId, firstName, lastName, dateOfBirth, vendor):
    #payload for the API request
    payload = {
        "memberId": memberId,
        "firstName": firstName,
        "lastName": lastName,
        "dateOfBirth": dateOfBirth,
        "vendor": vendor,
        "specialtyId": specialty_id,
        "includePDF": True  
    }

 
    response = requests.post(url, json=payload, headers=headers)
    response_dir = "response"


    file_name = f"{response_dir}/{firstName}_{lastName}.json"
    with open(file_name, "w") as json_file:
        json.dump(response.json(), json_file, indent=4)

    # printing log
    if response.status_code == 200:
        print(f"Success for member {memberId}: {response.text}")
    else:
        print(f"Error for member {memberId}: {response.status_code}, {response.text}")

# Function to read CSV file of patient data and make requests
def read_csv_and_make_requests(csv_file):
    with open(csv_file, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Extract data from each row
            memberId = row["memberId"]
            firstName = row["firstName"]
            lastName = row["lastName"]
            dob = row["dob"]
            vendor = row["vendor"]

            # Make API request with extracted data
            make_request(memberId, firstName, lastName, dob, vendor)

#update path to csv
csv_file = "/data/instantVob.csv"

#read data and making request
read_csv_and_make_requests(csv_file)
