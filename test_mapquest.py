from json import JSONDecodeError
from urllib.parse import urlencode 
from typing import Dict
from requests import get

def test_location(origin=None, destination=None) -> Dict:
    main_api = "https://www.mapquestapi.com/directions/v2/route?"
    key = "YgdNCMGADzfWaERY5bk0e3bxEZcCRJzu"

    url = main_api + urlencode({"key":key, "from":origin, "to":destination})

    try :
        json_data = get(url).json()
    except JSONDecodeError :
        print("\nUnexpected Error happened: Key maybe invalid")
        return 1
    
    json_status = json_data["info"]["statuscode"]
    return json_status

def test_api():
    test_location_var = test_location("Manila, Philippines", "Cavite, Philippines")
    assert test_location_var == 0