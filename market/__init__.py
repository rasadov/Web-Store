from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market.db'
app.config['SECRET_KEY'] = 'a637a56ab80d8a3ba645ac50'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


from market.modules import User, Item
from market import routes



# with app.app_context():
#     db.create_all()
    # u1 = User(username='rauf',password_hash='123456',email_adress='randombs@gmail.com')
    # db.session.add(u1)
    # item1 = Item.query.all()[0]
    # item2 = Item.query.all()[1]
    # item2.owner = User.query.all()[0].id

    # db.create_all()
    # item1 = Item(name="Ford", price=50000, description="ksdhgfdggkjhsd", owner=5, forsale=1)
    # db.session.add(item1)
    # db.session.commit()
    # Item.query.all()
    # item2 = Item(name="BMW", price=60000,
    #              barcode="457266435834", description="decsasd")
    # db.session.add(item2)
    # db.session.commit()
    # for i in Item.query.filter_by(id=1):
    #     print(i.name)
    #     print(i.price)
    #     print(i.description)
    #     print(i.id)
    #     print(i.barcode)
    #     print()

