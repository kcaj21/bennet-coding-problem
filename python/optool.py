import requests
import sys
import pdb

def main(chemical_code):
    name = get_chemical_name(chemical_code)
    print(name)


def get_chemical_name(chemical_code):
    
    if not (len(chemical_code) == 9):
        raise ValueError("must be 9 character chemical code")
    
    url = "https://openprescribing.net/api/1.0/bnf_code"
    resp = requests.get(url, params={"q": chemical_code, "exact": "true", "format": "json"})
    # pdb.set_trace()
    resp.raise_for_status()
    
    results = resp.json()
    
    if (len(results) == 0):
        raise ValueError("not found")
        
    # Exact matches return just one result if the code is found or none if it is not
    result = results[0]

    return result["name"]


if __name__ == "__main__":
    chemical_code = sys.argv[1]
    main(chemical_code)
