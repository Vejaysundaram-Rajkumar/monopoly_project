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

def transaction_func(t_type,player_name,amount,pr_type,propt_name,dice_roll):
    con=connect_db()
    cursor=con.cursor()
    cursor.execute("SELECT counter FROM game")
    num=cursor.fetchone()
    no=int(num[0])+1
    cursor.execute(" INSERT INTO transactions (id, transaction_type, player_name,amount,property_type,specific_property,dice_roll) VALUES (?,?,?,?,?,?,?)",(no,t_type,player_name,locale.currency(amount, grouping=True),pr_type,propt_name,dice_roll))
    upc = "UPDATE game SET counter = ? "
    val = (no,)
    cursor.execute(upc, val)
    con.commit()
    con.close()

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
            cursor.execute("UPDATE trains SET current_rent = 'rent_2T' WHERE Owner = (SELECT name FROM players WHERE id = ?)", (player_id,))
        elif station_count == 3:
            cursor.execute("UPDATE trains SET current_rent = 'rent_3T' WHERE Owner = (SELECT name FROM players WHERE id = ?)", (player_id,))
        elif station_count == 4:
            cursor.execute("UPDATE trains SET current_rent = 'rent_4T' WHERE Owner = (SELECT name FROM players WHERE id = ?)", (player_id,))
        con.commit()

#updating the money into its brackt of the players for each transactions    
def money_update(ttype,player,amtt):
    print(amtt)
    con=connect_db()
    cursor=con.cursor()
    #getting the other gained value from the database
    cursor.execute("SELECT {} FROM players WHERE name = ?".format(ttype), (player,))
    money_bal=cursor.fetchone()
    print(money_bal[0])
    new_money=money_bal[0]+amtt
    #updating the builder's balance amount into is database
    up1 = "UPDATE players SET {} = ? WHERE name = ?".format(ttype)
    val2 = (new_money, player)
    cursor.execute(up1, val2)
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
                            WHEN c.current_rent = 'rent_H4' THEN 4 * house_cost 
                            WHEN c.current_rent = 'rent_Hotel' THEN 4 * house_cost + hotel_cost
                            ELSE 0
                        END), 0) AS houses_and_hotels_cost,
            COALESCE(SUM(CASE WHEN c.Owner != 'bank' THEN c.purchase_price ELSE 0 END), 0) AS sites_cost,
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
    net_worths.sort(key=lambda x: x[2],reverse=True)
    print(net_worths)
    return net_worths

