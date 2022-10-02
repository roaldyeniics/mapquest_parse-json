import urllib.parse
import requests

main_api = "https://www.mapquestapi.com/directions/v2/route?"
key = "YgdNCMGADzfWaERY5bk0e3bxEZcCRJzu"

while True:
    orig = input("Starting Location: ")
    if orig == "quit" or orig == "q":
        break

    dest = input("Destination: ")
    if dest == "quit" or orig == "q":
        break
        
    url = main_api + urllib.parse.urlencode({"key":key, "from":orig, "to":dest})
    print("URL: " + (url))
    json_data = requests.get(url).json()
    json_status = json_data["info"]["statuscode"]
    
    if json_status == 0:
        print("API Status: " + str(json_status) + " = A successful route call.\n")






