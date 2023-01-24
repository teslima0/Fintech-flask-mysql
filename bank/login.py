from flask_jwt_extended import create_access_token

from flask_jwt_extended import current_user
from flask import request,Blueprint,jsonify
from . import *
from passlib.hash import pbkdf2_sha256 as sha256

auths=Blueprint('auths',__name__) 

#login route
@auths.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data['email']
    password = data['password']
    my_cursor = mydb.cursor(MySQLdb.cursors.DictCursor)
    my_cursor.execute('''SELECT * FROM register WHERE email = %s ''', [email])  #check db if the email exist
    query = my_cursor.fetchone()
    if query and sha256.verify(password, query[3]):
        access_token = create_access_token(identity=query)  
        return jsonify(access_token=access_token)
    else:
        return jsonify('email or password is incorrect'),401