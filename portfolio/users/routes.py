from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from portfolio import db, bcrypt
from portfolio.models import User, Post
from portfolio.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                                   RequestResetForm, ResetPasswordForm)
from portfolio.users.utils import save_picture, send_reset_email

# Create Blueprint to register, login, logout, account management,
# check other user's post and reset user's password
users = Blueprint('users', __name__)

# url path to register user (form)
@users.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated: # check if user user already signed in
        return redirect(url_for('main.home')) # redirect user to home page
    form = RegistrationForm() # initialise form class
    if form.validate_on_submit(): # check if form submitted
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8') # hash the password 
        # store username, email, password into user database
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user) # add user to database
        db.session.commit() # submit changes
        flash('Your account has been created! You are now able to log in', 'success') # display success message
        return redirect(url_for('users.login')) # redirect user to login
    # display register page and pass form data 
    return render_template('main_pages/register.html', form=form) 

# url path to login user (form)
@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated: # check if user user already signed in
        return redirect(url_for('main.home')) # redirect user to home page
    form = LoginForm() # initialise form class
    if form.validate_on_submit(): # check if form submitted
        user = User.query.filter_by(username=form.username.data).first() # search first user with same username
        if user and bcrypt.check_password_hash(user.password, form.password.data): # check is password matches password hash
            login_user(user, remember=form.remember.data) # start user session, check if remeber is true/false
            next_page = request.args.get('next') # store recent page on
            # redirect to current page otherwise redirect to home page
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger') # display danger message
    # display login page and pass form data 
    return render_template('main_pages/login.html', form=form)

# url path to logout user (form)
@users.route("/logout")
def logout():
    logout_user() # end user session
    return redirect(url_for('users.login')) # redirect user to login page

# url path to user's account
@users.route("/account", methods=['GET', 'POST'])
@login_required # must be logged in
def account():
    form = UpdateAccountForm() # initialise form class
    if form.validate_on_submit(): # check if form submitted
        if form.picture.data: # check if picture uploaded
            picture_file = save_picture(form.picture.data) # store picture 
            current_user.image_file = picture_file # change user's profile image to new image
        current_user.username = form.username.data # update username
        current_user.email = form.email.data # update email
        db.session.commit() # submit changes
        flash('Your account has been updated!', 'success') # display success message
        return redirect(url_for('users.account')) # redirect to account page
    elif request.method == 'GET': # check if GET request
        form.username.data = current_user.username # fill field with current username
        form.email.data = current_user.email # fill field with current email
    # get profile pic from profile_pics folder 
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file) 
    # display account page and pass form data and profile image
    return render_template('main_pages/account.html', image_file=image_file, form=form)

# url path to other user's account
@users.route("/user/<string:username>")
def user_posts(username):
    # get current page number , default page set to 1, and are integers
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404() # search if username exist or display 404 error page
    # sort posts in decending order by that user with 5 post per page
    posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5) 
    # display other user's post and pass post data and user data
    return render_template('util_pages/user_posts.html', posts=posts, user=user)

# url path to reset password
@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated: # check if user is signed in
        return redirect(url_for('main.home')) # redirect user to home page
    form = RequestResetForm() # initialise from class
    if form.validate_on_submit(): # check if form submitted
        user = User.query.filter_by(email=form.email.data).first() # search if email in database
        send_reset_email(user) # send reset email request to user
        flash('An email has been sent with instructions to reset your password.', 'info') # display info message
        return redirect(url_for('users.login')) # redirect to login page 
    # display reset password page and pass form data
    return render_template('util_pages/reset_request.html', form=form)

# url path to reset password with expiry token
@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated: # check if user is signed in
        return redirect(url_for('main.home')) # redirect user to home page
    user = User.verify_reset_token(token) # verify user
    if user is None: # check if false
        flash('That is an invalid or expired token', 'warning') # display warning message
        return redirect(url_for('users.reset_request')) # redirect user to reset password page
    form = ResetPasswordForm() # initialise form class
    if form.validate_on_submit(): # check if form submitted  
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8') # hash password 
        user.password = hashed_password # store hash password 
        db.session.commit() # submit changes 
        flash('Your password has been updated! You are now able to log in', 'success') # display success message
        return redirect(url_for('users.login')) # redirect user to login page
    # display reset password page and pass form data
    return render_template('util_pages/reset_token.html', form=form) 