from flask import Flask

app = Flask(__name__)

@app.route('/members', methods=['GET'])
def members():
    return {'members' : ['member1', 'member2']}

if __name__ == "__main__":
    app.run(debug=True, port=3005)

