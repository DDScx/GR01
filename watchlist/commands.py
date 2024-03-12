import click

from watchlist import app, db
from watchlist.models import User


@app.cli.command()
@click.option('--drop', is_flag=True, help='Create after drop.')
def initdb(drop):  # 初始化数据库
    if drop:
        db.drop_all()
        click.echo('删除数据库')
    db.create_all()
    click.echo('建立数据库')


@app.cli.command()
@click.option('--username', prompt=True, help='用户名，可以理解为账号，不是昵称')
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help='密码')
def adduser(username, password):  # 创建用户
    db.create_all()

    user = User.query.first()
    if user is not None:
        click.echo('更新用户信息中...')
        user.username = username
        user.set_password(password)
    else:
        click.echo('创建用户信息中...')
        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
    db.session.commit()

    user = User.query.first()
    if user.nickname is not None:
        click.echo('用户名：' + user.nickname + ' 已完成更新')
    else:
        user.nickname = '新用户' + str(user.id)
        click.echo('新用户：' + user.nickname + ' 已完成创建')
        db.session.add(user)
        db.session.commit()
