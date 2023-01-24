from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from datetime import timedelta
from flask import Blueprint,jsonify,request
from . import *
import datetime
from passlib.hash import pbkdf2_sha256 as sha256

transact=Blueprint('transact',__name__) 

@transact.route('/balance', methods=['GET'])
@jwt_required()
def balance():
    
    verify = get_jwt_identity()
    user = verify[5]
   
   
    if user is None:
        return('token expired or tampared go generate a new token to reset your password')
    return jsonify(user)


#deposit route
@transact.route('/deposite', methods=['POST'])
@jwt_required()
def deposit():
        current_user = get_jwt_identity()
        user_id = current_user[0]
        data = request.json
        amount = data['amount']
        pin = data['pin']
        typ = "deposit"             # type of transaction
        now = datetime.datetime.now()
        dt_now = now.strftime("%d-%m-%Y %H:%M:%S")


        my_cursor = mydb.cursor(MySQLdb.cursors.DictCursor)

        my_cursor.execute('SELECT balance FROM register WHERE id = %s', [user_id])
        user = my_cursor.fetchone()
        balance = ''.join(map(str, user))  #change the tuple from the database to string
        user_balance = int(balance)  #change the string to int

        total = user_balance + amount
        print(total)

        if current_user and sha256.verify(pin, current_user[4]):
            my_cursor.execute(""" UPDATE register SET balance=%s WHERE id = %s""", [total, user_id])
            my_cursor.execute("INSERT INTO  transactions (email,amount,type,date) VALUES(%s,%s,%s,%s)", [user_id, amount, typ, dt_now])
            mydb.commit()
            return jsonify(str(amount) + " Deposited " + " Remaining :  " + str(total) + ' balance')
        else:
            return jsonify("invalid pin")


#withdraw route
@transact.route('/withdraw', methods=['POST'])
@jwt_required()
def withdraw():

        current_user = get_jwt_identity()
        user_id = current_user[0]

        data = request.json
        amount = data['amount']
        pin = data['pin']
        typ = "withdraw"       #type of transaction
        now = datetime.datetime.now()
        dt_now = now.strftime("%d-%m-%Y %H:%M:%S")
        my_cursor = mydb.cursor(MySQLdb.cursors.DictCursor)
        my_cursor.execute('SELECT balance FROM register WHERE id = %s', [user_id])
        user = my_cursor.fetchone()
        carry = ''.join(map(str, user))  #change the tuple from the database to string
        change_user = int(carry)     #change the string to int

        if amount >= change_user :
            return jsonify('insufficient account')
        else:

           total = change_user - amount
           if current_user and sha256.verify(pin, current_user[4]):
               my_cursor.execute(""" UPDATE register SET balance=%s WHERE id =%s""", [total,user_id])
               my_cursor.execute("INSERT INTO  transactions (email,amount,type,date) VALUES(%s,%s,%s,%s)", [user_id, amount, typ, dt_now])
               mydb.commit()
               return jsonify ( str(amount) + " withdraw, " + " Remain " + str(total))
           else:
              return jsonify("invalid pin")


@transact.route('/history', methods=['GET'])
@jwt_required()
def history():
        current_user = get_jwt_identity()
        user_id = current_user[0]
        if current_user is None:
                return jsonify('You have to login')
        else:
             my_cursor = mydb.cursor(MySQLdb.cursors.DictCursor)
             my_cursor.execute('SELECT * FROM transactions WHERE email = %s', [user_id])
             user = my_cursor.fetchall()
             return jsonify(user)

#admin
@transact.route('/admin', methods=['GET'])
@jwt_required()
def admin():
        current_user = get_jwt_identity()
        user_id = current_user[0]
        if  current_user is None:
          return jsonify("login to access")
        else:
           my_cursor = mydb.cursor(MySQLdb.cursors.DictCursor)

           my_cursor.execute('SELECT * FROM register')
           user = my_cursor.fetchall()
           return jsonify(user)


@transact.route('/transactions', methods=['GET'])
@jwt_required()
def transactions():
    current_user = get_jwt_identity()
    user_id = current_user[0]
    if current_user  is None:
        return jsonify("login to access")
    else:
        my_cursor = mydb.cursor(MySQLdb.cursors.DictCursor)
        my_cursor.execute('SELECT * FROM transactions ')
        user = my_cursor.fetchall()
        return jsonify(user)