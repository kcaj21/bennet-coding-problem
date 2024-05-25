import requests
import sys
import pdb


def main(chemical_code):
    name = get_chemical_name(chemical_code)
    print(name)
    
    icb_spending_data = get_icb_spending_data(chemical_code)
    for row in icb_spending_data:
        print(row)
    # print(icb_spending_data)

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
    
    #sorting the results by items 1st, date 2nd, so the first object per date will contain highest items value
    results.sort(key=lambda x: x["items"], reverse=True)
    results.sort(key=lambda x: x["date"], reverse=True)
    
    #creating a list of the unique dates from the json data
    unique_dates = {res["date"] for res in results}
    
    #instantiating a new list to add only the ojects with the highest items value per date
    new_list = []
    
    #using the unique dates to iterate over the json data
    for date in unique_dates:
        # print(date)
        
        #per iteration, filtering for objects per date and adding them to a temporary list
        filtered_list = list(
        filter(
        lambda x: x["date"] == date,
        results
        )
        )
        # print("HELLO LIST")
        # print(filtered_list)
        
        #filtering the temporary list for objects where the items value is equal to the highest items value (I'm not simply returning the first record, because there could be more than one icb per date sharing the same items value)
        final_list = list(
        filter(
        lambda x: x["items"] == filtered_list[0]["items"],
        filtered_list
        )
        )
        # print(final_list)
        #adding the result of the iteration to the new_list variable
        new_list.extend(final_list)
        
    #sorting again by date, as the unique_dates variable is an unordered set
    new_list.sort(key=lambda x: x["date"], reverse=True)

    #creating the final spend_data list through list comprehension, only including the date, icb and amount properties    
    spend_data = [res["date"] + " " + res["row_name"] + " " + str(res["items"]) for res in new_list]

    return spend_data
    
if __name__ == "__main__":
    chemical_code = sys.argv[1]
    main(chemical_code)
