from numerize import numerize
from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3
import hashlib
import locale
import json
import random
from flask import jsonify
locale.setlocale(locale.LC_MONETARY, 'en_IN')
import gamelogiccopy
import traceback

#Creating an object for the flask called app
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

#Connect with the customers database to store the user details
def connect_db():
    connection = sqlite3.connect('gamedetails.db')
    return connection

#rendering the landing or the home page
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/manager')
def manager():
    try:
        con=connect_db()
        cursor=con.cursor()
        cursor.execute("SELECT DISTINCT game_name FROM players")
        gname=cursor.fetchone()
        if(gname==None):
            error_message="There is no Saved games found in the database!"
            return redirect(url_for('error', status='No Saved Games found!!', message=error_message))
        else:
            gamename=gname[0]
            cursor.execute("SELECT name FROM players")
            player_name=cursor.fetchall()
            cursor.execute("SELECT * FROM transactions")
            transaction_list=cursor.fetchall()
            player_names= [name[0] for name in player_name]
            num_players=len(player_names)
            cursor.execute("SELECT current_money FROM players")
            payer_balance=cursor.fetchall()
            player_info = [{'name': player, 'amount': locale.currency(amount[0], grouping=True)} for player, amount in zip(player_names, payer_balance)]
            
            players_data = gamelogiccopy.get_players_data(num_players,player_names)

            cursor.execute("SELECT name FROM cities WHERE Owner= ?",("bank",))
            cities_list=cursor.fetchall()
            site_names = [name[0] for name in cities_list]
            
            cursor.execute("SELECT name FROM utilities WHERE Owner= ?",("bank",))
            utilities_list=cursor.fetchall()
            utilities_names = [name[0] for name in utilities_list]
            
            cursor.execute("SELECT name FROM trains WHERE Owner= ?",("bank",))
            trains_list=cursor.fetchall()
            train_names = [name[0] for name in trains_list]

            site_name=json.dumps(site_names)
            utilities_name=json.dumps(utilities_names)
            train_name=json.dumps(train_names)

            cursor.execute("SELECT name FROM cities WHERE Owner!= ?",("bank",))
            cities_list=cursor.fetchall()
            paysite_names = [name[0] for name in cities_list]
            
            cursor.execute("SELECT name FROM utilities WHERE Owner!= ?",("bank",))
            utilities_list=cursor.fetchall()
            payutilities_names = [name[0] for name in utilities_list]
            
            cursor.execute("SELECT name FROM trains WHERE Owner!= ?",("bank",))
            trains_list=cursor.fetchall()
            paytrain_names = [name[0] for name in trains_list]

            
            paysite_name=json.dumps(paysite_names)
            payutilities_name=json.dumps(payutilities_names)
            paytrain_name=json.dumps(paytrain_names)


            return render_template("gamemanager.html",gamename=gamename,num_of_players=num_players,player_info=player_info,player_names=player_names,site_names=site_name,train_names=train_name,utilities_names=utilities_name,paysite_name=paysite_name,payutilities_name=payutilities_name,paytrain_name=paytrain_name,transaction_list=transaction_list)
    except Exception as e:
        
        print(f"Exception: {e}")
        traceback.print_exc()
        error_message = "Some error occurred while updating the database!!"
        return redirect(url_for('error', status='Database updation errorr!!', message=error_message))
    
@app.route('/submit', methods=['POST'])
def submit():
    gamelogiccopy.deletegame()
    gamename = request.form.get('gamename')
    num_players = int(request.form.get('numPlayers'))
    player_names = [request.form.get(f'player{i+1}') for i in range(num_players)]
    print(f'Game Name: {gamename}')
    print(f'Number of Players: {num_players}')
    print(f'Player Names: {player_names}')
    try:
        gamelogiccopy.newgame(num_players, player_names,gamename)
        print("Database updated sucessfully")
        return redirect('/manager')
    except:
        error_message="Some error occured while updating the database!!"
        return redirect(url_for('error', status='Database updation errorr!!', message=error_message))

