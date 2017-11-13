from flask import Flask, request, make_response, redirect, abort, render_template
from flask_bootstrap import Bootstrap
from flask_script import Manager, Server

app = Flask(__name__)
manager = Manager(app)
manager.add_command("runserver",Server(host="localhost",port=8888,use_debugger=True))
app.config['BOOTSTRAP_SERVE_LOCAL']=True
bootstrap = Bootstrap(app)


@app.route('/')
def index():
    return "<h1>hello world</h1>"


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



if __name__ == '__main__':
    app.run()