from flask import Flask,jsonify,request,session
from flask_socketio import SocketIO,emit
from flask_restful import Resource,Api
from flask_cors import CORS
from flask_session import Session
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app,cors_allowed_origins='*',manage_session=True)
api = Api(app)
CORS(app)

#configuring session
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_LIFETIME'] = 3600
app.config['SESSION_USE_SIGNER'] = True

Session(app)

users = {'user1': 'password1', 'user2': 'password2'}
temp_user:str

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

#socket code
@socketio.on('connect')
def user_connect():
    global temp_user
    session['user'] = temp_user
    print("user connected",session)
    emit('thanks',"thank you for connecting")

@socketio.on('my_message')
def user_msg(msg):
    print("request recived")
    print(session)
    if "user" in session:
        print(msg,session['user'])
    else:
        print("there is no user in the session")
@socketio.on('sendmsg')
def send_msge(msg):
    print("message recived",msg)
    emit("recive",{"message":msg,"user":session['user']})

@socketio.on('disconnect')
def user_disconnect():
    session.pop('user',None)
    print("user dissconnected")


#http code
class userHandeler(Resource):
    def get(self):
        return jsonify({
            "message":"working correctly",
            "passed":"ok",
        })
    
    def post(self):
        global temp_user
        _json = request.json
        _name = _json['mail']
        _pass = _json['pass']
        if _name in users and users[_name] == _pass:
            # session['user_n'] = _name
            temp_user = _name
            print("user loged in!!!!")
            return jsonify({
                'message':"user loged in",
                "passed": "ok",
            })
        else:
            print('user not ')

    
api.add_resource(userHandeler,'/api')

if __name__ == "__main__":
    socketio.run(app,debug=True)