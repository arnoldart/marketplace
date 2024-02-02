from flask import render_template, request, redirect, url_for, flash, session
from app import app 

@app.route('/home', methods=['GET', 'POST'])
def home():
  return render_template('index.html')

@app.route('/detail', methods=['GET', 'POST'])
def detail():
  return render_template('detail.html')

