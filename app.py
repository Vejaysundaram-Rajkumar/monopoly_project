from numerize import numerize
from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3
import hashlib
import locale
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
        return render_template("gamemanager.html",gamename=gamename,num_of_players=num_players,player_info=player_info)
    else:
        print("Database updation errorr!!")
        return render_template("error.html")




if __name__ == '__main__':
    app.run(host="0.0.0.0")
