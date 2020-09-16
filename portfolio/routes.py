from flask import render_template, url_for, flash, redirect, request
from portfolio import app, db, bcrypt
from portfolio.forms import RegistrationForm, LoginForm
from portfolio.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required

posts = [
    {
        'author': 'Corey Schafer',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'April 21, 2018'
    }
]

# tells the application which URL should call the associated function. 
@app.route("/")
@app.route("/home")
def home():
    return render_template('index.html')



@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm() # store register form data
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/account")
@login_required
def account():
    return render_template('account.html', title='Account')


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/blog ")
def blog():
    return render_template('blog.html', posts=posts)

@app.route('/experience')
def experience():
    return render_template('experience.html')

@app.route('/portfolio')
def portfolio():
    return render_template('portfolio.html')

@app.route('/education')
def education():
    return render_template('education.html')

@app.route('/achievements')
def achievements():
    return render_template('achievements.html')