def buy_house_hotel_func(buyer,b_type,prop_name):
    if(prop_name==""):
        b=-4
        return b
    #function la b_type is used as int ..aana b_type string aa varum paathuko da
    #same for buyer too
    #siteno --> prop_name
    con=connect_db()
    cursor=con.cursor()
    cursor=con.cursor()
    #get the current rent bracket 
    cursor.execute("SELECT current_rent FROM cities WHERE name = ?",(prop_name,))
    rent_set=cursor.fetchone()
    #print(rent_set)
    #Finding the owner of the property  
    cursor.execute("SELECT Owner FROM cities WHERE name = ?",(prop_name,))
    owner=cursor.fetchone()

    if(owner[0]!="bank"):
        # Checking if the player is the owner of the property that he/she tries to build house or hotel
        if(owner[0]==buyer):
            if(rent_set[0]=="rent_Hotel"):
                b=9
                return b
            else: 
                #if maximum is reached then returning the message for the builder
                if(rent_set[0]!="rent_H4" and b_type=='house'):
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
                    cursor.execute("SELECT house_cost FROM cities WHERE name = ?",(prop_name,))
                    Hbuild_cost=cursor.fetchone()

                    #getting the balance of the player
                    cursor.execute("SELECT current_money FROM players WHERE name= ?",(buyer,))
                    b_balance=cursor.fetchone()

                    if(Hbuild_cost[0]<=b_balance[0]):
                        builder_balance=b_balance[0]-Hbuild_cost[0]
                        #updating the builder's balance amount into is database
                        up1 = "UPDATE players SET current_money = ? WHERE name = ?"
                        val2 = (builder_balance, buyer)
                        cursor.execute(up1, val2)

                        #updating the owner of the property into is database                        
                        up2 = "UPDATE cities SET current_rent = ? WHERE name = ?"
                        val3 = (next_rent,prop_name)
                        cursor.execute(up2, val3)
                        con.commit()
                        b=1
                        money_update("spent_construction",buyer,Hbuild_cost[0])
                        transaction_func("built house",buyer,Hbuild_cost[0],"site",prop_name,0)
                        return b
                    else:
                        b=-1
                        con.close()
                        return b
                elif(b_type=='hotel' and rent_set[0]=='rent_H4'):
                    next_rent="rent_Hotel"
                    #Getting the cost for building an house
                    cursor.execute("SELECT hotel_cost FROM cities WHERE name = ?",(prop_name,))
                    Hbuild_cost=cursor.fetchone()
                    #getting the balance of the player
                    cursor.execute("SELECT current_money FROM players WHERE name= ?",(buyer,))
                    b_balance=cursor.fetchone()

                    if(Hbuild_cost[0]<=b_balance[0]):
                        builder_balance=b_balance[0]-Hbuild_cost[0]
                        #updating the builder's balance amount into is database
                        up1 = "UPDATE players SET current_money = ? WHERE name = ?"
                        val2 = (builder_balance, buyer)
                        cursor.execute(up1, val2)

                        #updating the owner of the property into is database                        
                        up2 = "UPDATE cities SET current_rent = ? WHERE name = ?"
                        val3 = (next_rent,prop_name)
                        cursor.execute(up2, val3)
                        con.commit()
                        b=1
                        money_update("spent_construction",buyer,Hbuild_cost[0])
                        transaction_func("built hotel",buyer,Hbuild_cost[0],"site",prop_name,0)
                        return b
                    else:
                        print("Insufficient balance for the player!!")
                        con.close()
                        b=-1
                        return b
                elif(b_type=='hotel' and rent_set[0]!="rent_H4"):
                    print("REQUIRED AMOUNT OF HOUSES IS NOT BUILT YET IN THIS PROPERTY!!")
                    b=-2
                    return b
                elif(b_type=='hotel' and rent_set[0]=="rent_Hotel"):
                    print("NO MORE HOTEL CAN BE BUILT IN THIS PROPERTY!!")
                    b=5
                    return b
                else:
                    print("NO MORE HOUSES CAN BE BUILT IN THIS PROPERTY!!")
                    b=4
                    return b
        else:
            print("The owner of the property and the builder mismatched!!")
            b=0
            return b
    else:
        b=-3
        print("The property is not yet bought from the bank yet by any players!!")
        return b
#Starting an new game
def startgame(gname):
    p=True
    while(p!=False):
        print("------------------------------------------------------------------------------------------------")
        print("---------------------------WELCOME TO GAME MANAGER OF",gname,"----------------------------------")
        print(" 1:Pay Rent\n 2: Buy an Property or Utility\n3:Build an HOUSE or an HOTEL\n4:Pay FINE TO THE GOVERNMENT OR GET REWARD FROM THE GOVERNMENT\n5:End the Game and give the winner\n")
        ch=int(input("ENTER ACTION TO BE DONE:"))
        if(ch==3):
            pass

        elif(ch==5):
            pass
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
    if(prop_name==""):
        b=-2
        return b
    con=connect_db()
    cursor=con.cursor()
    u1 = "SELECT Owner FROM {} WHERE name = ?".format(p_type)
    va1 = (prop_name,)
    cursor.execute(u1, va1)
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
            money_update("spent_property",playername,prop_cost[0])
            transaction_func("buy",playername,prop_cost[0],p_type,prop_name,0)
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

