from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO, join_room, leave_room, ConnectionRefusedError
from flask_login import LoginManager, UserMixin, login_user, current_user, login_required, logout_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

login_manager = LoginManager()
login_manager.init_app(app)

users = {
    'admin': {
        'password': 'admin',
        'role': '0',
        'alliance': 'admin'
        },
    'r1': {
        'password': '1',
        'role': '1',
        'alliance': 'red'
        },
    'r2': {
        'password': '1',
        'role': '1',
        'alliance': 'red'
        },
    'b1': {
        'password': '1',
        'role': '1',
        'alliance': 'blue'
        },
    'b2': {
        'password': '1',
        'role': '1',
        'alliance': 'blue'
        }
    }  

class User(UserMixin):
    pass

@login_manager.user_loader  
def user_loader(account):  
    """  
 設置二： 透過這邊的設置讓flask_login可以隨時取到目前的使用者id   
 :param email:官網此例將email當id使用，賦值給予user.id    
 """   
  
    user = User()  
    user.id = account
    user.role = users[account]['role']
    user.alliance = users[account]['alliance']

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
           return render_template('login.html')

    account = request.form['account']
    password = request.form['password']

    if account not in users:  
        return render_template('login.html', wrong_account=True)

    if password == users[account]['password']:  
        #  實作User類別  
        user = User()  
        #  設置id就是email  
        user.id = account  
        #  這邊，透過login_user來記錄user_id，如下了解程式碼的login_user說明。  
        login_user(user)  
        #  登入成功，轉址  
        return redirect(url_for('index'))  
    
    return render_template('login.html', wrong_password=True)

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
@login_required
def counter():
    return render_template("counter.html")

@app.route('/scoreboard')
def scoreboard():
    return render_template("scoreboard.html")

@app.route('/control')
def control():
    if int(current_user.role) > 0:
        return "", 403
    return render_template("control.html")

@app.route('/test')
def test():
    return render_template("login copy.html")
    # return render_template("test2.html")
@app.route('/test2')
def test2():
    return render_template("test2.html")


@socketio.on('connect')
def connect():
    if not current_user.is_authenticated:
        raise ConnectionRefusedError('unauthorized!')
    
    print("connected")
    join_room(current_user.alliance)
    socketio.emit('sync_game_status', {
    "matchLevel":"practice",
    "matchNumber": 555,
    "matchStatus": "started",
    "alliance": current_user.alliance,
    "team1": "435t-2",
    "team2": 12
})

@socketio.on('update_score')
def update_score(data):
    socketio.emit('update_score', data, to=current_user.alliance)
    # print('received message: ' + data)
    print("send to alliance: ", current_user.alliance)

@socketio.on('update_selection')
def update_selection(data):
    socketio.emit('update_selection', data, to=current_user.alliance)
    print("send to alliance: ", current_user.alliance)
    print(data)

if __name__ == '__main__':
    app.debug = True
    socketio.run(app, host='0.0.0.0', port=5000)