from market import app
from flask import render_template, redirect, url_for, flash, get_flashed_messages, request
from market.modules import Item
from market.modules import User
from market.forms import RegisterForm, LoginForm, PurchaseItemForm, SellItemForm, StopSellingForm, CreateItemForm
from market import db  
from flask_login import login_user, login_manager, logout_user, current_user

@app.route("/")
@app.route("/home")
def home_page():
    return render_template("index.html")


@app.route("/market", methods=['GET','POST'])
def market_page():
    purchase_form = PurchaseItemForm()
    if request.method == "POST":
        if current_user.is_authenticated:
            purchased_item = request.form.get('purchased_item')
            p_item_obj = Item.query.filter_by(name=purchased_item).first()
            if p_item_obj:
                if current_user.can_afford(p_item_obj):
                    p_item_obj.buy(current_user)
                    flash(f"You puchased {p_item_obj.name} for {p_item_obj.price} ", category="success")
                else: flash("You dont have enough money to buy this", category="danger")
        else: 
            flash("First you have to log in", category="danger")
        return redirect(url_for('market_page'))
    
    if request.method == 'GET':
        items = Item.query.filter_by(forsale=1)
        if current_user.is_authenticated:
            owned_items = Item.query.filter_by(owner=current_user.id)
        else:
            owned_items = []
        return render_template('market.html', items=items, owned_items=owned_items, purchase_form=purchase_form)

@app.route("/register", methods=['GET','POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email_adress=form.email_adress.data,
                              password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        # form = LoginForm()
        login_user(user_to_create)
        return redirect(url_for('market_page'))
    if form.errors != {}: # if there are no errors from validations
        for err_msg in form.errors.values():
            flash(f"There was an error: {err_msg[0]}", category='danger')
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET','POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first() 
        if attempted_user and attempted_user.chech_password_correction(
            attempted_password=form.password.data):
            login_user(attempted_user)
            flash(f"Success! You are logged in as: {attempted_user.username}", category='success')
            return redirect(url_for('market_page'))
        else: flash('Username and password are not match', category='danger')
    # else: flash('Username and password are not match', category='danger')
    return render_template('login.html', form=form)

@app.route('/logout')
def logout_page():
    logout_user()
    flash("You have been logged out", category="info")
    return redirect(url_for("home_page"))

@app.route('/profile/<username>', methods=['GET','POST'])
def profile(username):
    sell_form = SellItemForm()
    stop_form = StopSellingForm()
    user = User.query.filter_by(username=username).first()
    if user == None:
        return render_template('404.html')
    if request.method == 'GET':
        print(user.id)
        owned_items = Item.query.filter_by(owner=user.id)
        if owned_items.count() == 0:
            owned_items = 0
        print(owned_items)
        return render_template('profile.html', username=username, owned_items=owned_items, sell_form=sell_form, stop_form=stop_form)
        
    if request.method == 'POST':
        if current_user.username == username:
            sold_item = request.form.get('sell_item')
            p_item_obj = Item.query.filter_by(name=sold_item).first()
            if p_item_obj:
                p_item_obj.sell()
                flash(f"You put an offer: {p_item_obj.name} for {p_item_obj.price} ", category="success")
            
            stop_selling = request.form.get('stop_selling')
            p_item_obj = Item.query.filter_by(name=stop_selling).first()
            if p_item_obj:
                p_item_obj.stop_selling()
                flash(f"You removed the offer: {p_item_obj.name} for {p_item_obj.price} ", category="success")
        else: 
            flash("First you have to log in", category="danger")
        return redirect(url_for('profile', username=username) )


@app.route("/create_item", methods=['GET','POST'])
def create_item_page():
    form = CreateItemForm()
    if request.method == "GET":
        return render_template('create_item.html', create_form=form)
    
    if form.validate_on_submit():
        item_to_create = Item(name=form.name.data,
                                price=form.price.data,
                                description=form.description.data,
                                owner=current_user.id,
                                forsale=1)
                                
        db.session.add(item_to_create)
        db.session.commit()
        return redirect(url_for('market_page'))
    
    return render_template('create_item.html', create_form=form)
