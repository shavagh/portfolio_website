import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from portfolio import mail

# save user's profile picture
def save_picture(form_picture):
    random_hex = secrets.token_hex(8) # store generated 8 byte hex code
    _, f_ext = os.path.splitext(form_picture.filename) # get file extention of picture
    picture_fn = random_hex + f_ext # combine generated hex with file extention
    # join app root path, profile picture folder path and picture name to create path
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)
    output_size = (125, 125) # limit the profile picture size to 125
    i = Image.open(form_picture) # get user's profile picture
    i.thumbnail(output_size) # display user's profile picture
    i.save(picture_path) # save image in file path location
    return picture_fn # return image file name

# send email to reset passord
def send_reset_email(user):
    token = user.get_reset_token() # store reset token
    # create message with sender, recipients and content details
    msg = Message('Password Reset Request',sender='noreply@demo.com',  recipients=[user.email])
    # display message in email body with token
    msg.body = f'''To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}
If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg) # send email to user to details