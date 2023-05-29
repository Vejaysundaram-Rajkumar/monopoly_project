from numerize import numerize
import sqlite3

play=True
playernames=[]

#Connect with the customers database to store the user details
def connect_db():
    connection = sqlite3.connect('gamedetails.db')
    return connection
#delete the game
def deletegame():
    try:
        con=connect_db()
        cursor=con.cursor()
        cursor.execute("SELECT DISTINCT game_name FROM players ")
        n=cursor.fetchall()
        if(n):
            print("------------------------------------------------------------------------------------------------")
            print("SAVED GAMES:")
            for i in n:
                print(i[0])
            print("------------------------------------------------------------------------------------------------")
            name=input("Enter the name of the game you want to delete:")
            cursor.execute('DELETE FROM players WHERE game_name = ?',(name,));        
            con.commit()
            con.close()
            print("------------------------------------------------------------------------------------------------")
            print("You have successfully deleted the game!")
            print("------------------------------------------------------------------------------------------------")
        else:
            print("------------------------------------------------------------------------------------------------")
            print("NO SAVED GAMES !!")  

    except:
        err_message="error deleting the data"
        print("------------------------------------------------------------------------------------------------")
        print(err_message)

#checking if the gamename is already in used or not
def checkgamename(name):
    if(name==''):
        gname=input("Enter a name for the game:")
        con=connect_db()
        cursor=con.cursor()
        cursor.execute("SELECT count(*) FROM players WHERE game_name = ?",(gname,))
        n=cursor.fetchone()
        con.commit()
        con.close()
        print(n)
        if(n[0]>=1):
            gname=''
            print("Game name already in use!!")
            return checkgamename(gname)
        else:
            print("Game Created :)")
            print(gname)
            return gname
    

def newgame():
    print("-------------------------------------------------------------------------------------------------")
    print("-----------------------------------------NEW GAME------------------------------------------------")
    n=int(input("Enter number of players:"))
    money=2000000
    name=''
    gamename=checkgamename(name)
    print(gamename)    
    for i in range(1,n+1):
        print("Enter the name of Player",i,end=' ')
        temp_name=input()
        try:
            con=connect_db()
            cursor=con.cursor()
            cursor.execute("INSERT INTO players (name, current_money,game_name) VALUES (?, ?, ?)", (temp_name,money,gamename))
            con.commit()
            con.close()
        except:
            err_message="error updating the database"
            print("------------------------------------------------------------------------------------------------")
            print(err_message)
    
    
    
    
    print("-------------------------------------------------------------------------------------------------")
    

def continuegame():
    pass


while(play!=False):
    print("------------------------------------------------------------------------------------------------")
    print("---------------------------WELCOME TO GAME MANAGER OF MONOPOLY----------------------------------")
    print("1.NEW GAME\n2.CONTINUE GAME\n3.DELETE SAVED GAME\n4.EXIT")
    ch=int(input("ENTER YOUR CHOICE:"))
    if(ch==1):
        newgame()
    elif(ch==2):
        continuegame()  
    elif(ch==3):
        print("Under construction!!!")
    elif(ch==4):
        exit(0)
    else:
        print("Invalid Choice!..Please try again")