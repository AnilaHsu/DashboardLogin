from flask import Flask, Response, request
import sqlite3
from flask.json import jsonify
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "super-iot" 
jwt = JWTManager(app)

@app.route('/login', methods=['POST'])
def login():
    try:
        json = request.get_json()
        username = json["username"]
        password = json["password"]
    except:
        return Response(status=400)
    
    conn = sqlite3.connect('accounts.db')
    c = conn.cursor()
    c.execute('SELECT * FROM accounts where username=? and password=?', (username, password))
    info = c.fetchone()

    access_token = create_access_token(identity=username)
    
    if info:
        return jsonify({
            "access_token": access_token
        })
    else:
        return Response(status=403)