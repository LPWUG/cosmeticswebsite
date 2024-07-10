import pickle
from flask import Flask, flash, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import numpy as np

from flask_wtf.csrf import validate_csrf

from sklearn import linear_model
from sklearn.calibration import LabelEncoder
from sklearn.discriminant_analysis import StandardScaler
import sklearn.model_selection
from wtforms import BooleanField, FloatField, StringField, PasswordField, SubmitField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length, Email, EqualTo
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user, logout_user
from flask_wtf import CSRFProtect


import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier


from flask_bcrypt import Bcrypt




app = Flask(__name__)

app.app_context().push()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'rZ5£2V1$~Wty'
csrf = CSRFProtect(app)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)



login_manager = LoginManager(app)
login_manager.login_view = "sign_in_page"
login_manager.login_message_category = "info"

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

########################################### MODEL AI CLASSFICATION #######################################
# Load and preprocess data
df = pd.read_csv('skincare.csv')

le_skin_type = LabelEncoder()
df['SkinTypeLabel'] = le_skin_type.fit_transform(df['Skin_Type'])

skin_types = ['SkinTypeLabel']
X = df[skin_types] 
y = df['SkinTypeLabel']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)

clf = RandomForestClassifier(random_state=42)
clf.fit(X_train, y_train)

y_pred = clf.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Model Accuracy: {accuracy:.2f}")

@app.route('/recommendation_form')
def index():
    skin_types = sorted(df['Skin_Type'].unique())
    categories = Category.query.all()
    return render_template('recommendation_form.html', skin_types=skin_types,categories=categories)

@app.route('/remmended', methods=['POST'])
def recommend():
    skin_type = request.form['skin_type']
    categories = Category.query.all()
    df_query = pd.DataFrame({'SkinTypeLabel': [df[df['Skin_Type'] == skin_type]['SkinTypeLabel'].iloc[0]]})
    predictions = clf.predict(df_query)
    
    recommended_products = df[df['SkinTypeLabel'] == predictions[0]].head(10).to_dict(orient='records')

    return render_template('recommandation_product.html', skin_type=skin_type, products=recommended_products,
                            accuracy=accuracy,categories=categories)

########################################### END MODEL CODE ###############################################

class UsersEmail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email_address_user = db.Column(db.String(length=50), nullable=False, unique=True)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    image_url_category = db.Column(db.String(), nullable=True)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name_product = db.Column(db.String(length=30), nullable=False, unique=True)
    image_url_product = db.Column(db.String(length=200), nullable=True)
    price_product = db.Column(db.Integer, nullable=False)
    shipping_address_product = db.Column(db.String(length=40), nullable=False)
    size_product = db.Column(db.String(length=10), nullable=True)
    color_product = db.Column(db.String(length=10), nullable=True)
    description_product = db.Column(db.String(length=1000), nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    category_product = db.relationship('Category', backref=db.backref('items', lazy=True))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))



class Bag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    products = db.relationship('BagProduct', back_populates='bag')

class BagProduct(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bag_id = db.Column(db.Integer, db.ForeignKey('bag.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('item.id'))
    quantity = db.Column(db.Integer, nullable=False, default=1)
    price = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(200), nullable=False)
    bag = db.relationship('Bag', back_populates='products')
    product = db.relationship('Item')
    bag = db.relationship('Bag', back_populates='products')
    product = db.relationship('Item')


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name_user = db.Column(db.String(length=30), nullable=False, unique=True)
    email_address_user = db.Column(db.String(length=50), nullable=False, unique=True)
    password_user = db.Column(db.String(length=60), nullable=False)
    retype_password_user = db.Column(db.String(length=60), nullable=False)
    items = db.relationship('Item', backref=db.backref('user_products', lazy=True))
    bag = db.relationship('Bag', uselist=False, backref='user') 

    @property
    def password(self):
        return self.password_user
    
    @password.setter
    def password(self, plain_text_password):
        self.password_user = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    @property
    def retype_password(self):
        return self.retype_password_user
    
    @retype_password.setter
    def retype_password(self, plain_text_password):
        self.retype_password_user = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_user, attempted_password)
    
    def check_retype_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.retype_password_user, attempted_password)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    brand = db.Column(db.String())
    price = db.Column(db.String())
    rank = db.Column(db.String())


