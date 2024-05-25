import requests
import sys
import pdb


def main(chemical_code):
    name = get_chemical_name(chemical_code)
    print(name)
    
    icb_spending_data = get_icb_spending_data(chemical_code)
    for row in icb_spending_data:
        print(row)

def get_chemical_name(chemical_code):
    
    # checks the chemical code entered is 9 characters long
    if not (len(chemical_code) == 9):
        raise ValueError("must be 9 character chemical code")
    
    # fetches the chemical name from the api
    url = "https://openprescribing.net/api/1.0/bnf_code"
    resp = requests.get(url, params={"q": chemical_code, "exact": "true", "format": "json"})
    resp.raise_for_status()
    
    results = resp.json()
    
    # checks if there are any results returned from the get request
    if (len(results) == 0):
        raise ValueError("not found")
        
    # Exact matches return just one result if the code is found or none if it is not
    result = results[0]

    return result["name"]

def get_icb_spending_data(chemical_code):
    
    # fetches the spending data from the api
    url = "https://openprescribing.net/api/1.0/spending_by_org/?"
    resp = requests.get(url, params={"code": chemical_code, "format": "json", "org_type": "icb"})
    resp.raise_for_status()
    
    results = resp.json()
    
    #creating new list through list comprehension, only including the date, icb and amount properties    
    spend_data = [res["date"] + " " + res["row_name"] + " " + str(res["items"]) for res in results]
    
    return spend_data
    
if __name__ == "__main__":
    chemical_code = sys.argv[1]
    main(chemical_code)
