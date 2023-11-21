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
                #Finding the owner of the property  
                cursor.execute("SELECT Owner FROM cities WHERE id = ?",(siteno,))
                owner=cursor.fetchone()
                if(owner[0]!="bank"):
                    #get the current rent bracket 
                    cursor.execute("SELECT current_rent FROM cities WHERE id = ?",(siteno,))
                    rent_set=cursor.fetchone()
                    
                    #get the rent money in that particular bracket
                    cursor.execute("SELECT {} FROM cities WHERE id = ?".format(rent_set[0]), (siteno,))
                    rent_money=cursor.fetchone()

                    #Get the balance money of the payer whom has to pay the rent
                    cursor.execute("SELECT current_money FROM players WHERE id = ?",(payer,))
                    payer_balance=cursor.fetchone()                
                
                    #getting the balance of the owner of the property
                    cursor.execute("SELECT current_money FROM players WHERE name = ?",(owner[0],))
                    owner_balance=cursor.fetchone()
                    if(rent_money[0]<payer_balance[0]):
                        p_balance=payer_balance[0]-rent_money[0]
                        o_balance=owner_balance[0]+rent_money[0]
                        #updating the payer's balance amount into is database
                        up1 = "UPDATE players SET current_money = ? WHERE id = ?"
                        val2 = (p_balance, payer)
                        cursor.execute(up1, val2)
                        #updating the payer's balance amount into is database
                        up2 = "UPDATE players SET current_money = ? WHERE name = ?"
                        val3 = (o_balance,owner[0])
                        cursor.execute(up2, val3)
                        con.commit()    
                    else:
                        print("Insufficient balance for the player!!")
                    con.close()        
                else:
                    print("This property is not bought by any of the players")

            elif(ch==2):
                pass
            elif(ch==3):
                buyer=int(input("Enter the Player number whom is buying the property: "))
                siteno=int(input("Enter the site number of the property:"))
                con=connect_db()
                cursor=con.cursor()
                #Finding the owner of the property  
                cursor.execute("SELECT Owner FROM cities WHERE id = ?",(siteno,))
                owner=cursor.fetchone()
                if(owner[0]=="bank"):
                    #Get the cost of the property from cities table
                    cursor.execute("SELECT buy_cost FROM cities WHERE id = ?",(siteno,))
                    prop_cost=cursor.fetchone()                

                    #getting the balance of the player
                    cursor.execute("SELECT current_money FROM players WHERE id= ?",(buyer,))
                    b_balance=cursor.fetchone()
                    
                    if(prop_cost[0]<=b_balance[0]):
                        buyer_balance=b_balance[0]-prop_cost[0]
                        #updating the buyer's balance amount into is database
                        up1 = "UPDATE players SET current_money = ? WHERE id = ?"
                        val2 = (buyer_balance, buyer)
                        cursor.execute(up1, val2)
                        #updating the owner of the property into is database
                        cursor.execute("SELECT name FROM players WHERE id = ?",(buyer,))
                        owner_name=cursor.fetchone()
                        up2 = "UPDATE cities SET Owner = ? WHERE id = ?"
                        val3 = (owner_name[0],siteno)
                        cursor.execute(up2, val3)
                        con.commit()
                    else:
                        print("Insufficient balance for the player!!")
                    con.close()
                else: 
                    print("This property is not available and it cannot be bought by you!!!")
                
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

def deletegame():
    con=connect_db()
    cursor=con.cursor()
    cursor.execute("DELETE FROM players")
    up1 = "UPDATE cities SET Owner = 'bank'"
    cursor.execute(up1)
    up2 = "UPDATE cities SET current_rent = 'rent'"
    cursor.execute(up2)
    con.commit()
    print("The Saved game is sucessfully deleted!!")
    con.close()

while(play!=False):
    print("------------------------------------------------------------------------------------------------")
    print("---------------------------WELCOME TO GAME MANAGER OF MONOPOLY----------------------------------")
    print("1.NEW GAME\n2.Deletegame\n3.Exit game")
    ch=int(input("ENTER YOUR CHOICE:"))
    if(ch==1):
        deletegame()
        newgame()
    elif(ch==2):
        k=int(input("The Game will be deleted!Are you sure?\n1.Yes\n2.No\n"))
        if(k==1):
            deletegame()  
        else:
            pass
    elif(ch==3):
        exit()
    else:
        print("Invalid Choice!..Please try again")