from numerize import numerize
import sqlite3

play=True
playernames=[]

#Connect with the customers database to store the user details
def connect_db():
    connection = sqlite3.connect('gamedetails.db')
    return connection

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

#Starting an new game
def startgame(gname):
    p=True
    while(p!=False):
        print("------------------------------------------------------------------------------------------------")
        print("---------------------------WELCOME TO GAME MANAGER OF",gname,"----------------------------------")
        print(" 1:Pay Propertity Rent\n 2:Pay Utility Rent\n 3: Buy an Property or Utility\n4:Build an House/Hotel \n5:End the Game and give the winner\n")
        ch=int(input("ENTER ACTION TO BE DONE:"))
        if(ch==1):
            p_type=int(input("Enter the type of the Property:\n1.SITE\2.Utitility\n3.Railways\n"))
            if(p_type>=1 and p_type<=3):
                payer=int(input("Enter the player number whom has to pay the rent: "))
                siteno=int(input("Enter the id number of the property:"))
                con=connect_db()
                cursor=con.cursor()
                if(p_type==1):
                    #Finding the owner of the property  
                    cursor.execute("SELECT Owner FROM cities WHERE id = ?",(siteno,))
                    owner=cursor.fetchone()
                elif(p_type==2):
                    #Finding the owner of the property  
                    cursor.execute("SELECT Owner FROM utilities WHERE id = ?",(siteno,))
                    owner=cursor.fetchone()
                elif(p_type==3):
                    #Finding the owner of the property  
                    cursor.execute("SELECT Owner FROM trains WHERE id = ?",(siteno,))
                    owner=cursor.fetchone()
                if(owner[0]!="bank"):
                    if(p_type==1):
                        #get the current rent bracket 
                        cursor.execute("SELECT current_rent FROM cities WHERE id = ?",(siteno,))
                        rent_set=cursor.fetchone()
                    
                        #get the rent money in that particular bracket
                        cursor.execute("SELECT {} FROM cities WHERE id = ?".format(rent_set[0]), (siteno,))
                        rent_money=cursor.fetchone()

                    elif(p_type==2):
                        diceroll=int(input("Enter the number displayed on your dice: "))
                        #current multiplyer bracket is found here from the database
                        cursor.execute("SELECT current_rate FROM utilities WHERE id = ?",(siteno,))
                        owner=cursor.fetchone()
                        if(owner[0]=="rent_multiplier_1"):
                            m=4
                        elif(owner[0]=="rent_multiplier_2"):
                            m=10
                        rent_money=m*diceroll

                    elif(p_type==3):
                        #get the current rent bracket 
                        cursor.execute("SELECT current_rate FROM trains WHERE id = ?",(siteno,))
                        rent_set=cursor.fetchone()
                    
                        #get the rent money in that particular bracket
                        cursor.execute("SELECT {} FROM trains WHERE id = ?".format(rent_set[0]), (siteno,))
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

            else:
                print("Invalid choice!!.")
        elif(ch==2):
           pass
        elif(ch==3):
            p_type=int(input("Enter the type of the Property:\n1.SITE\2.Utitility\n3.Railways\n"))
            if(p_type>=1 and p_type<=3):
                buyer=int(input("Enter the player number who wants to buy: "))
                siteno=int(input("Enter the id number of the property:"))
                con=connect_db()
                cursor=con.cursor()
                if(p_type==1):
                    #Finding the owner of the property  
                    cursor.execute("SELECT Owner FROM cities WHERE id = ?",(siteno,))
                    owner=cursor.fetchone()
                elif(p_type==2):
                    #Finding the owner of the property  
                    cursor.execute("SELECT Owner FROM utilities WHERE id = ?",(siteno,))
                    owner=cursor.fetchone()
                elif(p_type==3):
                    #Finding the owner of the property  
                    cursor.execute("SELECT Owner FROM trains WHERE id = ?",(siteno,))
                    owner=cursor.fetchone()
                if(owner[0]=="bank"):
                    if(p_type==1):
                        #Get the cost of the property from cities table
                        cursor.execute("SELECT buy_cost FROM cities WHERE id = ?",(siteno,))
                        prop_cost=cursor.fetchone()
                    elif(p_type==2):
                        #Get the cost of the property from utilities table
                        cursor.execute("SELECT purchase_price FROM utilities WHERE id = ?",(siteno,))
                        prop_cost=cursor.fetchone()

                    elif(p_type==3):
                        #Get the cost of the property from trains table
                        cursor.execute("SELECT purchase_price FROM trains WHERE id = ?",(siteno,))
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
                        if(p_type==1):
                            up2 = "UPDATE cities SET Owner = ? WHERE id = ?"
                            val3 = (owner_name[0],siteno)
                            cursor.execute(up2, val3)
                            con.commit()
                        elif(p_type==2):
                            up2 = "UPDATE utilities SET Owner = ? WHERE id = ?"
                            val3 = (owner_name[0],siteno)
                            cursor.execute(up2, val3)
                            con.commit()
                        elif(p_type==3):
                            up2 = "UPDATE trains SET Owner = ? WHERE id = ?"
                            val3 = (owner_name[0],siteno)
                            cursor.execute(up2, val3)
                            con.commit()            
                    else:
                        print("Insufficient balance for the player!!")
                    con.close()
                else:
                    print("This property is not available and it cannot be bought by you!!!")
            else: 
                print("INVALID CHOICE!!")
            
        elif(ch==4):
            pass
        elif(ch==5):
            pass
        else:
            print("Invalid Choice!..Please try again")



#creating an new game 
def newgame():  
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
#Deleting the created game.
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


#continue an saved game
def continue_game():
    con=connect_db()
    cursor=con.cursor()
    cursor.execute("SELECT DISTINCT game_name FROM players")
    names=cursor.fetchone()
    if(names==None):
        print("NO SAVED GAMES EXIST!!. Create an new game:)")
    else:
        print("THE SAVED GAME NAME IS ",names[0],"\n DO YOU WANT TO CONTINUE THIS GAME OR CREATE A NEW GAME?\n1.CONTINUE GAME\n2.NEW GAME :")
        con=int(input())
        if(con==1):
            startgame(names[0])
        else:
            deletegame()
            newgame()

#starting of the code
while(play!=False):
    print("------------------------------------------------------------------------------------------------")
    print("---------------------------WELCOME TO GAME MANAGER OF MONOPOLY----------------------------------")
    print("1.NEW GAME\n2.Continue Game\n3.Exit game")
    ch=int(input("ENTER YOUR CHOICE:"))
    if(ch==1):
        deletegame()
        newgame()
    elif(ch==2):
        continue_game()
    elif(ch==3):
        exit()
    else:
        print("Invalid Choice!..Please try again")