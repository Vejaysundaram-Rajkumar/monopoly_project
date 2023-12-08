from numerize import numerize
import sqlite3
import locale
locale.setlocale(locale.LC_MONETARY, 'en_IN')
play=True
playernames=[]
#Connect with the customers database to store the user details
def connect_db():
    connection = sqlite3.connect('gamedetails.db')
    return connection

#checking if the gamename is already in used or not
#def checkgamename(gname):
    con=connect_db()
    cursor=con.cursor()
    cursor.execute("SELECT count(*) FROM players WHERE game_name = ?",(gname,))
    n=cursor.fetchone()
    con.commit()
    con.close()
    #print(n)
    if(n[0]>=1):
        #print("Game name already in use!!")
        return False
    else:
        #print("Game Created :)")
        #print(gname)
        return True

def utility_rent_check():
    con=connect_db()
    cursor=con.cursor()
    # Identify players with more than 1 utility
    cursor.execute("SELECT p.id, COUNT(u.id) as utility_count FROM players p LEFT JOIN utilities u ON p.name = u.Owner WHERE u.Owner != 'bank' GROUP BY p.id HAVING utility_count > 1")

    # Fetch the player IDs and utility counts
    player_utility_counts = cursor.fetchall()

    # Update current_rent for each player based on the utility count
    for player_info in player_utility_counts:
        player_id, utility_count = player_info
        if utility_count == 2:
            cursor.execute("UPDATE utilities SET current_rent = 'rent_multiplier_2' WHERE Owner = (SELECT name FROM players WHERE id = ?)", (player_id,))
        else:
            cursor.execute("UPDATE utilities SET current_rent = 'rent_multiplier_1' WHERE Owner = (SELECT name FROM players WHERE id = ?)", (player_id,))
        con.commit()

def trains_rent_check():
    con=connect_db()
    cursor=con.cursor()
    # Identify players with more than 1 train station
    cursor.execute("SELECT p.id, COUNT(t.id) as station_count FROM players p LEFT JOIN trains t ON p.name = t.Owner WHERE t.Owner != 'bank' GROUP BY p.id HAVING station_count > 1")

    # Fetch the player IDs and station counts
    player_station_counts = cursor.fetchall()
    #print(player_station_counts)
    # Update current_rate for each player based on the station count
    for player_info in player_station_counts:
        player_id, station_count = player_info
        if station_count == 2:
            cursor.execute("UPDATE trains SET current_rate = 'rent_2T' WHERE Owner = (SELECT name FROM players WHERE id = ?)", (player_id,))
        elif station_count == 3:
            cursor.execute("UPDATE trains SET current_rate = 'rent_3T' WHERE Owner = (SELECT name FROM players WHERE id = ?)", (player_id,))
        elif station_count == 4:
            cursor.execute("UPDATE trains SET current_rate = 'rent_4T' WHERE Owner = (SELECT name FROM players WHERE id = ?)", (player_id,))
        con.commit()

