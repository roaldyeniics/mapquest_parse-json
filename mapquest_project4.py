from tkinter import *
import urllib
import urllib.request
import requests
import webbrowser
import time

class MapQuest:
    def __init__(self):
        window = Tk()
        window.resizable(0,0)
        window.title("Destination Route Details using MapQuest")
        window.geometry("600x700")
        window.configure(background = "white")

        #frame for the labels and entry box
        frame1 = Frame(window)
        frame1.pack()

        #frame for the buttons
        frame3 = Frame(window)
        frame3.pack()

        #frame for the output
        frame4 = Frame(window)
        frame4.pack()
        
        #label for the starting location
        Label(frame1, text = "Starting Location: ", bg = "white").grid(row = 1, column = 1, sticky = W)

        self.startingLocation = StringVar()
        Entry(frame1, textvariable = self.startingLocation, justify = LEFT, width = 70).grid(row = 1, column = 2, sticky = W)

        #label for the destination location
        Label(frame1, text = "Destination Location: ", bg = "white").grid(row = 2, column = 1, sticky = W)

        #entry box for the destination location
        self.destinationLocation = StringVar()
        Entry(frame1, textvariable = self.destinationLocation, justify = LEFT, width = 70).grid(row = 2, column = 2, sticky = W)

        #label for the output
        Label(frame4, text = "Route Details: ", bg = "white").grid(row = 1, column = 1, sticky = W)

        #button to display the route
        Button(frame3, text = "Display Route Details", bg ="sky blue", padx = 5, command = self.displayRouteDetails).grid(row = 1, column = 1, sticky = W, padx = 5)

        #button to clear the entry boxes
        Button(frame3, text = "Clear", bg ="indian red", command = self.clear).grid(row = 1, column = 2, sticky = W, padx = 5)

        #text box for the output
        self.output = Text(frame4, width = 70, height = 35, wrap = WORD, background = "light gray")
        self.output.grid(row = 2, column = 1, sticky = W)

        window.mainloop()

    def displayRouteDetails(self):
        #get the starting location and destination location from the entry boxes
        startingLocation = self.startingLocation.get()
        destinationLocation = self.destinationLocation.get()

        main_api = "https://www.mapquestapi.com/directions/v2/route?" #API for MapQuest
        key = "YgdNCMGADzfWaERY5bk0e3bxEZcCRJzu" #Personal Consumer Key
        #YgdNCMGADzfWaERY5bk0e3bxEZcCRJzu

        #url to get the route details
        url = main_api + urllib.parse.urlencode({"key":key, "from":startingLocation, "to":destinationLocation})

        json_data = requests.get(url).json()
        json_status = json_data["info"]["statuscode"] #Checks if the route exists

        if json_status == 0: #Route exists
            #display the route information
            self.output.delete(0.0, END)
            self.output.config(fg = "black")
            self.output.insert(END, "Distance Away: ")
            self.output.insert(END, str("{:.2f}".format((json_data["route"]["distance"])*1.61) + " km/"))
            self.output.insert(END, str("{:.2f}".format((json_data["route"]["distance"])) + " mi") + "\n\n")
            self.output.insert(END, "Travel Time: " + (json_data["route"]["formattedTime"]) + "\n")
            self.output.insert(END, "Starting Address: " + startingLocation + "\n")
            self.output.insert(END, "Destination Address: " + destinationLocation + "\n")
            
            # not working anymore
            # self.output.insert(END, "Fuel Used: " + str("{:.2f}".format((json_data["route"]["fuelUsed"])*3.78) + "\n\n"))

            #display the directions
            self.output.insert(END, "Directions:\n")
            for maneuver in json_data["route"]["legs"][0]["maneuvers"]:
                directions = maneuver["narrative"]
                self.output.insert(END, directions + "\n")

            #copy text to clipboard
            self.output.clipboard_clear()
            self.output.clipboard_append(self.output.get(1.0, END))
            self.output.insert(END, "\nRoute Directions copied to clipboard\n")

            #open in browser
            self.output.insert(END, "\nURL: " + url) 
            self.output.insert(END, "\n\nURL opening in browser...")
            webbrowser.open(url)
            
        #error code 402
        elif json_status == 402:
            self.output.delete(0.0, END)
            self.output.config(fg = "red")
            self.output.insert(END, "Status Code: " + str(json_status) + ". Invalid user inputs for one or both locations.\n")
        
        #error code 611
        elif json_status == 611:
            self.output.delete(0.0, END)
            self.output.config(fg = "red")
            self.output.insert(END, "Status Code: " + str(json_status) + ". Missing an entry for one or both locations.\n")
        
        #other error codes
        else:
            self.output.delete(0.0, END)
            self.output.config(fg = "red")
            url_refer = "https://developer.mapquest.com/documentation/directions-api/status-codes"
            self.output.insert(END, "For Status Code: " + str(json_status) + ". Refer to: " + url_refer +"\n")
            self.output.insert(END, "Status Code Documentation opening in browser after 2 seconds...")
            time.sleep(2)
            webbrowser.open(url_refer)
        
    def clear(self):
        #clear the entry boxes
        self.startingLocation.set("")
        self.destinationLocation.set("")

        #clear the output
        self.output.delete(0.0, END)

#run application  
MapQuest()