def payingrent_func(payer,p_type,prop_name,diceno):
    if(prop_name==""):
        b=-3
        return b
    if(diceno==""):
        diceno='0'
        diceno=int(diceno)
    else:
        diceno=int(diceno)
    con=connect_db()
    cursor=con.cursor()
    up1 = "SELECT Owner FROM {} WHERE name = ?".format(p_type)
    val1 = (prop_name,)
    cursor.execute(up1, val1)
    owner = cursor.fetchone()
    print(owner)
    if(owner[0]!="bank"):
        if(owner[0]==payer):
            b=-2
            return b
        else:            
            #get the current rent bracket 
            up2 = "SELECT current_rent FROM {} WHERE name = ?".format(p_type)
            val2 = (prop_name,)
            cursor.execute(up2, val2)
            rent_set=cursor.fetchone()    
            #get the rent money in that particular bracket
            up2 = "SELECT {} FROM {} WHERE name = ?".format(rent_set[0],p_type)
            val2 = (prop_name,)
            cursor.execute(up2, val2)
            rent_money=cursor.fetchone()
                    
            if(p_type=="utilities" and diceno!=0):
                util_rent=rent_money[0]*diceno
                print("rent",util_rent)
            else:
                pass
            #Get the balance money of the payer whom has to pay the rent
            cursor.execute("SELECT current_money FROM players WHERE name = ?",(payer,))
            payer_balance=cursor.fetchone()                
            
            #getting the balance of the owner of the property
            cursor.execute("SELECT current_money FROM players WHERE name = ?",(owner[0],))
            owner_balance=cursor.fetchone()
            print(owner_balance)
            if(p_type=="utilities"):
                if(util_rent<payer_balance[0]):
                    print(owner_balance)
                    p_balance=payer_balance[0]-util_rent
                    o_balance=owner_balance[0]+util_rent
                    #updating the payer's balance amount into is database
                    up1 = "UPDATE players SET current_money = ? WHERE name = ?"
                    val2 = (p_balance, payer)
                    cursor.execute(up1, val2)
                    #updating the owner's balance amount into is database
                    up2 = "UPDATE players SET current_money = ? WHERE name = ?"
                    val3 = (o_balance,owner[0])
                    cursor.execute(up2, val3)
                    con.commit()    
                    money_update("spent_rent",payer,util_rent)
                    money_update("gained_rent",owner[0],util_rent)
                    transaction_func("pay_rent",payer,util_rent,p_type,prop_name,diceno)
                else:
                    b=-1
                    return b
            else:        
                if(rent_money[0]<payer_balance[0]):
                    p_balance=payer_balance[0]-rent_money[0]
                    o_balance=owner_balance[0]+rent_money[0]
                    #updating the payer's balance amount into is database
                    up1 = "UPDATE players SET current_money = ? WHERE name = ?"
                    val2 = (p_balance, payer)
                    cursor.execute(up1, val2)
                    #updating the payer's balance amount into is database
                    up2 = "UPDATE players SET current_money = ? WHERE name = ?"
                    val3 = (o_balance,owner[0])
                    cursor.execute(up2, val3)
                    con.commit()
                    money_update("spent_rent",payer,rent_money[0])
                    money_update("gained_rent",owner[0],rent_money[0])
                    transaction_func("pay_rent",payer,rent_money[0],p_type,prop_name,diceno)    
                else:
                    b=-1
                    return b
            b=1
            con.close()
            return b        
    else:
        b=0
        return b

def pay_bank_func(payer,amount):
    if(amount==""):
        amount=0
    else:
        amount=int(amount)
    con=connect_db()
    cursor=con.cursor()
    #getting the balance of the player
    cursor.execute("SELECT current_money FROM players WHERE name= ?",(payer,))
    b_balance=cursor.fetchone()
    if(amount<=b_balance[0]):
        payer_bal=b_balance[0]-amount
        #updating the builder's balance amount into is database
        up1 = "UPDATE players SET current_money = ? WHERE name = ?"
        val2 = (payer_bal, payer)
        cursor.execute(up1, val2)
        con.commit()
        money_update("other_spendings",payer,amount)
        transaction_func("pay_bank",payer,amount,"","",0)
        b=1
        return b
    else:
        b=-1
        return b
    
