import os
from flask import Flask, request, make_response, redirect, abort, render_template, session, url_for, flash
from flask_bootstrap import Bootstrap
from flask_script import Manager, Server
from flask_moment import Moment
from datetime import datetime
from Form import NameForm
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
# 跨站点请求伪造保护
app.config['SECRET_KEY'] = 'hard to guess string'
bootstrap = Bootstrap(app)
# 使用bootstrap
app.config['BOOTSTRAP_SERVE_LOCAL']=True
# 使用管理（代码可在控制台运行）
manager = Manager(app)
manager.add_command("runserver",Server(host="localhost",port=8888,use_debugger=True))
# 使用时间插件（便利而强大的时间功能）
moment = Moment(app)
# 设置数据库
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLAlchemy_DATABASE_URI']='mysql:\\\\'+'root:root@localhost:3306/test'
app.config['SQLALchemy_COMMIT_ON_TEARDOWN'] = True
db = SQLAlchemy(app)


# mysql的url格式
# mysql://username:password@hostname/database

@app.route('/',methods=['get','post'])
def index():
    myFrom = NameForm()
    if myFrom.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name!= myFrom.name.data:
            # 闪现消息
            flash('小样，你换了名字我就不认识你了？')
        session['name']=myFrom.name.data
        from test import User as uu
        users = uu.query.all()
        print(users)
        return redirect(url_for('index',_external=True))
    return render_template("index.html",
                           current_time=datetime.utcnow(),
                           form = myFrom)


@app.route("/user/<name>")
def index_name(name):
    if(name == 'honfeil'):
        # abort 抛出404
        abort(404)
    return render_template("user.html",
                           name = name)


@app.route("/agent")
def agent():
    # 获取request的头部数据
    agent = request.headers.get('user-agent')
    return "<h1>您的浏览器是：%s</h1>" % agent


@app.route("/400")
def badReq():
    response = make_response("<h1>Bad Request</h1>")
    # 添加cookie
    response.set_cookie("123","123")
    return response


@app.route("/redirect")
def redict_to_baidu():
    return redirect("http://www.baidu.com")


@app.errorhandler(404)
def no_page_found(e):
    return render_template("404.html")


@app.errorhandler(500)
def interl_server_error(e):
    return render_template("500.html")


if __name__ == '__main__':
    app.run(port=8888,debug=True)
    db.create_all()


class User(db.Model):
    __tablename__='my_user'
    user_id = db.Column(db.INTEGER,primary_key=True)
    user_name = db.Column(db.String,unique=True)
    user_pwd = db.Column(db.String)

    def __repr__(self):
        return '<User $r>' % self.user_name