@app.route('/endgame')
def endgame():
    try:
        result=gamelogiccopy.result_func()
        formatted_result = []
        for i in range(len(result)):
            formatted_value = locale.currency(result[i][2], grouping=True)
            formatted_result.append((result[i][0], result[i][1], formatted_value))
        winner_name = formatted_result[0][1]
        return render_template('leaderboard.html', players=formatted_result, winner_name=winner_name)
    
    except:
        error_message="There is no Saved games found in the database!"
        return redirect(url_for('error', status='No Saved Games found!!', message=error_message))
    

@app.route('/buy_property', methods=['POST'])
def buy_property():
    try:
        data = request.get_json()
        player_name = data.get('playerName')
        property_type = data.get('propertyType')
        specific_property = data.get('specificProperty')
        build_db=gamelogiccopy.building_func(player_name, property_type, specific_property)
        print(build_db)    
        if(build_db==-1):
            return jsonify({'status': 'error', 'message': 'insufficient funds !! You dont have enough funds to buy this property.' })
        elif(build_db==-2):
            return jsonify({'status': 'error', 'message': 'No property available right now!' })
        elif(build_db==1):
            return jsonify({'status': 'success'})
        elif(build_db==0):
            return jsonify({'status': 'error', 'message': 'bought already!!' })
        else:
            return jsonify({'status': 'error', 'message': '404' })
    except:    
        error_message="Some error occured while buying the property!!"
        return redirect(url_for('error', status='Database updation errorr!!', message=error_message))

@app.route('/pay_rent', methods=['POST'])
def pay_rent():
    try:
        data = request.get_json()
        player_name = data.get('playerName')
        property_type = data.get('propertyType')
        specific_property = data.get('specificProperty')
        diceRoll = data.get('diceRoll')
        print(diceRoll)
        build_db=gamelogiccopy.payingrent_func(player_name, property_type, specific_property,diceRoll)
        print(build_db)    
        if(build_db==-1):
            return jsonify({'status': 'error', 'message': 'insufficient funds!! You dont have enough funds to buy this property.' })
        elif(build_db==-3):
            return jsonify({'status': 'error', 'message': 'No property available right now!' })
        elif(build_db==1):
            return jsonify({'status': 'success'})
        elif(build_db==0):
            return jsonify({'status': 'error', 'message': 'This property is not yet bought! ' })
        elif(build_db==-2):
            return jsonify({'status': 'error', 'message': 'Same Person' })
        else:
            return jsonify({'status': 'error', 'message': '404' })
    except:        
        error_message="Some error occured while paying the rent!!"
        return redirect(url_for('error', status='Database updation errorr!!', message=error_message))

@app.route('/pay_bank', methods=['POST'])
def pay_bank():
    try:
        data = request.get_json()
        player_name = data.get('playerName')
        amt=data.get('amt')
        build_db=gamelogiccopy.pay_bank_func(player_name, amt)
        print(build_db)    
        if(build_db==-1):
            return jsonify({'status': 'error', 'message': 'insufficient funds !! You dont have enough funds to pay the bank!.' })
        elif(build_db==1):
            return jsonify({'status': 'success'})
        else:
            return jsonify({'status': 'error', 'message':'404'})
    except:
        error_message="Some error occured while paying the bank!!"
        return redirect(url_for('error', status='Database updation errorr!!', message=error_message))

@app.route('/reward_bank', methods=['POST'])
def reward_bank():
    try:
        data = request.get_json()
        player_name = data.get('playerName')
        amt=data.get('amt')
        build_db=gamelogiccopy.reward_bank_func(player_name, amt)
        print(build_db)    
        if(build_db==1):
            return jsonify({'status': 'success'})
        else:
            return jsonify({'status': 'error','message':'404'})
    except:
        error_message="Some error occured while transwering the reward!!"
        return redirect(url_for('error', status='Database updation errorr!!', message=error_message))

@app.route('/collectsalary', methods=['POST'])
def collectsalary():
    try:
        data = request.get_json()
        player_name = data.get('playerName')
        build_db=gamelogiccopy.collect_salary_func(player_name)
        print(build_db)    
        if(build_db==1):
            return jsonify({'status': 'success'})
        else:
            return jsonify({'status': 'error','message':'404' })
    except:
        error_message="Some error occured while transwering your salary!!"
        return redirect(url_for('error', status='Database updation errorr!!', message=error_message))

