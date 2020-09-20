from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from portfolio import db
from portfolio.models import Post
from portfolio.posts.forms import PostForm

# create Blueprint for create, view, update, delete post
posts = Blueprint('posts', __name__)

# url path to create new post (form)
@posts.route("/post/new", methods=['GET','POST'])
@login_required # must be logged in
def new_post():
    form = PostForm() # initialise form class
    if form.validate_on_submit(): # check if form submitted
        # pass form data into database class post
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post) # add post data to database
        db.session.commit() # submit changes
        flash('Your post has been created!', 'success') # display success message
        return redirect(url_for('main.blog')) # redirect user to blog page
    # display create post page and pass form data , and legend title
    return render_template('util_pages/create_post.html', form=form, legend='New Post')

# url path to different user's post
@posts.route("/post/<int:post_id>") # post_id must be int
def post(post_id): # takes user's post id as parameter
    post = Post.query.get_or_404(post_id) # search if post exist or display 404 error page
    # display user post page and pass post data 
    return render_template('main_pages/post.html', post=post)

# url path to user post to update (form)
@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required # must be logged in
def update_post(post_id):
    post = Post.query.get_or_404(post_id) # search if post exist or display 404 error page
    # if post author and current user doesnt match display 403 error page
    if post.author != current_user: 
        abort(403)
    form = PostForm() # initialise form class
    if form.validate_on_submit(): # check if form submitted
        post.title = form.title.data # store form title input in database
        post.content = form.content.data # store form content input in database
        db.session.commit() # submit changes
        flash('Your post has been updated!', 'success') # display success message
        # redirect user to post method and pass post id to template
        return redirect(url_for('posts.post', post_id=post.id)) 
    elif request.method == 'GET': # check if GET request
        form.title.data = post.title # fill post title field with title data
        form.content.data = post.content # fill post cotnent field with content data
    # display create post page and pass form data , and legend title
    return render_template('util_pages/create_post.html', form=form, legend='Update Post')

# url path to delete a post 
@posts.route("/post/<int:post_id>/delete", methods=['POST']) 
@login_required # must be logged in 
def delete_post(post_id):
    post = Post.query.get_or_404(post_id) # search if post exist or display 404 error page 
    if post.author != current_user: # check if post author not current user
        abort(403) # display 403 error page
    db.session.delete(post) # remove post from database
    db.session.commit() # submit changes
    flash('Your post has been deleted!', 'danger') # display danger message
    return redirect(url_for('main.blog')) # redirect to blog page 