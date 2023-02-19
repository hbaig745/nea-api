from flask import Flask
from flask_cors import CORS, cross_origin
from flask import request
from flask import send_file
import json
import sqlite3
from gym_graph import *
from datetime import datetime

app = Flask(__name__)

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

def current_time():
    now = datetime.now()
    current = now.strftime('%H:%M')
    current = current.split(':')
    current = int(current[0])*60 + int(current[1])

    return current

def gym_is_open(gym):
    with open('./gym_information.json', 'r') as f:
        data = json.load(f)
        if gym != 'start':
            if data[gym]['always_open'] == False:
                open_time = data[gym]['open_time'].split(':')
                close_time = data[gym]['close_time'].split(':')

    if gym == 'start':
        return True
    
    if data[gym]['always_open']:
        return True

    open_time = int(open_time[0])*60 + int(open_time[1])
    close_time = int(close_time[0])*60 + int(close_time[1])

    if current_time() in range(open_time, close_time):
        return True
    
    return False
    
@app.route('/gymgraph-picture', methods=['GET'])
def gymgraphPicture():
    return send_file('gym-graph.png', mimetype='image/png')
    

@app.route('/user', methods=['GET', 'POST'])
def user():
    if request.method == 'GET':
        username = request.args.get('username')
        password = request.args.get('password')

        CHECK_USER_EXISTS = 'SELECT * FROM Users WHERE Username=? AND Password=?'
        args = (username, password)

        with sqlite3.connect('database.db') as connection:
            cursor = connection.cursor()
            cursor.execute(CHECK_USER_EXISTS, args)

        result = cursor.fetchall()

        if len(result) == 0:
            return {'data' : False }
        else:
            return {'data' : True}

    if request.method == 'POST':
        data = request.args.get('data')
        data_dict = json.loads(data)

        INSERT_USER_DETAILS = 'INSERT INTO Users (Username, Password, Name, Email, PhoneNumber) VALUES (?, ?, ?, ?, ?)'
        args = (str(data_dict['username']) , str(data_dict['password']), str(data_dict['name']), str(data_dict['email']), str(data_dict['phone']))

        with sqlite3.connect('database.db') as connection:
            cursor = connection.cursor()
            cursor.execute(INSERT_USER_DETAILS, args)

        return 'success'

@app.route('/get_user_details', methods=['GET'])
def get_users():
    username = request.args.get('username')
    GET_USER_DETAILS = f"SELECT * FROM Users WHERE Username = '{username}'"

    with sqlite3.connect('database.db') as connection:
        cursor = connection.cursor()
        cursor.execute(GET_USER_DETAILS)

    return cursor.fetchall()

@app.route('/closest_gym', methods=['GET'])
def closest_gym():
    current_gym = request.args.get('current_gym')

    #initialise the graph
    graph = initialise_graph()
    results = graph.dijkstra(current_gym)
    results['start'] = [10000000, None]
    with open('./gym_information.json', 'r') as f:
        data = json.load(f)
        lowest = 'start'
        for node in results:
            if gym_is_open(node):
                if results[node][0] < results[lowest][0] and node != current_gym:
                    lowest = node
    return f'Closest open gym is {lowest} with a distance of {results[lowest][0]}'

@app.route('/gym_info', methods=['GET'])
def gym_info():

    with open('./gym_information.json', 'r') as f:
        data = json.load(f)
        temp = json.dumps(data)
        return temp

@app.route('/classes', methods=['GET', 'POST'])
def classes():
    if request.method == 'GET':
        GET_CLASSES = 'SELECT * FROM Classes'

        with sqlite3.connect('database.db') as connection:
            cursor = connection.cursor()
            cursor.execute(GET_CLASSES)

        temp = []
        for r in cursor.fetchall():
            temp.append(r)

        temp = str(temp).replace('[','').replace(']','').replace("'", '"')

        return temp

    if request.method == 'POST':
        username = request.args.get('username')
        class_id = request.args.get('classID')
        BOOK_CLASS = 'INSERT INTO UserClass VALUES (?, ?)'
        args = (username, class_id)

        with sqlite3.connect('database.db') as connection:
            cursor = connection.cursor()
            cursor.execute(BOOK_CLASS, args)

        return 'success'

@app.route('/booked-classes', methods=['GET', 'DELETE'])
def booked_classes():

    if request.method == 'GET':
        username = request.args.get('username')
        GET_BOOKED_CLASSES = f"SELECT Classes.ClassName FROM UserClass INNER JOIN Classes ON Classes.ClassID = UserClass.ClassID WHERE UserClass.Username = '{username}'"

        with sqlite3.connect('database.db') as connection:
            cursor = connection.cursor()
            cursor.execute(GET_BOOKED_CLASSES)


        return f"You've booked classes {cursor.fetchall()}"

    if request.method == 'DELETE':
        username = request.args.get('username')
        classId = request.args.get('classID')


        DELETE_BOOKING = f"DELETE FROM UserClass WHERE Username = '{username}' AND ClassID = {classId}"
        print(DELETE_BOOKING)

        with sqlite3.connect('database.db') as connection:
            cursor = connection.cursor()
            cursor.execute(DELETE_BOOKING)

        return 'success'



if __name__ == "__main__":
    app.run(debug=True, port=3005)

