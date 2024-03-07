import pathlib

from flask import render_template, request, url_for, redirect, flash
from flask_login import login_user, login_required, logout_user
from spire.pdf.common import *
from spire.pdf import *

from watchlist import app
from watchlist.models import User

@app.route('/')
def index(): # 首页：①首页展示
    return render_template('index.html')

@app.route('/build', methods=['GET', 'POST'])
def build(): # 建卡：①建卡页面展示。②提交建卡信息。
    return render_template('build.html')

@app.route('/store')
@login_required
def store(): # 卡库：①仓库页面展示。
    return render_template('store.html')

@app.route('/card_lom_1')
@login_required
def card_lom_1():
    return render_template('card_lom_1.html')

@app.route('/rbook_lom_1')
def rbook_lom_1():
    if(pathlib.Path("./watchlist/static/rbook_lom_1/0.html").exists() != True):
        doc = PdfDocument()
        doc.LoadFromFile('./watchlist/static/rbook_lom_1/0.pdf')
        doc.SaveToFile('./watchlist/static/rbook_lom_1/0.html', FileFormat.HTML)
        doc.Clone()
    html = open('./watchlist/templates/test.html', 'r', encoding='utf-8').read()
    return render_template('rbook_lom_1.html', html=html)


@app.route('/user')
@login_required
def user(): # 用户：①用户信息展示。
    return render_template('user.html')

@app.route('/login', methods=['GET', 'POST'])
def login(): # 登录：①用户名、密码登录。②查看登录页面。
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            flash('空的用户名或密码')
            return redirect(url_for('login'))

        user = User.query.first()

        if username == user.username and user.validate_password(password):
            login_user(user)
            flash('登陆成功')
            return redirect(url_for('index'))

        flash('错误的用户名或密码')
        return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout(): # 登出：①登出。
    logout_user()
    flash('登出成功')
    return redirect(url_for('index'))