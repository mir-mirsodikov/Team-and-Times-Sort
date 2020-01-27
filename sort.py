'''
    Project Name: Times and Teams Sort
    Name: Mukhammad Mirsodikov
    Date: January 23 2020

    Project functionality:
        * The user will take a PDF of 'Top Times' from http://www.kshsaa.org/Public/Swimming/Main.cfm
            - This PDF file will then be turned into a text file using an online formatter
        * The text file will then be moved to the directory
        * The script will run through the text file and get rid of all of the 6A schools leaving 1-5A
        * This information will then be written to a seperate text file
        * Instead of everything being in a text file, put it all in a Google Sheet using gspread

    Future goals:
        * Automate the process of downloading the PDF file and then converting it to a text file
        * Allow the user to type in the name of the text file they want to write to
        * Put in general meet results and then do:
            - Allow user to type in name of team
            - Have the script read through the file and compile all of the results from that team
            - Keep a log of the top times from that team and update it when a new meet result comes out
'''

import gspread
import time
from oauth2client.service_account import ServiceAccountCredentials

#Set up the GSpread information
scope = ["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/spreadsheets","https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
client = gspread.authorize(creds)
file = client.open("1-5A State Top Times")
worksheet = file.sheet1

event_names = ["200 Yard Medley Relay", "200 Yard Individual Medley", "200 Yard Freestyle", "50 Yard Freestyle", "Dive", "100 Yard Fly", "100 Yard Freestyle", "500 Yard Freestyle", "200 Yard Freestyle Relay",
"100 Yard Backstroke", "100 Yard Breaststroke", "400 Yard Freestyle Relay"]

# Create new sheets with the given names from the array 'event_names'
#for e in event_names:
#    worksheet = file.add_worksheet(title=e, rows="20", cols="8")

topTimes = open("TopTimes.txt", "r") # open the text file 'TopTimes' to read
teamNames6A = open("teams.txt", "r") # open the text file 'teams' to read
sortedTimes = open("SortedTimes.txt", "w") # open the text file 'SortedTimes' to write in -- this is where the results will be written

team_array = teamNames6A.read()       # Read all of the contents from the text file and put in the variable
team_array = team_array.split("\n")   # Split all the variable into an array at every new line

teamInfo = ""
event = 0
position = 1

for line in topTimes: # Loop through the 'TopTimes' file 
    if "Event" in line: # This is split of events
        event += 1 #event counter
        worksheet = file.get_worksheet(event) # switch between worksheets based on the event number
        if event == 5: # event 5 is diving so skip over it since I do not need it
            continue
        else:
            sortedTimes.write("----------------------------------------- \n") # seperator between each and every event
            sortedTimes.write(line + "\n") # the line is the event name and number
        position = 1 # this is the overall placement of each athleter/team
    elif event == 5: # skip over diving 
        continue
    else:
        if line[0].isdigit(): # take the line that starts with a number --- lines with a number are the lines I need
            teamInfo = line.split(" ") # split the line into an array 
            team_name = "" # add the team name
            athlete_name = "" # add the athlete name
            new_team_info = [] # new array to sort the information the way i need

            # assign the team team_name to the variable 'name' from the array
            if event == 1 or event == 9 or event == 12:
                #events 1, 9, and 4 are relays so their team name is at a differnt position
                #Format: Postion Team_Name Time
                for s in range(1, len(teamInfo) - 1, 1):
                    team_name += teamInfo[s] + " "
                new_team_info = [teamInfo[0], team_name, teamInfo[-1]] # set up the array
            else:
                #these are the individual events so their team name is different than relays
                #Format: Positon First_Name Last_Name Team_Name Time
                for s in range(3, len(teamInfo) - 1, 1):
                    team_name += teamInfo[s] + " "
                athlete_name += teamInfo[1] + " " + teamInfo[2] # the athlete name
                new_team_info = [teamInfo[0], athlete_name, team_name, teamInfo[-1]] # set up the array

            team_name = team_name.strip() # get rid of all of the spaces from the team name

            if team_name not in team_array: # if the team name is NOT in the array of 6A teams then use it
                teamInfo[0] = str(position) + "." # the first index is the position
                new_team_info[0] = teamInfo[0] # format the new array with the position

                for s in range(0, len(teamInfo), 1):
                    if s != len(teamInfo) - 1:
                        sortedTimes.write(teamInfo[s] + " ")
                    else:
                        sortedTimes.write(teamInfo[s])

                for i in range(0, len(new_team_info), 1): # add the info into the cells
                    worksheet.update_cell(position, i + 1, new_team_info[i])

                time.sleep(5) # the Google Sheets API can only take information ata certain speed
                position += 1 # increase the position by 1

# close all of the files
topTimes.close()
teamNames6A.close()
sortedTimes.close()