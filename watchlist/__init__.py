from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev'  # 密钥（测试）
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://gradmin:grpassword@localhost/grdb?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭对模型修改的监控

# 实例化
db = SQLAlchemy(app)
login_manager = LoginManager(app)


@login_manager.user_loader
def load_user(user_id):  # 用户加载回调函数，用户 ID 作为参数
    from watchlist.models import User
    user = User.query.get(int(user_id))
    return user


login_manager.login_view = 'login'


@app.context_processor
def inject_user():  # 模板共用参数-用户信息
    from watchlist.models import User
    user = User.query.first()
    return dict(user=user)


from watchlist import views, errors, commands