#printing the results of the game 
def result_func():
    con=connect_db()
    cursor=con.cursor()
    # Calculate net worth for each player
    cursor.execute("""
        SELECT
            p.id,
            p.name,
            p.current_money,
            COALESCE(SUM(CASE
                            WHEN c.current_rent = 'rent_H1' THEN house_cost
                            WHEN c.current_rent = 'rent_H2' THEN 2 * house_cost
                            WHEN c.current_rent = 'rent_H3' THEN 3 * house_cost
                            WHEN c.current_rent = 'rent_H4' THEN 4 * house_cost + hotel_cost
                            WHEN c.current_rent = 'rent_Hotel' THEN 4 * house_cost + hotel_cost
                            ELSE 0
                        END), 0) AS houses_and_hotels_cost,
            COALESCE(SUM(CASE WHEN c.Owner != 'bank' THEN c.buy_cost ELSE 0 END), 0) AS sites_cost,
            COALESCE(SUM(CASE WHEN t.Owner != 'bank' THEN t.purchase_price ELSE 0 END), 0) AS trains_cost,
            COALESCE(SUM(CASE WHEN u.Owner != 'bank' THEN u.purchase_price ELSE 0 END), 0) AS utilities_cost
        FROM
            players p
        LEFT JOIN
            cities c ON p.name = c.Owner
        LEFT JOIN
            trains t ON p.name = t.Owner
        LEFT JOIN
            utilities u ON p.name = u.Owner
        GROUP BY
            p.id, p.name, p.current_money
    """)

    # Fetch player information
    player_info = cursor.fetchall()

    # Calculate and print net worth for each player
    net_worths = []
    for player in player_info:
        player_id, player_name, current_money, houses_and_hotels_cost, sites_cost, trains_cost, utilities_cost = player
        net_worth = current_money + houses_and_hotels_cost + sites_cost + trains_cost + utilities_cost
        net_worths.append((player_id, player_name, net_worth))

    # Sort players by net worth
    net_worths.sort(key=lambda x: x[2], reverse=True)

    # Print the leaderboard
    print("Leaderboard:")
    print("Player Rank | Player Name | Net Worth")
    for i, (player_id, player_name, net_worth) in enumerate(net_worths, 1):
        print(f"{i:10} | {player_name:11} | {locale.currency(net_worth, grouping=True)}")

    # Declare the winner and runner
    if len(net_worths) >= 1:
        winner_id, winner_name, winner_net_worth = net_worths[0]
        print(f"\nWinner: Player {winner_name} (ID: {winner_id}) - Net Worth: {locale.currency(winner_net_worth, grouping=True)}")

    if len(net_worths) >= 2:
        runner_id, runner_name, runner_net_worth = net_worths[1]
        print(f"Runner-up: Player {runner_name} (ID: {runner_id}) - Net Worth: {locale.currency(runner_net_worth, grouping=True)}")

