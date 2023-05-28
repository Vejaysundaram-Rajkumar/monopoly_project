from numerize import numerize
from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3
import hashlib

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

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        num_players = int(request.form['myDropdown'])
        money=2000000
        conn = sqlite3.connect('gamedetails.db')
        cursor = conn.cursor()
        player_name = "aa"
        print(player_name)
        cursor.execute("INSERT INTO players (id,name,current_money) VALUES (?, ?, ?)", (1,player_name,money))
        conn.commit()
        conn.close()

    return redirect('/')


if __name__ == '__main__':
    app.run(host="0.0.0.0")
