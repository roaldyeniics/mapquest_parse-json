from json import JSONDecodeError
import urllib.parse
import requests

def test_location(key, origin, destination):
    main_api = "https://www.mapquestapi.com/directions/v2/route?"
    key = "YgdNCMGADzfWaERY5bk0e3bxEZcCRJzu"

    url = main_api + urllib.parse.urlencode({"key":key, "from":origin, "to":destination})

    try :
        json_data = requests.get(url).json()
    except JSONDecodeError :
        print("\nUnexpected Error happened: Key maybe invalid")
    
    json_status = json_data["info"]["statuscode"]
    return json_status

def test_api():
    test_location_var = test_location("YgdNCMGADzfWaERY5bk0e3bxEZcCRJzu", "Manila, Philippines", "Cavite, Philippines")
    assert test_location_var == 0
