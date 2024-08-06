from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from token_gen import generate_token
from img_gen import generate_random_image
from embed_token import embed_token_into_image
from save_image import save_image
from PIL import UnidentifiedImageError
from token_extraction import extract_token_from_image, binary_to_text, decode_base64
import io
from PIL import Image

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        image = request.files.get('image')

        user = User.query.filter_by(username=username).first()

        if user:
            expected_data_length = user.binary_len

            if image and image.filename != '':
                image_bytes = io.BytesIO(image.read())
                binary_data = extract_token_from_image(image_bytes, expected_data_length)
                base64_str = binary_to_text(binary_data)
                decoded_hash = decode_base64(base64_str)

                if check_password_hash(user.password, password):
                    if decoded_hash == decode_base64(user.token):
                        flash('Logged in successfully!', category='success')
                        login_user(user, remember=True)
                        return redirect(url_for('views.home'))
                    else:
                        flash('Incorrect picture, try again.', category='error')
                else:
                    flash('Incorrect password, try again.', category='error')
            else:
                flash('No image provided, please upload an image.', category='error')
        else:
            flash('User does not exist', category='error')
    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(username=username).first()

        token = generate_token(username, password1)

        image = generate_random_image(400, 400)
        image_path = save_image(image, username)
        print("Saving image at: ", image_path)

        image_with_token, binary_len = embed_token_into_image(image_path, token)
        output_path = save_image(image_with_token, username)
        print("Saving token image at: ", output_path)

        if user:
            flash('User already exists.', category='error')
        elif len(username) < 4:
            flash('Username must be at least 4 characters.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        else:
            new_user = User(username=username, password=generate_password_hash(password1), token=token, binary_len=binary_len)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))
    
    return render_template("register.html", user=current_user)