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

@app.route('/deletegame')
def deletegame():
    return render_template("error.html")

@app.route('/submit', methods=['POST'])
def submit():
    gamename = request.form.get('gamename')
    num_players = int(request.form.get('numPlayers'))
    player_names = [request.form.get(f'player{i+1}') for i in range(num_players)]
    print(f'Game Name: {gamename}')
    print(f'Number of Players: {num_players}')
    print(f'Player Names: {player_names}')
    db=gamelogiccopy.newgame(num_players, player_names,gamename)
    if(db):
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

        return render_template("gamemanager.html",gamename=gamename,num_of_players=num_players,player_info=player_info,player_names=player_names,site_names=site_name,train_names=train_name,utilities_names=utilities_name)
    else:
        print("Database updation errorr!!")
        return render_template("error.html")

@app.route('/buy_property', methods=['POST'])
def buy_property():
    data = request.get_json()
    player_name = data.get('playerName')
    property_type = data.get('propertyType')
    specific_property = data.get('specificProperty')
    build_db=gamelogiccopy.building_func(player_name, property_type, specific_property)    
    if(build_db==-1):
        return render_template("insuff_amount.html")
    elif(build_db==0):
        con=connect_db()
        cursor=con.cursor()
        cursor.execute("SELECT game_name FROM players")
        gamename=cursor.fetchone()
        cursor.execute("SELECT COUNT(*) FROM players")
        num_players=cursor.fetchone()  
        cursor.execute("SELECT name FROM players")
        p_names=cursor.fetchall()
        player_names = [name[0] for name in p_names]
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

        return render_template("gamemanager.html",gamename=gamename[0],num_of_players=num_players[0],player_info=player_info,player_names=player_names,site_names=site_name,train_names=train_name,utilities_names=utilities_name)

    elif(build_db==1):
        build_status=1
    else:
        return render_template("error.html")
    return jsonify({'status': build_status})


if __name__ == '__main__':
    app.run(host="0.0.0.0")
