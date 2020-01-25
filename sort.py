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

    Future goals:
        * Automate the process of downloading the PDF file and then converting it to a text file
        * Allow the user to type in the name of the text file they want to write to
        * Put in general meet results and then do:
            - Allow user to type in name of team
            - Have the script read through the file and compile all of the results from that team
            - Keep a log of the top times from that team and update it when a new meet result comes out
'''

def check_team(name):
    for team in teamNames6A:
        team = team.strip()
        if name == team:
            return False
        else:
            return True

topTimes = open("TopTimes.txt", "r")
teamNames6A = open("teams.txt", "r")
sortedTimes = open("test.txt", "w")

teamInfo = ""
event = 0

for line in topTimes:
    if "Event" in line:
        sortedTimes.write("----------------------------------------- \n")
        sortedTimes.write(line + "\n")
        event += 1
    else:
        if line[0].isdigit():   
            teamInfo = line.split(" ")
            name = ""
            
            ''' assign the team name to the variable 'name' from the array '''
            if event == 1 or event == 9 or event == 12:
                'events 1, 9, and 4 are relays so their team name is at a differnt position'
                for s in range(1, len(teamInfo) - 1, 1):
                    name += teamInfo[s] + " "
            else:
                'these are the individual events so their team name is different than relays'
                for s in range(3, len(teamInfo) - 1, 1):
                    name += teamInfo[s] + " "
            
            name = name.strip()
            valid_team = check_team(name)
            print(name)
            for a in teamInfo:
                sortedTimes.write(a + " ")


    
    

topTimes.close()
teamNames6A.close()
sortedTimes.close()
