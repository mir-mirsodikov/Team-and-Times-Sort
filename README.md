# Project Name: Times and Teams Sort
## Name: Mukhammad Mirsodikov
## Date: January 23 2020

### Project functionality:
* The user will take a PDF of 'Top Times' from http://www.kshsaa.org/Public/Swimming/Main.cfm
    * This PDF file will then be turned into a text file using an online formatter
* The text file will then be moved to the directory
* The script will run through the text file and get rid of all of the 6A schools leaving 1-5A
* This information will then be written to a seperate text file
* Instead of everything being in a text file, put it all in a Google Sheet using gspread

### Future goals:
* Automate the process of downloading the PDF file and then converting it to a text file
* Allow the user to type in the name of the text file they want to write to
* Put in general meet results and then do:
    * Allow user to type in name of team
    * Have the script read through the file and compile all of the results from that team
    * Keep a log of the top times from that team and update it when a new meet result comes out
