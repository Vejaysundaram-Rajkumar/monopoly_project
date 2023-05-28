from numerize import numerize
import sqlite3

play=True
playernames=[]

#Connect with the customers database to store the user details
def connect_db():
    connection = sqlite3.connect('gamedetails.db')
    return connection

def newgame():
    print("-------------------------------------------------------------------------------------------------")
    print("-----------------------------------------NEW GAME------------------------------------------------")
    n=int(input("Enter number of players:"))
    for i in range(1,n+1):
        print("Enter the name of Player",i,end='')
        temp_name=input()
        playernames.append(temp_name)
        print("\n")
    print(playernames)
    
    
    
    
    print("-------------------------------------------------------------------------------------------------")
    





while(play!=False):
    print("------------------------------------------------------------------------------------------------")
    print("------------------------------------------------------------------------------------------------")
    print("---------------------------WELCOME TO GAME MANAGER OF MONOPOLY----------------------------------")
    print("1.NEW GAME\n2.ABOUT\n3.HOW TO MANAGE\n4.EXIT")
    ch=int(input("ENTER YOUR CHOICE:"))
    if(ch==1):
        newgame()