class RegisterForm(FlaskForm):
    username = StringField(label='Username', validators=[Length(min=4, max=30), DataRequired()])
    email_address = StringField(label='Email', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='Password', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label='Confirm Password', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Create An Account')


class EmailForm(FlaskForm):
    email = StringField(label='Email', validators=[Email(), DataRequired()])
    Submit = SubmitField(label='Subscribe')

class SignInForm(FlaskForm):
    username = StringField(label='Username', validators=[Length(min=4, max=30), DataRequired()])
    password = PasswordField(label='Password', validators=[Length(min=6), DataRequired()])
    submit = SubmitField(label='Sign In')

class AddProductForm(FlaskForm):
    name_product = StringField(label='Product Name', validators=[Length(min=6, max=30), DataRequired()])
    image_url_product = StringField(label='Image URL', validators=[DataRequired()])
    product_price = StringField(label='Product Price', validators=[DataRequired()])
    shipping_address = StringField(label='Shipping Address', validators=[Length(min=6), DataRequired()])
    size_product = StringField(label='Product Size', validators=[DataRequired()])
    color_product = StringField(label='Product Color', validators=[Length(max=20), DataRequired()])
    description_product = StringField(label='Product Description', validators=[Length(min=100, max=3000), DataRequired()])
    categoryid = StringField(label='Category ID', validators=[DataRequired()])
    Addproduct = SubmitField(label='Add Product')

class BagData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name_product = db.Column(db.String(length=30), nullable=False, unique=True)
    image_url_product = db.Column(db.String(length=200), nullable=True)
    price_product = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

class BagForm(FlaskForm):
    name_product = StringField(label='Product Name')
    image_url_product = StringField(label='Image URL', validators=[DataRequired()])
    product_price = StringField(label='Product Price', validators=[DataRequired()])
    submit = SubmitField(label='Add To Bag')


class SearchForm(FlaskForm):
    sensitive_skin = BooleanField('Suitable for sensitive skin')
    oily_skin = BooleanField('Suitable for Oily skin')
    combination_skin = BooleanField('Suitable for Combination skin')
    dry_skin = BooleanField('Suitable for dry skin')
    normal_skin = BooleanField('Suitable for normal skin')
    product_name = StringField(label='Product Name', validators=[Length(max=30)])
    product_brand = StringField(label='Product Brand', validators=[Length(max=20)])
    product_category = StringField(label='Product Category', validators=[Length(max=20)])
    submit = SubmitField('Search')
    save = SubmitField('Save Selected Products')


class Saveproduct(FlaskForm):
    product_name = StringField('Product Name', validators=[DataRequired()])
    product_brand = StringField('Brand', validators=[DataRequired()])
    product_price = StringField('Price', validators=[DataRequired()])
    product_rank = StringField('Rank', validators=[DataRequired()])
    submit_product = SubmitField('Save Product')


@app.route('/Register', methods=['GET', 'POST'])
def register_page():

    emailform()

    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = Users(
            name_user=form.username.data,
            email_address_user=form.email_address.data,
            password=form.password1.data,
            retype_password=form.password2.data
        )
        db.session.add(user_to_create)
        db.session.commit()
        return redirect(url_for('market_page'))
    
    if form.errors:
        for err_msg in form.errors.values():
            flash(f'There was an error with creating an account: {err_msg}', category='danger')
    return render_template('registration_page.html', form=form,email_form=EmailForm())


    

#function for email subscription
def emailform():
    email_form = EmailForm()
    if email_form.validate_on_submit():
        email_add = UsersEmail(
            email_address_user=email_form.email.data
        )
        db.session.add(email_add)
        db.session.commit()
        flash('Thanks for subscribing to our Cosmetics website', category='success')
    else:
        flash('Sorry, something went wrong with the subscription, Please try again later', category='danger')


@app.route('/market', methods=['GET', 'POST'])
def market_page():

    emailform()
    search = request.args.get('search', '')
    items = Item.query.filter(Item.name_product.like(f'%{search}%')).all() if search else Item.query.all()
    categories = Category.query.all()
    return render_template('market.html', items=items, categories=categories,email_form=EmailForm())


@app.route('/productdisplay', methods=['GET','POST'])
def product_display():

    products = Product.query.all()
    return render_template('products_cosmitics.html',products=products )




@app.route('/product/<int:product_id>', methods=['GET', 'POST'])
def product_details(product_id):
    product = Item.query.get_or_404(product_id)
    category = Category.query.get_or_404(product.category_id)
    categories = Category.query.all()
    search = request.args.get('search', '')
    items = Item.query.filter(Item.name_product.like(f'%{search}%')).all() if search else Item.query.all()

    form = BagForm()
    if form.validate_on_submit():
        product_to_create = BagData(
            name_product=form.name_product.data,
            image_url_product=form.image_url_product.data,
            price_product=form.product_price.data,
            user_id=current_user.id
        )
        db.session.add(product_to_create)
        db.session.commit()
        flash('Successfully added to Bag', category='success')

        return redirect(url_for('product_details', product_id=product_id))  # Redirect to avoid form resubmission
    elif request.method == 'POST':
        print(form.errors)  # Debug form errors
        flash('Something went wrong, please try again.', category='danger')
    #elif BagData == form :


    return render_template('product1.html', product=product, category=category, categories=categories, items=items, form=form)


@app.route('/SignIn', methods=['GET', 'POST'])
def sign_in_page():
    form = SignInForm()
    if form.validate_on_submit():
        attempted_user = Users.query.filter_by(name_user=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            login_user(attempted_user)
            flash(f'Success! You are logged in as: {attempted_user.name_user}', category='success')
            return redirect(url_for('market_page'))
        else:
            flash('Username and password do not match! Please try again', category='warning')
    return render_template('log_in_page.html', form=form)

@app.route('/Dashboard')
@login_required
def dashboard_page():
    products = Item.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', products=products)

@app.route('/AddProduct', methods=['GET', 'POST'])
@login_required
def add_product_page():
    form = AddProductForm()
    if form.validate_on_submit():
        product_to_create = Item(
            name_product=form.name_product.data,
            image_url_product=form.image_url_product.data,
            price_product=form.product_price.data,
            shipping_address_product=form.shipping_address.data,
            size_product=form.size_product.data,
            color_product=form.color_product.data,
            description_product=form.description_product.data,
            category_id=form.categoryid.data,
            user_id=current_user.id
        )
        db.session.add(product_to_create)
        db.session.commit()
        return redirect(url_for('dashboard_page'))
    return render_template('add_product.html', form=form)


@app.route('/cart',methods=['GET','POST'])
@login_required
def cart_page():
    user_bag_items = BagData.query.filter_by(user_id=current_user.id).all()
    if not user_bag_items:
        flash('Your bag is empty.', category='info')
        return redirect(url_for('market_page'))

    return render_template('shopping_bag.html', bag_products=user_bag_items)

#favorite page for products
@app.route('/favorites')
@login_required
def favorites_products():

    return render_template('favorites_products.html')


@app.route('/')
def official_page():
    categories = Category.query.all()
    items = Item.query.all()

    return render_template('Home_page.html',categories=categories,items=items)




@app.route('/category/<int:category_id>')
def category_page(category_id):
    emailform()
    category = Category.query.get_or_404(category_id)
    items = Item.query.filter_by(category_id=category_id).all()
    categorial = Category.query.all()
    categories = Category.query.all()
    
    return render_template('category.html', category=category, items=items,
                           categories=categories,email_form=EmailForm(),
                           categorial=categorial
                           )

#Button add to Bag
@app.route('/add_to_bag/<int:product_id>', methods=['POST'])
@login_required
def add_to_bag(product_id):
    product = Item.query.get_or_404(product_id)
    user_bag = current_user.bag

    
    if not user_bag:
        user_bag = Bag(user_id=current_user.id)
        db.session.add(user_bag)
        db.session.commit()

    bag_product = BagProduct.query.filter_by(bag_id=user_bag.id, product_id=product.id).first()

    if bag_product:
        bag_product.quantity += 1
    else:
        bag_product = BagProduct(
            bag_id=user_bag.id,
            product_id=product.id,
            quantity=1,
            price=product.price_product,
            image_url=product.image_url_product
        )
        db.session.add(bag_product)
    
    db.session.commit()
    flash(f'Added {product.name_product} to your bag.', category='success')
    return redirect(url_for('market_page'))


@app.route('/delete_bag_product/<int:product_id>', methods=['GET','POST'])
@login_required
def delete_bag_product(product_id):
    product = BagData.query.get_or_404(product_id)
    if product.user_id != current_user.id:
        flash('You do not have permission to delete this product.', category='danger')
        return redirect(url_for('cart_page'))

    try:
        db.session.delete(product)
        db.session.commit()
        flash('The product has been removed successfully', category='success')
    except Exception as e:
        print(str(e))  # Optional: Print the error for debugging purposes
        flash('There was a problem deleting that product, please try again later', category='danger')

    return redirect(url_for('cart_page'))


@app.route('/modify_product/<int:product_id>', methods=['GET'])
@login_required
def modify_item(product_id):
    try:
        product = Item.query.get(product_id)
        if product:
            categories = Category.query.all() 
            return render_template('modify_product.html', product=product, categories=categories)
        else:
            flash('Item not found', category='danger')
            return redirect(url_for('dashboard_page'))  
    except Exception as e:
        print(f"Error fetching item details: {e}")
        flash('There was a problem loading item details', category='danger')
        return redirect(url_for('dashboard_page'))  
    


@app.route('/update_product/<int:product_id>', methods=['POST'])
@login_required
def update_item(product_id):
    try:
        product = Item.query.get(product_id)
        if product:
            product.name_product = request.form['name_product']
            product.image_url_product = request.form['image_url_product']
            product.price_product = request.form['price_product']
            product.shipping_address_product = request.form['shipping_address_product']
            product.size_product = request.form['size_product']
            product.color_product = request.form['color_product']
            product.description_product = request.form['description_product']
            product.category_id = request.form['category_id']


            validate_csrf(request.form.get('csrf_token'))
            db.session.commit()
            flash('Item updated successfully', category='success')
        else:
            flash('Item not found', category='danger')
    except Exception as e:
        print(f"Error updating item: {e}")
        flash('There was a problem updating the item', category='danger')

    return redirect(url_for('dashboard_page')) 






#Delete button from Dashboard Page
@app.route('/delete_product/<int:product_id>')
@login_required
def delete_product(product_id):
    product = Item.query.get_or_404(product_id)
    try:
        db.session.delete(product)
        db.session.commit()
        flash('The product has been removed successfully', category='danger')
        return redirect('/Dashboard')

    except:
        flash('There was a problem deleting that product please try again later', category='danger')
    




@app.route('/logout')
def logout_page():
    logout_user()
    flash('You have been logged out', category='info')
    return redirect(url_for('market_page'))

#about_us page
@app.route('/about')
def about_page():

    return render_template('about_us.html')

#accessiblity page
@app.route('/accessibility')
def accessibility_page():

    return render_template('Accessibility.html')

#Current promotoin page
@app.route('/promotions')
def promotions_page():

    return render_template('CurrentPromotions.html')

#FAQ page
@app.route('/FAQ')
def faq_page():

    return render_template('FAQs.html')

#Orders & Payments page
@app.route('/Orders&Payments')
def orders_payments():

    return render_template('Orders&Payments.html')

#Privacy page
@app.route('/Privacy')
def privacy_page():

    return render_template('privacy.html')

#TERMS -CONDITIONS page
@app.route('/terms')
def terms_conditions():

    return render_template('TERMSCONDITIONS.html')

#Returns page
@app.route('/Returns')
def returns_page():

    return render_template('Returns.html')

#Shipping page
@app.route('/Shipping')
def shipping_page():

    return render_template('Shipping.html')


if __name__ == '__main__':
    app.run(debug=True)