@app.route('/chance', methods=['POST'])
def chance():
    try:
        id=random.choice(chance_ids)
        print(id)
        data = request.get_json()
        player_name = data.get('playerName')
        build_db=gamelogiccopy.chance_func(player_name,id)
        print(build_db)    
        if(build_db[0]==1):
            return jsonify({'status': 'success','message':build_db[1]})
        else:
            return jsonify({'status': 'error','message':'404'})
    except:
        error_message="Some error occured while implementing the chance statement!!"
        return redirect(url_for('error', status='Database updation errorr!!', message=error_message))

@app.route('/communitychest', methods=['POST'])
def communitychest():
    try:
        id=random.choice(community_chest_ids)
        data = request.get_json()
        player_name = data.get('playerName')
        build_db=gamelogiccopy.community_chest_func(player_name,id)
        print(build_db)    
        if(build_db[0]==1):
            return jsonify({'status': 'success','message':build_db[1]})
        else:
            return jsonify({'status': 'error','message':'404'})
    except:
        error_message="Some error occured while implementing the chance statement!!"
        return redirect(url_for('error', status='Database updation errorr!!', message=error_message))

@app.route('/buildingconstruction', methods=['POST'])
def buildingconstruction():
    try:
        data = request.get_json()
        player_name = data.get('playerName')
        property_type = data.get('propertyType')
        specific_property = data.get('specificProperty')
        print(specific_property)
        build_db=gamelogiccopy.buy_house_hotel_func(player_name, property_type, specific_property)
        print(build_db)    
        if(build_db==-1):
            return jsonify({'status': 'error', 'message': 'insufficient funds!! You dont have enough funds to buy this property.' })
        elif(build_db==-2):
            return jsonify({'status': 'error', 'message': 'Required houses not yet built' })
        elif(build_db==1):
            return jsonify({'status': 'success'})
        elif(build_db==0):
            return jsonify({'status': 'error', 'message': 'player and owner mismatch! ' })
        elif(build_db==-3):
            return jsonify({'status': 'error', 'message': 'Property not yet bought' })
        elif(build_db==-4):
            return jsonify({'status': 'error', 'message': 'No property available right now!' })
        elif(build_db==4):
            return jsonify({'status': 'error', 'message': 'maximum house is built!' })
        elif(build_db==5):
            return jsonify({'status': 'error', 'message': 'maximum hotel is built!' })
        elif(build_db==9):
            return jsonify({'status': 'error', 'message': 'maximum number of hotel and houses is built!' })
        else:
            return jsonify({'status': 'error', 'message': '404' })
    except:
        error_message="Some error occured while paying the rent!!"
        return redirect(url_for('error', status='Database updation errorr!!', message=error_message))

@app.route('/deletegame', methods=['POST'])
def deletegame():
    data = request.get_json()
    txt = data.get('txt')
    try:
        if(txt==1):
            st=gamelogiccopy.deletegame()
            if(st!=None):
                return jsonify({'status': 'success',})
            else:
                print("gg")
                return jsonify({'status': 'error', 'message': 'no game found'})
        else:
            return jsonify({'status': 'error','message': '404'})
    except:
        error_message="Some error occured while deleting the game!!"
        return redirect(url_for('error', status='Database updation errorr!!', message=error_message))


@app.route('/error')
def error():
    status = request.args.get('status', 'unknown')
    message = request.args.get('message', 'An error occurred.')
    return render_template('error.html', error_title=status, error_message=message), 500

con=connect_db()
cursor=con.cursor()
cursor.execute('SELECT Id FROM cards WHERE Option = "community chest"')
community_chest_ids = [row[0] for row in cursor.fetchall()]
# Get IDs for rows with "chance"
cursor.execute('SELECT Id FROM cards WHERE Option = "chance"')
chance_ids = [row[0] for row in cursor.fetchall()]
con.close()


if __name__ == '__main__':
    app.run(host="0.0.0.0")
