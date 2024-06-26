from flask import Flask, flash, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from wtforms import StringField, PasswordField, SubmitField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length, Email, EqualTo
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user, logout_user
from flask_wtf import CSRFProtect

app = Flask(__name__)
csrf = CSRFProtect(app)
app.app_context().push()



app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

app.config['SECRET_KEY'] = 'rZ5£2V1$~Wty'

db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = "sign_in_page"
login_manager.login_message_category = "info"

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))



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
    bag = db.relationship('Bag', uselist=False, backref='user')  # One-to-one relationship

    
class RegisterForm(FlaskForm):
    username = StringField(label='Username', validators=[Length(min=4, max=30), DataRequired()])
    email_address = StringField(label='Email', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='Password', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label='Confirm Password', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Create An Account')

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


@app.route('/Register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = Users(
            name_user=form.username.data,
            email_address_user=form.email_address.data,
            password_user=form.password1.data,
            retype_password_user=form.password2.data
        )
        db.session.add(user_to_create)
        db.session.commit()
        return redirect(url_for('market_page'))
    
    if form.errors:
        for err_msg in form.errors.values():
            flash(f'There was an error with creating an account: {err_msg}', category='danger')
    return render_template('registration_page.html', form=form)


@app.route('/market')
def market_page():
    search = request.args.get('search', '')
    items = Item.query.filter(Item.name_product.like(f'%{search}%')).all() if search else Item.query.all()

    
    categories = Category.query.all()
    return render_template('market.html', items=items, categories=categories)

@app.route('/product/<int:product_id>')
def product_details(product_id):
    product = Item.query.get_or_404(product_id)
    category = Category.query.get_or_404(product.category_id)
    categories = Category.query.all()
    search = request.args.get('search', '')
    items = Item.query.filter(Item.name_product.like(f'%{search}%')).all() if search else Item.query.all()

    return render_template('product1.html', product=product, category=category, categories=categories, items=items)



@app.route('/SignIn', methods=['GET', 'POST'])
def sign_in_page():
    form = SignInForm()
    if form.validate_on_submit():
        attempted_user = Users.query.filter_by(name_user=form.username.data).first()
        if attempted_user and attempted_user.password_user == form.password.data:
            login_user(attempted_user)
            flash(f'Success! You are logged in as: {attempted_user.name_user}', category='success')
            return redirect(url_for('market_page'))
        else:
            flash('Username and password do not match! Please try again', category='danger')
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


@app.route('/cart')
@login_required
def cart_page():
    user_bag = current_user.bag
    if not user_bag:
        flash('Your bag is empty.', category='info')
        return redirect(url_for('market_page'))

    bag_products = BagProduct.query.filter_by(bag_id=user_bag.id).all()
    return render_template('shopping_bag.html', bag_products=bag_products)



@app.route('/')
def official_page():
    categories = Category.query.all()
    return render_template('Home_page.html',categories=categories)

@app.route('/category/<int:category_id>')
def category_page(category_id):
    category = Category.query.get_or_404(category_id)
    items = Item.query.filter_by(category_id=category_id).all()
    
    return render_template('category.html', category=category, items=items)



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


@app.route('/addtobag_product/<int:product_id>')
@login_required
def bag_product(product_id):
    product = Item.query.get_or_404(product_id)
    try:
        db.session.add(product)
        db.session.commit()
        return redirect('/Dashboard')

    except:
        return ('There was a problem deleting that product please try again later')



@app.route('/delete_product/<int:product_id>')
@login_required
def delete_product(product_id):
    product = Item.query.get_or_404(product_id)
    try:
        db.session.delete(product)
        db.session.commit()
        return redirect('/Dashboard')

    except:
        return ('There was a problem deleting that product please try again later')
    

@app.route('/modify_product/<int:product_id>',methods=['GET', 'POST'])
@login_required
def modify_product(product_id):
    form = AddProductForm()
    product_to_modify = Item.query.get_or_404(product_id)
    if request.method == 'POST':
        product_to_modify.name = request.form['']



@app.route('/logout')
def logout_page():
    logout_user()
    flash('You have been logged out', category='info')
    return redirect(url_for('market_page'))

if __name__ == '__main__':
    app.run(debug=True)
