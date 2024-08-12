from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO, ConnectionRefusedError
from flask_login import LoginManager, UserMixin, login_user, current_user, login_required, logout_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

login_manager = LoginManager()
login_manager.init_app(app)

users = {'a@a.a': {'password': 'a'}}  

class User(UserMixin):
    pass

@login_manager.user_loader  
def user_loader(email):  
    """  
 設置二： 透過這邊的設置讓flask_login可以隨時取到目前的使用者id   
 :param email:官網此例將email當id使用，賦值給予user.id    
 """   
    if email not in users:  
        return  
  
    user = User()  
    user.id = email  
    return user  

@login_manager.unauthorized_handler
def unauthorized_callback():
    print("request.path", request.path)
    return redirect(url_for("login"))
    # return redirect('/login?next=' + request.path)

@app.route('/login', methods=['GET', 'POST'])  
def login():  
    """  
 官網git很給力的寫了一個login的頁面，在GET的時候回傳渲染     
 """   
    if request.method == 'GET':  
           return '''
     <form action='login' method='POST'>
     <input type='text' name='email' id='email' placeholder='email'/>
     <input type='password' name='password' id='password' placeholder='password'/>
     <input type='submit' name='submit'/>
     </form>
                  '''

    email = request.form['email']  
    if request.form['password'] == users.get(email, {"password":""})['password']:  
        #  實作User類別  
        user = User()  
        #  設置id就是email  
        user.id = email  
        #  這邊，透過login_user來記錄user_id，如下了解程式碼的login_user說明。  
        login_user(user)  
        #  登入成功，轉址  
        return redirect(url_for('index'))  
    
    return 'Bad login' 

@app.route('/logout')  
def logout():  
    """  
 logout\_user會將所有的相關session資訊給pop掉 
 """ 
    logout_user()  
    return 'Logged out'  

@app.route('/')
def index():
    return redirect(url_for("counter"))

@app.route('/counter')
# @login_required
def counter():
    return render_template("counter.html")

@app.route('/test')
def test():
    return render_template("test.html")


@socketio.on('connect')
def connect():
    print("\n",request)
    print("\n",request.sid)
    print("\n",request.args)
    if not current_user.is_authenticated:
        raise ConnectionRefusedError('unauthorized!')
    
    print("connected")
    socketio.emit('sync_game_status', {
    "matchLevel":"practice",
    "matchNumber": 555,
    "matchStatus": "started",
    "alliance": "blue",
    "team1": "435t-2",
    "team2": 12
})

@socketio.on('message')
def handle_message(data):
    print('received message: ' + data)

if __name__ == '__main__':
    app.debug = True
    socketio.run(app, host='0.0.0.0', port=5000)