from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)


db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="friendsdb"
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_friends', methods=['POST'])
def get_friends():
    category = request.form['category']
    month = request.form['month']
    

   
    cursor = db.cursor(dictionary=True)
    query = "SELECT name FROM friends WHERE category = %s AND MONTH(DOB) = %s"
    cursor.execute(query, (category, month))
    friends = cursor.fetchall()

    return render_template('friends_list.html', friends=friends,category=category,month=month)

if __name__ == '__main__':
    app.run(debug=True)
