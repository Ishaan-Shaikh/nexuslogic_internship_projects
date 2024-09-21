#libraries
from flask import Flask, render_template, request, redirect, url_for
from models import db, Item, User
from werkzeug.security import generate_password_hash, check_password_hash

#flask framework
#error- ara tha yaha pe
#geeks pe dekh le
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# DB (file type db)
with app.app_context():
    db.create_all()

# Dashboard Route (View Items)
@app.route('/dashboard')
def dashboard():
    items = Item.query.all()  # Fetch all items from the database
    return render_template('items.html', items=items)

# Home Route
@app.route('/')
def index():
    return render_template('index.html')

# User Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Query the user from the database
        user = User.query.filter_by(username=username).first()
        
        # Verify the password
        if user and check_password_hash(user.password, password):
            return redirect(url_for('dashboard'))  # Redirect to dashboard after successful login
        else:
            return 'Invalid credentials'
    
    return render_template('login.html')

# User Registration Route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        try:
            hashed_password = generate_password_hash(password)  # No need to specify the method
            new_user = User(username=username, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))
        except Exception as e:
            print(f"Error: {e}")  # Print the error to the console for debugging
            return 'An error occurred while registering. Please try again.'
    
    return render_template('signup.html')

# Add Item Route
@app.route('/add_item', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        quantity = request.form['quantity']
        
        new_item = Item(name=name, description=description, quantity=quantity)
        db.session.add(new_item)
        db.session.commit()
        
        return redirect(url_for('dashboard'))
    
    return render_template('add_item.html')

# Update Item Route
@app.route('/update_item/<int:id>', methods=['GET', 'POST'])
def update_item(id):
    item = Item.query.get_or_404(id)
    
    if request.method == 'POST':
        item.name = request.form['name']
        item.description = request.form['description']
        item.quantity = request.form['quantity']
        
        db.session.commit()
        return redirect(url_for('dashboard'))
    
    return render_template('update_item.html', item=item)

# Delete Item Route
@app.route('/delete_item/<int:id>')
def delete_item(id):
    item = Item.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    
    return redirect(url_for('dashboard'))

# script and debug yahase karenga
if __name__ == '__main__':
    app.run(debug=True)

  # This creates the necessary tables in your database



# from flask import Flask, render_template, request, redirect, url_for, flash, session
# from flask_sqlalchemy import SQLAlchemy
# from werkzeug.security import generate_password_hash, check_password_hash

# app = Flask(__name__)
# app.config['SECRET_KEY'] = 'your_secret_key'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory.db'
# db = SQLAlchemy(app)


# # MODELS yahape dalunga
# # test = "hello"
# # print(test)
# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(150), nullable=False, unique=True)
#     password_hash = db.Column(db.String(150), nullable=False)

#     def set_password(self, password):
#         self.password_hash = generate_password_hash(password)

#     def check_password(self, password):
#         return check_password_hash(self.password_hash, password)

# class Item(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     description = db.Column(db.String(300), nullable=True)
#     quantity = db.Column(db.Integer, nullable=False)
#     price = db.Column(db.Float, nullable=False)

# # Create the database
# with app.app_context():
#     db.create_all()

# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         if User.query.filter_by(username=username).first():
#             flash('Username already exists')
#             return redirect(url_for('register'))
        
#         new_user = User(username=username)
#         new_user.set_password(password)
#         db.session.add(new_user)
#         db.session.commit()
#         flash('Registration successful!')
#         return redirect(url_for('login'))
    
#     return render_template('register.html')

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         user = User.query.filter_by(username=username).first()
#         if user and user.check_password(password):
#             session['user_id'] = user.id
#             return redirect(url_for('view_items'))
#         flash('Invalid username or password')
    
#     return render_template('login.html')

# @app.route('/logout')
# def logout():
#     session.pop('user_id', None)
#     flash('You have been logged out')
#     return redirect(url_for('login'))


# @app.route('/items')
# def view_items():
#     if 'user_id' not in session:
#         return redirect(url_for('login'))
    
#     items = Item.query.all()
#     return render_template('items.html', items=items)

# @app.route('/item/add', methods=['GET', 'POST'])
# def add_item():
#     if 'user_id' not in session:
#         return redirect(url_for('login'))
    
#     if request.method == 'POST':
#         name = request.form['name']
#         description = request.form['description']
#         quantity = int(request.form['quantity'])
#         price = float(request.form['price'])

#         new_item = Item(name=name, description=description, quantity=quantity, price=price)
#         db.session.add(new_item)
#         db.session.commit()

#         return redirect(url_for('view_items'))
    
#     return render_template('add_item.html')

# @app.route('/item/update/<int:id>', methods=['GET', 'POST'])
# def update_item(id):
#     if 'user_id' not in session:
#         return redirect(url_for('login'))
    
#     item = Item.query.get_or_404(id)
#     if request.method == 'POST':
#         item.name = request.form['name']
#         item.description = request.form['description']
#         item.quantity = int(request.form['quantity'])
#         item.price = float(request.form['price'])
#         db.session.commit()

#         return redirect(url_for('view_items'))

#     return render_template('update_item.html', item=item)

# @app.route('/item/delete/<int:id>')
# def delete_item(id):
#     if 'user_id' not in session:
#         return redirect(url_for('login'))
    
#     item = Item.query.get_or_404(id)
#     db.session.delete(item)
#     db.session.commit()

#     return redirect(url_for('view_items'))


# if __name__ == '__main__':
#     app.run(debug=True)