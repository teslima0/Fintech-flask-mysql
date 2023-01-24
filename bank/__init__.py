from flask_swagger_ui import get_swaggerui_blueprint
from flask import Flask,send_from_directory,Blueprint
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from os import path
import mysql.connector
import MySQLdb.cursors
from flask_jwt_extended import JWTManager
db=SQLAlchemy()
app= Flask(__name__)
from connexion.resolver import RestyResolver
from flask_restx import Api



#app.register_blueprint(request_api.get_blueprint())

app.config['SECRET_KEY']= '234d45f959e5465ebde816af8c51ce21'
mydb = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = '',
    database = 'fintech',
    )
def create_app():
    app= Flask(__name__)
    app.config['SECRET_KEY']= '234d45f959e5465ebde816af8c51ce21'
    #app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db" 
    app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://root:pa@127.0.0.1:3306/fintech' 
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] =timedelta(hours=2)
    db.init_app(app)
    jwt = JWTManager(app)
    SWAGGER_URL = '/swagger'
    API_URL='/static/swagger.json'
    SWAGGER_BLUPRINT= get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': 'Todo List API'
    }
    )

    app.register_blueprint(SWAGGER_BLUPRINT, url_prefix= SWAGGER_URL)
    '''
    @app.route('/static/<path:path>')
    def send_static(path):
        return send_from_directory('static',path)

    SWAGGER_URL= '/swagger'
    API_URL= '/static/swagger.json'
    swaggerui_blueprint=get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'api_name':"Python Flask"
    }

    )
    app.register_blueprint(swaggerui_blueprint,url_prefix=SWAGGER_URL)
    '''
    

    my_cursor = mydb.cursor()


    my_cursor.execute( '''CREATE TABLE IF NOT EXISTS register (
        id INT(11) NOT NULL AUTO_INCREMENT,
        fullname	VARCHAR(50) NOT NULL,
        email	VARCHAR(120) NOT NULL,
        password	VARCHAR(200) NOT NULL,
        transaction_pin VARCHAR(200) NOT NULL,
        balance INT(200)  NOT NULL,
        PRIMARY KEY(id),
        UNIQUE(email)
    )
    ''')
    mydb.commit()

    my_cursor = mydb.cursor()

  


    my_cursor.execute( '''CREATE TABLE IF NOT EXISTS transactions (
        trans_id INT(11) NOT NULL AUTO_INCREMENT,
        email	VARCHAR(120) NOT NULL,
        amount INT(200)  NOT NULL,
        type VARCHAR(20) NOT NULL,
        date VARCHAR(120) NOT NULL,
        PRIMARY KEY(trans_id)
        
        )
        ''')
    mydb.commit()

    #register view
    from .register import views
    from .login import auths
    from .transactions import transact
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auths, url_prefix='/')
    app.register_blueprint(transact, url_prefix='/')

    return app