#Starting an new game
def startgame(gname):
    p=True
    while(p!=False):
        print("------------------------------------------------------------------------------------------------")
        print("---------------------------WELCOME TO GAME MANAGER OF",gname,"----------------------------------")
        print(" 1:Pay Rent\n 2: Buy an Property or Utility\n3:Build an HOUSE or an HOTEL\n4:Pay FINE TO THE GOVERNMENT OR GET REWARD FROM THE GOVERNMENT\n5:End the Game and give the winner\n")
        ch=int(input("ENTER ACTION TO BE DONE:"))
        if(ch==1):
            p_type=int(input("Enter the type of the Property:\n1.SITE\n2.Utitility\n3.Railways\n"))
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
                        cursor.execute("SELECT current_rent FROM utilities WHERE id = ?",(siteno,))
                        rent_mul=cursor.fetchone()
                        if(rent_mul[0]=="rent_multiplier_1"):
                            m=4000
                        elif(rent_mul[0]=="rent_multiplier_2"):
                            m=10000
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
                    print(owner_balance)
                    if(p_type==2):
                        if(rent_money<payer_balance[0]):
                            print(owner_balance)
                            p_balance=payer_balance[0]-rent_money
                            o_balance=owner_balance[0]+rent_money
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
                    else:        
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
            b_type=int(input("Enter the type of Construction:\n1.House\n2.Hotel\n"))
            con=connect_db()
            cursor=con.cursor()
            cursor=con.cursor()
            buyer=int(input("Enter the player number who wants to build:"))
            siteno=int(input("Enter the id number of the property in which you want to build:"))
            #get the current rent bracket 
            cursor.execute("SELECT current_rent FROM cities WHERE id = ?",(siteno,))
            rent_set=cursor.fetchone()
            #print(rent_set)
            #Finding the owner of the property  
            cursor.execute("SELECT Owner FROM cities WHERE id = ?",(siteno,))
            owner=cursor.fetchone()

            if(owner!="bank"):
                # Finding the owner's id  of the property
                cursor.execute("SELECT name FROM players WHERE id = ?",(buyer,))
                owner_name=cursor.fetchone()
                if(owner==owner_name):
                    #if maximum is reached then returning the message for the builder
                    if(rent_set[0]!="rent_H4" and b_type==1):
                        #getting the next rent bracket  
                        if(rent_set[0]=="rent"):
                            next_rent="rent_H1"
                        elif(rent_set[0]=="rent_H1"):
                            next_rent="rent_H2"
                        elif(rent_set[0]=="rent_H2"):
                                next_rent="rent_H3"
                        elif(rent_set[0]=="rent_H3"):
                            next_rent="rent_H4"

                        #Getting the cost for building an house
                        cursor.execute("SELECT house_cost FROM cities WHERE id = ?",(siteno,))
                        Hbuild_cost=cursor.fetchone()

                        #getting the balance of the player
                        cursor.execute("SELECT current_money FROM players WHERE id= ?",(buyer,))
                        b_balance=cursor.fetchone()

                        if(Hbuild_cost[0]<=b_balance[0]):
                            builder_balance=b_balance[0]-Hbuild_cost[0]
                            #updating the builder's balance amount into is database
                            up1 = "UPDATE players SET current_money = ? WHERE id = ?"
                            val2 = (builder_balance, buyer)
                            cursor.execute(up1, val2)

                            #updating the owner of the property into is database                        
                            up2 = "UPDATE cities SET current_rent = ? WHERE id = ?"
                            val3 = (next_rent,siteno)
                            cursor.execute(up2, val3)
                            con.commit()
                        else:
                            print("Insufficient balance for the player!!")
                            con.close()
                    elif(b_type==2 and rent_set[0]=='rent_H4'):
                        next_rent="rent_Hotel"
                        #Getting the cost for building an house
                        cursor.execute("SELECT house_cost FROM cities WHERE id = ?",(siteno,))
                        Hbuild_cost=cursor.fetchone()
                        #getting the balance of the player
                        cursor.execute("SELECT current_money FROM players WHERE id= ?",(buyer,))
                        b_balance=cursor.fetchone()

                        if(Hbuild_cost[0]<=b_balance[0]):
                            builder_balance=b_balance[0]-Hbuild_cost[0]
                            #updating the builder's balance amount into is database
                            up1 = "UPDATE players SET current_money = ? WHERE id = ?"
                            val2 = (builder_balance, buyer)
                            cursor.execute(up1, val2)

                            #updating the owner of the property into is database                        
                            up2 = "UPDATE cities SET current_rent = ? WHERE id = ?"
                            val3 = (next_rent,siteno)
                            cursor.execute(up2, val3)
                            con.commit()
                        else:
                            print("Insufficient balance for the player!!")
                            con.close()
                    elif(b_type==2 and rent_set[0]!="rent_H4"):
                        print("REQUIRED AMOUNT OF HOUSES IS NOT BUILT YET IN THIS PROPERTY!!")
                    elif(b_type==2 and rent_set[0]=="rent_Hotel"):
                        print("NO MORE HOTEL CAN BE BUILT IN THIS PROPERTY!!")
                    else:
                        print("NO MORE HOUSES CAN BE BUILT IN THIS PROPERTY!!")
                else:
                    print("The owner of the property and the builder mismatched!!")
            else:
                print("The property is not yet bought from the bank yet by any players!!")

        elif(ch==4):
            con=connect_db()
            cursor=con.cursor()
            payto=int(input("Choose the correct option\n1.Pay the Government\n2.Government pays you"))
            if(payto==1):
                amount=int(input("Enter the Fine or loss amount occured:"))
                payer=int(input("Enter the player number who has to pay:"))
                #getting the balance of the player
                cursor.execute("SELECT current_money FROM players WHERE id= ?",(payer,))
                b_balance=cursor.fetchone()
                if(amount<=b_balance[0]):
                    payer_bal=b_balance[0]-amount
                    #updating the builder's balance amount into is database
                    up1 = "UPDATE players SET current_money = ? WHERE id = ?"
                    val2 = (payer_bal, payer)
                    cursor.execute(up1, val2)
                    con.commit()
                else:
                    print("INSUFFICIENT BALANCE FOR THE PLAYER!!!")
            elif(payto==2):
                amount=int(input("Enter the Reward amount occured:"))
                payer=int(input("Enter the player number who has gets the Reward amount:"))
                #getting the balance of the player
                cursor.execute("SELECT current_money FROM players WHERE id= ?",(payer,))
                b_balance=cursor.fetchone()
                payer_bal=b_balance[0]+amount
                #updating the builder's balance amount into is database
                up1 = "UPDATE players SET current_money = ? WHERE id = ?"
                val2 = (payer_bal, payer)
                cursor.execute(up1, val2)
                con.commit()
            else:
                print("Enter an valid choice!!")
        elif(ch==5):
            result_func()
            con=connect_db()
            cursor=con.cursor()
            id_no=1
            value=1
            up1 = "UPDATE game SET endgame = ? WHERE id = ?"
            val2 = (value,id_no)
            cursor.execute(up1, val2)
            con.commit()
            con.close()
            exit()
        else:
            print("Invalid Choice!..Please try again")
