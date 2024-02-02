from flask import render_template, request, redirect, url_for, flash, session
from app import app 
from utils.db_utils import verify_user, user_exists, create_user  # Sesuaikan dengan struktur folder dan nama proyek Anda

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form.get('username')
#         password = request.form.get('password')

#         if verify_user(username, password):
#             session['username'] = username
#             flash('Login successful!', 'success')
#             return redirect('login')
#         else:
#             flash('Invalid username or password. Please try again.', 'error')

#     return render_template('auth/login.html')

# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         username = request.form.get('username')
#         password = request.form.get('password')

#         if not user_exists(username):
#             create_user(username, password)
#             flash('Registration successful!', 'success')
#             return redirect(url_for('login'))
#         else:
#             flash('Username already exists. Please choose another username.', 'error')

#     return render_template('auth/register.html')

# @app.route('/logout')
# def logout():
#     session.pop('username', None)
#     flash('Logout successful!', 'success')
#     return redirect(url_for('home'))