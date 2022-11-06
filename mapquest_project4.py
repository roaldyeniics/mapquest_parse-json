from json import JSONDecodeError
import urllib.parse
import requests
import webbrowser
import time
import pwinput
from colorama import init, Fore

#Initialize Colorama
init(autoreset=True)

main_api = "https://www.mapquestapi.com/directions/v2/route?"

#Mask Key with '*'
key = pwinput.pwinput(prompt='Enter your key: ', mask = '*')

#Global variable for choices
try_again = ""
unit_choice = ""

while True:
    #Input Starting location
    orig = input(Fore.GREEN + "Starting Location: ")
    if orig.lower() == "quit" or orig.lower() == "q":
        break

    #Input Destination location
    dest = input(Fore.GREEN + "Destination: ")
    if dest.lower() == "quit" or dest.lower() == "q":
        break

    #Select Unit of Measruement
    while True:
        unit_choice = input(Fore.GREEN + "Select unit of measurement [km/mi]: ")
        if (unit_choice.lower() == "km"):
            break
        elif (unit_choice.lower() == "mi"):
            break
        else:
            print(Fore.RED + "\nPlease enter a valid unit of measurement.\n")

    #URL 
    url = main_api + urllib.parse.urlencode({"key":key, "from":orig, "to":dest})
    print(Fore.YELLOW + "\nURL: " + (url) + "\n")

    try :
        json_data = requests.get(url).json()
    except JSONDecodeError :
        print("\nUnexpected Error happened: Key maybe invalid")
        key = pwinput.pwinput(prompt='Enter your key: ', mask = '*')
        continue
        
    json_status = json_data["info"]["statuscode"]

    if json_status == 0:
        #Route Call Success
        print(Fore.GREEN + "API Status: " + str(json_status) + " = A successful route call.\n")

        #Display information regarding Direction, Trip Duration, km/mi, Fuel used
        print(Fore.BLUE + "="*100)
        print(Fore.BLUE + "Directions from " + (orig) + " to " + (dest))
        print(Fore.BLUE + "Trip Duration: " + (json_data["route"]["formattedTime"]))
        
        if (unit_choice.lower() == "km"):
            print(Fore.BLUE + "Kilometers: " + str("{:.2f}".format((json_data["route"]["distance"])*1.61)))
        elif (unit_choice.lower() == "mi"):
            print(Fore.BLUE + "Miles: " + str("{:.2f}".format(json_data["route"]["distance"])))

        print(Fore.BLUE + "Fuel Used (Ltr): " + str("{:.2f}".format((json_data["route"]["fuelUsed"])*3.78)))
        print(Fore.BLUE + "="*100 + "\n") 

        #Display detailed direction information
        print(Fore.MAGENTA + "=" * 100) 
        for each in json_data["route"]["legs"][0]["maneuvers"]:
            print(Fore.MAGENTA + (each["narrative"])+ " (" + str("{:.2f}".format((each["distance"])*1.61) + " km)"))

        print(Fore.MAGENTA + "=" * 100 + "\n") 

        #Opens URL after 2 seconds
        print(Fore.YELLOW + "URL opening in browser after 2 seconds...\n")
        time.sleep(2)
        webbrowser.open(url)

    elif json_status == 402:
        print(Fore.RED + "*" * 100)
        print(Fore.RED + "Status Code: " + str(json_status) + ". Invalid user inputs for one or both locations.")
        print(Fore.RED + "*" * 100 + "\n")

    elif json_status == 611:
        print(Fore.RED + "*" * 100)
        print(Fore.RED +"Status Code: " + str(json_status) + ". Missing an entry for one or both locations.")
        print(Fore.RED +"*" * 100 + "\n")

    else:
        print(Fore.RED + "*" * 100)
        print(Fore.RED +"For Status Code: " + str(json_status) + ". Refer to: ")
        url_refer = "https://developer.mapquest.com/documentation/directions-api/status-codes"
        print(Fore.YELLOW + url_refer)
        print(Fore.RED + "*" * 100 + "\n")
        
        #Opens Status Code URL after 2 seconds
        print(Fore.YELLOW + "Status Code Documentation opening in browser after 2 seconds...")
        time.sleep(2)
        webbrowser.open(url_refer)
    
    #Validation if user wants to try again
    try_again = input(Fore.GREEN + 'Input another location? (Y/N): ')
    print("")
    if (try_again.lower() == 'yes' or try_again.lower() == 'y'):
        continue
    else:
        break