def reward_bank_func(player, amount):
    if(amount==""):
        amount=0
    else:
        amount=int(amount)
    con=connect_db()
    cursor=con.cursor()
    #getting the balance of the player
    cursor.execute("SELECT current_money FROM players WHERE name= ?",(player,))
    b_balance=cursor.fetchone()
    payer_bal=b_balance[0]+amount
    #updating the builder's balance amount into is database
    up1 = "UPDATE players SET current_money = ? WHERE name = ?"
    val2 = (payer_bal, player)
    cursor.execute(up1, val2)
    con.commit()
    money_update("other_gains",player,amount)
    transaction_func("reward",player,amount,"","",0)
    b=1
    return b



def collect_salary_func(player):
    con=connect_db()
    cursor=con.cursor()
    amount=2000000
    #getting the balance of the player
    cursor.execute("SELECT current_money FROM players WHERE name= ?",(player,))
    b_balance=cursor.fetchone()
    payer_bal=b_balance[0]+amount
    #updating the builder's balance amount into is database
    up1 = "UPDATE players SET current_money = ? WHERE name = ?"
    val2 = (payer_bal, player)
    cursor.execute(up1, val2)
    con.commit()
    money_update("gained_salary",player,amount)
    transaction_func("salary",player,amount,"","",0)
    b=1
    return b


def no_of_buildings(player_name):
    con=connect_db()
    cursor=con.cursor()
    cursor.execute("""
    SELECT COALESCE(SUM(CASE
    WHEN c.current_rent = 'rent_H1' THEN 1
    WHEN c.current_rent = 'rent_H2' THEN 2 
    WHEN c.current_rent = 'rent_H3' THEN 3 
    WHEN c.current_rent = 'rent_H4' THEN 4 
    WHEN c.current_rent = 'rent_Hotel' THEN 4 
    ELSE 0
    END), 0) AS houses_total
    FROM
    cities c
    WHERE
    c.owner = ?
    """, (player_name,))
    houses=cursor.fetchone()
    cursor.execute("""
    SELECT COALESCE(SUM(CASE
    WHEN c.current_rent = 'rent_Hotel' THEN 1 
    ELSE 0
    END), 0) AS hotel_total
    FROM
    cities c
    WHERE
    c.owner = ?
    """, (player_name,))
    hotels=cursor.fetchone()
    count=[houses[0],hotels[0]]
    return count

def statement_func(id):
    con=connect_db()
    cursor=con.cursor()
    cursor.execute('SELECT Statement FROM cards WHERE Id = ?', (id,))
    result = cursor.fetchone()
    con.close()
    return result[0]

def chance_func(player_name,id):
    ans=[]
    if(id<=14):
        if(id>=9 and id<=13):
            if(id==12):
                args=no_of_buildings(player_name)
                house_cost=args[0]*250000
                hotel_cost=args[1]*100000
                total_cost=house_cost+hotel_cost
                print(total_cost)
                r=pay_bank_func(player_name,total_cost)
                if(r==1):
                    ans.append(1)
                    res=statement_func(id)
                    ans.append(res)
                    transaction_func("chance",player_name,0,"",res,0)
                    return ans
                else:
                    ans.append(0)
                    ans.append(0) 
                    return ans
            else:
                con=connect_db()
                cursor=con.cursor()
                cursor.execute('SELECT Amount FROM cards WHERE Id = ?', (id,))
                amt=cursor.fetchone()
                r=reward_bank_func(player_name,amt[0])
                if(r==1):
                    ans.append(1)
                    res=statement_func(id)
                    ans.append(res)
                    transaction_func("chance",player_name,0,"",res,0)
                    return ans
                else:
                    ans.append(0)
                    ans.append(0) 
                    return ans
        elif(id==14):
            con=connect_db()
            cursor=con.cursor()
            cursor.execute('SELECT Amount FROM cards WHERE Id = ?', (id,))
            amt=cursor.fetchone()
            r=pay_bank_func(player_name,amt[0])
            if(r==1):
                ans.append(1)
                res=statement_func(id)
                ans.append(res)
                transaction_func("chance",player_name,0,"",res,0)
                return ans
            else:
                ans.append(0)
                ans.append(0) 
                return ans
    else:
        res=statement_func(id)
        transaction_func("chance",player_name,0,"",res,0)
        ans.append(1)
        ans.append(res)
        return ans
    

