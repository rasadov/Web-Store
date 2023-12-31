from market import db, bcrypt, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email_adress = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    budget = db.Column(db.Integer(), nullable=False, default=100000)
    items = db.relationship('Item', backref="owned_user", lazy=True)

    @property
    def prettier_budget(self):
        if len(str(self.budget)) >= 4:
            return "{:,}$".format(self.budget)
        else: return f"{self.budget}$"

    @property
    def password(self):
        return self.password
    
    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def chech_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)
    
    def can_afford(self, item_obj):
        return self.budget >= item_obj.price
        

class Item(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False, unique=False)
    price = db.Column(db.Integer(), nullable=False)
    description = db.Column(db.String(length=1024),
                            nullable=False, unique=False)
    owner = db.Column(db.Integer(), db.ForeignKey('user.id'))
    forsale = db.Column(db.Integer(), nullable=False)
    def __repr__(self) -> str:
        return f'Item {self.name}'
    
    def buy(self, buyer):
        if self.forsale:
            user = User.query.filter_by(id=self.owner).first()
            user.budget += self.price
            self.owner = buyer.id
            buyer.budget -= self.price
            self.forsale = 0
            db.session.commit()
    def sell(self):
        self.forsale = 1
        db.session.commit()
    
    def stop_selling(self):
        self.forsale = 0
        db.session.commit()