#checking if the game is there or not
def checkgamename(name):
    con=connect_db()
    cursor=con.cursor()
    cursor.execute("SELECT count(*) FROM players WHERE game_name = ?",(name,))
    n=cursor.fetchone()
    con.commit()
    con.close()
    print(n)
    if(n[0]>=1):
        return True
    else:
        return False
#creating an new game 
def newgame(n,players,gamename):  
    money=9000000
    c=checkgamename(gamename)
    if(c==True):
        return True
    else:    
        for i in range(n):
            temp_name=players[i]
            p_no=i+1
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
                return False
    return True


def building_func(playername,p_type,prop_name):
    con=connect_db()
    cursor=con.cursor()
    up1 = "SELECT Owner FROM {} WHERE name = ?".format(p_type)
    val1 = (prop_name,)
    cursor.execute(up1, val1)
    owner = cursor.fetchone()

    if(owner[0]=="bank"):
        #getting the cost of the property    
        up2 = "SELECT purchase_price FROM {} WHERE name = ?".format(p_type)
        val2 = (prop_name,)
        cursor.execute(up2, val2)
        prop_cost = cursor.fetchone()
       
        #getting the balance of the player
        cursor.execute("SELECT current_money FROM players WHERE name= ?",(playername,))
        b_balance=cursor.fetchone()
        
        if(prop_cost[0]<=b_balance[0]):
            buyer_balance=b_balance[0]-prop_cost[0]
            #updating the buyer's balance amount into is database
            up3 = "UPDATE players SET current_money = ? WHERE name = ?"
            val3 = (buyer_balance, playername)
            cursor.execute(up3, val3)

            #updating the owner to the player name for that property
            up4 = "UPDATE {} SET Owner = ? WHERE name = ?".format(p_type)
            val4 = (playername, prop_name)
            cursor.execute(up4, val4)
            con.commit()

            if(p_type=="utilities"):
                utility_rent_check()
            elif(p_type=="trains"):
                trains_rent_check()
            else:
                pass
        else:
            b=-1
            con.close()
            return b
        b=1
        con.close()
        return b
    else:
        b=0
        con.close()
        return b



#Deleting the created game.
def deletegame():
    con=connect_db()
    cursor=con.cursor()
    cursor.execute("DELETE FROM players")
    up1 = "UPDATE cities SET Owner = 'bank'"
    cursor.execute(up1)
    
    up2 = "UPDATE utilities SET Owner = 'bank'"
    cursor.execute(up2)
    
    up3 = "UPDATE trains SET Owner = 'bank'"
    cursor.execute(up3)

    up4 = "UPDATE trains SET current_rate = 'rent_1T'"
    cursor.execute(up4)
    
    up5 = "UPDATE cities SET current_rent = 'rent'"
    cursor.execute(up5)
    
    up6 = "UPDATE utilities SET current_rent = 'rent_multiplier_1'"
    cursor.execute(up6)

    up7 = "UPDATE game SET endgame = 0"
    cursor.execute(up7)
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
