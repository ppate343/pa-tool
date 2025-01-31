import csv


def load_payer_mapping(payer_file):
    payer_mapping = {}
    with open(payer_file, mode="r", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        print("Detected Headers:", reader.fieldnames)
        for row in reader:
            payer_mapping[row["insuranceName"]] = row["tradingPartnerServiceId"]
    return payer_mapping

def update_patients_file(patients_file, payer_mapping, output_file):
    with open(patients_file, mode='r') as infile, open(output_file, mode='w', newline='') as outfile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for row in reader:
            insurance_name = row["insuranceName"]
            if insurance_name in payer_mapping:
                row["tradingPartnerServiceId"] = payer_mapping[insurance_name]
            writer.writerow(row)

payer_file = "data/uniquePayers.csv"
patients_file = "data/patients-before.csv"
output_file = "data/patients-after.csv"


payer_mapping = load_payer_mapping(payer_file)
update_patients_file(patients_file, payer_mapping, output_file)