def community_chest_func(player_name,id):
    ans=[]
    if(id<=8):
        con=connect_db()
        cursor=con.cursor()
        cursor.execute('SELECT Amount FROM cards WHERE Id = ?', (id,))
        amt=cursor.fetchone()
        r=reward_bank_func(player_name,amt[0])
        if(r==1):
            ans.append(1)
            res=statement_func(id)
            ans.append(res)
            transaction_func("communitychest",player_name,0,"",res,0)
            return ans
        else:
            ans.append(0)
            ans.append(0) 
            return ans

    elif(id==15):
        args=no_of_buildings(player_name)
        house_cost=args[0]*140000
        hotel_cost=args[1]*215000
        total_cost=house_cost+hotel_cost
        print(total_cost)
        r=pay_bank_func(player_name,total_cost)
        if(r==1):
            ans.append(1)
            res=statement_func(id)
            ans.append(res)
            transaction_func("communitychest",player_name,0,"",res,0)
            return ans
        else:
            ans.append(0)
            ans.append(0) 
            return ans

    elif(id>=16 and id<=20):
        con=connect_db()
        cursor=con.cursor()
        cursor.execute('SELECT Amount FROM cards WHERE Id = ?', (id,))
        amt=cursor.fetchone()
        r=pay_bank_func(player_name,amt[0])
        if(r==1):
            ans.append(1)
            res=statement_func(id)
            ans.append(res)
            transaction_func("communitychest",player_name,0,"",res,0)
            return ans
        else:
            ans.append(0)
            ans.append(0) 
            return ans
    else:
        res=statement_func(id)
        transaction_func("communitychest",player_name,0,"",res,0)
        ans.append(1)
        ans.append(res)
        return ans
    

def get_players_data():
    con=connect_db()
    cursor=con.cursor()
    cursor.execute("SELECT id,name,spent_property,spent_construction,spent_rent,other_spendings,gained_rent,other_gains,gained_salary FROM players")
    data=cursor.fetchall()
    players_data=[]
    for i in data:
        player_data = {
            'id': i[0],
            'name': i[1],
            'spent_properties': i[2],
            'spent_construction': i[3],
            'spent_rent': i[4],
            'other_spendings': i[5],
            'gained_rent': i[6],
            'other_gains': i[7],
            'gained_salary': i[8]
        }
        players_data.append(player_data)
    return players_data

#Deleting the created game.
def deletegame():
    con=connect_db()
    cursor=con.cursor()
    cursor.execute("SELECT DISTINCT game_name FROM players")
    gname=cursor.fetchone()
    print(gname)
    if(gname==None):
        return None
    else:
        cursor.execute("DELETE FROM players")
        cursor.execute("DELETE FROM transactions")
        up1 = "UPDATE cities SET Owner = 'bank'"
        cursor.execute(up1)
        
        up2 = "UPDATE utilities SET Owner = 'bank'"
        cursor.execute(up2)
        
        up3 = "UPDATE trains SET Owner = 'bank'"
        cursor.execute(up3)

        up4 = "UPDATE trains SET current_rent = 'rent_1T'"
        cursor.execute(up4)
        
        up5 = "UPDATE cities SET current_rent = 'rent'"
        cursor.execute(up5)
        
        up6 = "UPDATE utilities SET current_rent = 'rent_multiplier_1'"
        cursor.execute(up6)

        up7 = "UPDATE game SET endgame = 0"
        cursor.execute(up7)

        up8 = "UPDATE game SET counter = 0"
        cursor.execute(up8)
        con.commit()
        print("The Saved game is sucessfully deleted!!")
        con.close()
        return True


#continue an saved game
def continuegame():
    con=connect_db()
    cursor=con.cursor()
    cursor.execute("SELECT DISTINCT game_name FROM players")
    names=cursor.fetchone()
    if(names==None):
        return None
    else:
        b=names[0]
        return b

