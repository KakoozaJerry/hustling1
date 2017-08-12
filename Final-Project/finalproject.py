from flask import Flask, render_template, request, redirect, jsonify, url_for, session, flash, abort, g
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Users, Events
from flask_sqlalchemy import SQLAlchemy
import datetime
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from forms import Login, RegisterForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm

app = Flask(__name__)

app.config['SECRET_KEY'] = 'deVElpPasswordkey1!'
engine = create_engine('sqlite:///handler.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = 'strong'
login_manager.login_view = 'login'

user = Users()


@login_manager.user_loader
def load_user(user_id):
    return user.query.get(int(user_id))


# Fake Restaurants
# restaurant = {'name': 'The CRUDdy Crab', 'id': '1'}

# restaurants = [{'name': 'The CRUDdy Crab', 'id': '1'}, {'name':'Blue Burgers', 'id':'2'},{'name':'Taco Hut', 'id':'3'}]


# Fake Menu Items
# items = [ {'name':'Cheese Pizza', 'description':'made with fresh cheese', 'price':'$5.99','course' :'Entree', 'id':'1'}, {'name':'Chocolate Cake','description':'made with Dutch Chocolate', 'price':'$3.99', 'course':'Dessert','id':'2'},{'name':'Caesar Salad', 'description':'with fresh organic vegetables','price':'$5.99', 'course':'Entree','id':'3'},{'name':'Iced Tea', 'description':'with lemon','price':'$.99', 'course':'Beverage','id':'4'},{'name':'Spinach Dip', 'description':'creamy dip with fresh spinach','price':'$1.99', 'course':'Appetizer','id':'5'} ]
# item =  {'name':'Cheese Pizza','description':'made with fresh cheese','price':'$5.99','course' :'Entree'}
# items = []

@app.route('/signup/', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()
    if request.method == 'POST':
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        user = Users(name=request.form['name'], password=hashed_password, email=request.form['email'])
        session.add(user)
        session.commit()
        flash('User successfully registered')
        return render_template('hello.html')
    return render_template('signup.html')


# creating an event
@app.route('/create/', methods=['GET', 'POST'])
@app.route('/login/create/', methods=['GET', 'POST'])
def createEvent():
    if request.method == 'POST':
        time = str(request.form['time']).split(':')
        time = datetime.time(int(time[0]), int(time[1]))
        date = str(request.form['date']).split('-')
        date = datetime.date(int(date[0]), int(date[1]), int(date[2]))
        events = Events(name=request.form['name'], fee=request.form['fee'], date=date, time=time,
                        location=request.form['location'],
                        organisers=request.form['organisers'], description=request.form['description'],
                        category=request.form['category'], privacy=request.form['privacy'])
        session.add(events)
        session.commit()
        return render_template('hello.html')
    return render_template('createEvent.html')


# logging in user
'''@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        remember_me = False
        registered_user = session.query(Users).filter_by(name=username)
        if username  not in registered_user:
            return 'invalid'

        #registered_user = Users.query.filter_by(name=username).first()
        if registered_user is None:
                flash('Username or Password is invalid')
                return redirect(url_for('login'))
        if check_password_hash(registered_user.password, request.form['password']):
            login_user(registered_user)
            flash('Logged in successfully')
            return redirect( url_for('index'))
    return render_template('logIn.html')
    form = Login()
    if form.validate_on_submit():
        user = Users.query.filter_by(name=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                flash('Logged in successfully.')
                return redirect(url_for('createEvent'))

        return '<h1>Invalid username or password</h1>'
        # return '<h1>' + form.username.data + ' ' + form.password.data + '</h1>'

    return render_template('sign in.html', form=form)'''


# return redire('home.html')
# return render_template('logIn.html', form=form)

@app.route('/')
@login_required
def index():
    return render_template('home.html')


@app.route('/new', methods=['GET', 'POST'])
@login_required
def new():
    return render_template(createEvent)


@app.route('/todos/<int:todo_id>', methods=['GET', 'POST'])
@login_required
def show_or_update(todo_id):
    return render_template('home.html')


@app.route("/logout")
# @login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.before_request
def before_request():
    g.user = current_user


@app.route('/secret')
@login_required
def secret():
    return 'Only authenticated users are allowed!'


@app.route('/event/<int:register_id>/menu/JSON')
def eventCategoryJSON(register_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(
        restaurant_id=restaurant_id).all()
    return jsonify(MenuItems=[i.serialize for i in items])


@app.route('/event/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def menuItemJSON(restaurant_id, menu_id):
    Menu_Item = session.query(MenuItem).filter_by(id=menu_id).one()
    return jsonify(Menu_Item=Menu_Item.serialize)


@app.route('/event/JSON')
def restaurantsJSON():
    restaurants = session.query(Restaurant).all()
    return jsonify(restaurants=[r.serialize for r in restaurants])


# Show when logged in
@app.route('/')
@app.route('/event/')
def showEvents():
    restaurants = session.query(Events).all()
    # return "This page will show all my events"
    return render_template('landing.html', restaurants=restaurants)


# Create a new restaurant
@app.route('/event/new/', methods=['GET', 'POST'])
def newRestaurant():
    if request.method == 'POST':
        newRestaurant = Restaurant(name=request.form['name'])
        session.add(newRestaurant)
        session.commit()
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('newRestaurant.html')
        # return "This page will be for making a new restaurant"


# Edit a restaurant


@app.route('/event/<int:restaurant_id>/edit/', methods=['GET', 'POST'])
def editRestaurant(restaurant_id):
    editedRestaurant = session.query(
        Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedRestaurant.name = request.form['name']
            return redirect(url_for('showRestaurants'))
    else:
        return render_template(
            'editRestaurant.html', restaurant=editedRestaurant)

        # return 'This page will be for editing restaurant %s' % restaurant_id


# Delete a restaurant


@app.route('/event/<int:restaurant_id>/delete/', methods=['GET', 'POST'])
def deleteRestaurant(restaurant_id):
    restaurantToDelete = session.query(
        Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        session.delete(restaurantToDelete)
        session.commit()
        return redirect(
            url_for('showRestaurants', restaurant_id=restaurant_id))
    else:
        return render_template(
            'deleteRestaurant.html', restaurant=restaurantToDelete)
        # return 'This page will be for deleting restaurant %s' % restaurant_id


# Show a restaurant menu
@app.route('/event/<int:restaurant_id>/')
@app.route('/event/<int:restaurant_id>/menu/')
def showMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(
        restaurant_id=restaurant_id).all()
    return render_template('menu.html', items=items, restaurant=restaurant)
    # return 'This page is the menu for restaurant %s' % restaurant_id


# Create a new menu item


@app.route(
    '/event/<int:event_id>/menu/new/', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    if request.method == 'POST':
        newItem = MenuItem(name=request.form['name'], description=request.form[
            'description'], price=request.form['price'], course=request.form['course'], restaurant_id=restaurant_id)
        session.add(newItem)
        session.commit()

        return redirect(url_for('showMenu', restaurant_id=event_id))
    else:
        return render_template('newmenuitem.html', restaurant_id=event_id)

    return render_template('newMenuItem.html', restaurant=restaurant)
    # return 'This page is for making a new menu item for restaurant %s'
    # %restaurant_id


# Edit a menu item


@app.route('/event/<int:event_id>/menu/<int:menu_id>/edit',
           methods=['GET', 'POST'])
def editMenuItem(event_id, menu_id):
    editedItem = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['description']:
            editedItem.description = request.form['name']
        if request.form['price']:
            editedItem.price = request.form['price']
        if request.form['course']:
            editedItem.course = request.form['course']
        session.add(editedItem)
        session.commit()
        return redirect(url_for('showMenu', restaurant_id=event_id))
    else:

        return render_template(
            'editmenuitem.html', restaurant_id=restaurant_id, menu_id=menu_id, item=editedItem)

        # return 'This page is for editing menu item %s' % menu_id


# Delete a menu item


@app.route('/event/<int:event_id>/menu/<int:menu_id>/delete',
           methods=['GET', 'POST'])
def deleteMenuItem(event_id, menu_id):
    itemToDelete = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        return redirect(url_for('showMenu', restaurant_id=event_id))
    else:
        return render_template('deleteMenuItem.html', item=itemToDelete)
        # return "This page is for deleting menu item %s" % menu_id


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
