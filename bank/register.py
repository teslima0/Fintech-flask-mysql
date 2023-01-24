from flask import request,jsonify,Blueprint
from . import *
from passlib.hash import pbkdf2_sha256 as sha256
#registration route

views=Blueprint('views',__name__) 
@views.route('/register', methods=['POST'])
def register():
    data = request.json
    fullname = data['fullname']
    email = data['email']
    password = data['password']
    confirm_password = data['confirm_password']
    transaction_pin = data['transaction_pin']
    confirm_pin = data['confirm_pin']
    my_cursor = mydb.cursor(MySQLdb.cursors.DictCursor)
    my_cursor.execute(''' SELECT * FROM register WHERE email = %s''', [email])
    query = my_cursor.fetchone()
    if query :
       return jsonify('email already exit! choose a different email ')
    else:
       if password == confirm_password :
          hash_password = sha256.hash(password)
       else:
            return jsonify('password didnt match')

       if transaction_pin == confirm_pin:
         if len(transaction_pin) !=4:
            return jsonify('pin must be 4 digits')
         else:
            hash_pin = sha256.hash(transaction_pin)
            my_cursor.execute('''INSERT INTO register(fullname, email, password, transaction_pin) VALUES (%s, %s, %s, %s)  ''' , [fullname, email, hash_password, hash_pin])
            mydb.commit()
            return jsonify('Thanks for registering you can login now')
       else:
         return jsonify('your pin didn\'t match')