import requests
import json

# API endpoint
url = "https://healthcare.us.stedi.com/2024-04-01/change/medicalnetwork/eligibility/v3"

# API key
api_key = "test_api_key"

# Headers
headers = {
    "Authorization": f"Key {api_key}",
    "Content-Type": "application/json"
}

# Payload
payload = {
    "controlNumber": "112233445",
    "tradingPartnerServiceId": "60054",
    "provider": {
        "organizationName": "Provider Name",
        "npi": "1999999984"
    },
    "subscriber": {
        "firstName": "John",
        "lastName": "Doe",
        "memberId": "AETNA9wcSu"
    },
    "dependents": [
        {
            "firstName": "Jordan",
            "lastName": "Doe",
            "dateOfBirth": "20010714"
        }
    ],
    "encounter": {
        "serviceTypeCodes": ["30"]
    }
}

# Make the POST request
response = requests.post(url, headers=headers, json=payload)

# Print response
print(response.status_code)
print(response.json())
