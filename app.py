from numerize import numerize
from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3
import hashlib
import locale
import json
from flask import jsonify
locale.setlocale(locale.LC_MONETARY, 'en_IN')
import gamelogiccopy


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


@app.route('/submit', methods=['POST'])
def submit():
    #gamelogiccopy.deletegame()
    gamename = request.form.get('gamename')
    num_players = int(request.form.get('numPlayers'))
    player_names = [request.form.get(f'player{i+1}') for i in range(num_players)]
    print(f'Game Name: {gamename}')
    print(f'Number of Players: {num_players}')
    print(f'Player Names: {player_names}')
    try:
        gamelogiccopy.newgame(num_players, player_names,gamename)
        print("Database updated sucessfully")
        con=connect_db()
        cursor=con.cursor()
        cursor.execute("SELECT current_money FROM players")
        payer_balance=cursor.fetchall()
        player_info = [{'name': player, 'amount': locale.currency(amount[0], grouping=True)} for player, amount in zip(player_names, payer_balance)]
        
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


        return render_template("gamemanager.html",gamename=gamename,num_of_players=num_players,player_info=player_info,player_names=player_names,site_names=site_name,train_names=train_name,utilities_names=utilities_name,paysite_name=paysite_name,payutilities_name=payutilities_name,paytrain_name=paytrain_name)
    except:
        error_title="Database updation errorr!!"
        error_message="Some error occured while updating the database!!"
        return render_template("error.html",error_title=error_title,error_message=error_message)



@app.route('/buy_property', methods=['POST'])
def buy_property():
    data = request.get_json()
    player_name = data.get('playerName')
    property_type = data.get('propertyType')
    specific_property = data.get('specificProperty')
    build_db=gamelogiccopy.building_func(player_name, property_type, specific_property)
    print(build_db)    
    if(build_db==-1):
        return jsonify({'status': 'error', 'message': 'insufficient funds' })
    elif(build_db==1):
        return jsonify({'status': 'success'})
    elif(build_db==0):
        return jsonify({'status': 'error', 'message': 'bought' })
    else:
        return render_template("error.html")

@app.route('/pay_rent', methods=['POST'])
def pay_rent():
    data = request.get_json()
    player_name = data.get('playerName')
    property_type = data.get('propertyType')
    specific_property = data.get('specificProperty')
    diceRoll = data.get('diceRoll')
    print(diceRoll)
    build_db=gamelogiccopy.payingrent_func(player_name, property_type, specific_property,diceRoll)
    print(build_db)    
    if(build_db==-1):
        return jsonify({'status': 'error', 'message': 'insufficient funds' })
    elif(build_db==1):
        return jsonify({'status': 'success'})
    elif(build_db==0):
        return jsonify({'status': 'error', 'message': 'This property is not yet bought! ' })
    elif(build_db==-2):
        return jsonify({'status': 'error', 'message': 'Same Person' })
    else:
        return render_template("error.html")

@app.route('/pay_bank', methods=['POST'])
def pay_bank():
    data = request.get_json()
    player_name = data.get('playerName')
    amt=data.get('amt')
    build_db=gamelogiccopy.pay_bank_func(player_name, amt)
    print(build_db)    
    if(build_db==-1):
        return jsonify({'status': 'error', 'message': 'insufficient funds' })
    elif(build_db==1):
        return jsonify({'status': 'success'})
    else:
        return render_template("error.html")

@app.route('/reward_bank', methods=['POST'])
def reward_bank():
    data = request.get_json()
    player_name = data.get('playerName')
    amt=data.get('amt')
    build_db=gamelogiccopy.reward_bank_func(player_name, amt)
    print(build_db)    
    if(build_db==1):
        return jsonify({'status': 'success'})
    else:
        return jsonify({'status': 'error'})




@app.route('/deletegame', methods=['POST'])
def deletegame():
    data = request.get_json()
    txt = data.get('txt')
    try:
        if(txt==1):
            gamelogiccopy.deletegame()
            return jsonify({'status': 'success',})
        else:
            return jsonify({'status': 'error',})
    except:
        error_title="Database updation errorr!!"
        error_message="Some error occured while deleting the game!!"
        return render_template("error.html",error_title=error_title,error_message=error_message)

if __name__ == '__main__':
    app.run(host="0.0.0.0")
