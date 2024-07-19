from flask import Flask, request, render_template
import mysql.connector

app = Flask(__name__)

MONTH_NAMES = {
    1: "January", 2: "February", 3: "March", 4: "April",
    5: "May", 6: "June", 7: "July", 8: "August",
    9: "September", 10: "October", 11: "November", 12: "December"
}

def get_friends_by_category(category):
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="friendsdb"
    )
    cursor = connection.cursor(dictionary=True)
    query = """
    SELECT name, image_url, DOB
    FROM friends
    WHERE category = %s
    """
    cursor.execute(query, (category,))
    friends = cursor.fetchall()
    
    # Convert birth month number to month name
    for friend in friends:
        month_num = friend['DOB'].month
        friend['birth_month_name'] = MONTH_NAMES[month_num]
    
    cursor.close()
    connection.close()
    return friends

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_friends', methods=['POST'])
def show_friends():
    category = request.form['category']
    friends = get_friends_by_category(category)
    return render_template('index.html', friends=friends)

if __name__ == '__main__':
    app.run(debug=True)
