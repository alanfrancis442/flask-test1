from flask import Flask,jsonify
from flask_socketio import SocketIO,emit
from flask_restful import Resource,Api
from flask_cors import CORS
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app,cors_allowed_origins='*')
api = Api(app)
CORS(app)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

#socket code
@socketio.on('connect')
def user_connect():
    print("user connected")
    emit('thanks',"thank you for connecting")

@socketio.on('my_message')
def user_connect(msg):
    print(msg)

@socketio.on('disconnect')
def user_disconnect():
    print("user dissconnected")


#http code
class userHandeler(Resource):
    def get(self):
        return jsonify({
            "message":"working correctly",
            "passed":"ok",
        })
    
api.add_resource(userHandeler,'/api')

if __name__ == "__main__":
    socketio.run(app,debug=True)