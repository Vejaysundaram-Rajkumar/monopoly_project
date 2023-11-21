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
            #print(gname)
            return gname
    

def newgame():
    def startgame(gname):
        p=True
        while(p!=False):
            print("------------------------------------------------------------------------------------------------")
            print("---------------------------WELCOME TO GAME MANAGER OF",gname,"----------------------------------")
            print(" 1:Pay Rent\n 2:Pay The Government or Bank\n 3: Buy an Property or Utility\n4:Build an House/Hotel \n5:End the Game and give the winner\n")
            ch=int(input("ENTER ACTION TO BE DONE:"))
            if(ch==1):
                payer=int(input("Enter the Player number whom has to pay the rent: "))
                siteno=int(input("Enter the site number of the property:"))
                con=connect_db()
                cursor=con.cursor()
                cursor.execute("SELECT current_rent FROM cities WHERE id = ?",(siteno,))
                n=cursor.fetchone()


                con.commit()
                con.close()
            elif(ch==2):
                pass
            elif(ch==3):
                pass
            elif(ch==4):
                pass
            elif(ch==5):
                pass
            else:
                print("Invalid Choice!..Please try again")
        
    print("-------------------------------------------------------------------------------------------------")
    print("-----------------------------------------NEW GAME------------------------------------------------")
    n=int(input("Enter number of players:"))
    money=2000000
    name=''
    gamename=checkgamename(name)
    #print(gamename)    
    for i in range(1,n+1):
        print("Enter the name of Player",i,end=' ')
        temp_name=input()
        p_no=int(input("Enter an number for this player:"))
        try:
            con=connect_db()
            cursor=con.cursor()
            cursor.execute("INSERT INTO players (id,name, current_money,game_name) VALUES (?, ?, ?, ?)", (p_no,temp_name,money,gamename))
            con.commit()
            con.close()
        except:
            err_message="error updating the database"
            print("------------------------------------------------------------------------------------------------")
            print(err_message)
    startgame(gamename)

def exitgame():
    con=connect_db()
    cursor=con.cursor()
    cursor.execute("DELETE FROM players")
    n=cursor.fetchone()
    con.commit()
    con.close()
    exit()

while(play!=False):
    print("------------------------------------------------------------------------------------------------")
    print("---------------------------WELCOME TO GAME MANAGER OF MONOPOLY----------------------------------")
    print("1.NEW GAME\n2.EXIT")
    ch=int(input("ENTER YOUR CHOICE:"))
    if(ch==1):
        newgame()
    elif(ch==2):
        k=int(input("The Game will be deleted!Are you sure?\n1.Yes\n2.No\n"))
        if(k==1):
            exitgame()  
        else:
            pass
    else:
        print("Invalid Choice!..Please try again")