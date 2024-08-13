from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO, emit, join_room, leave_room, ConnectionRefusedError
from flask_login import LoginManager, UserMixin, login_user, current_user, login_required, logout_user
from threading import Timer
from module.match import Match
from module.db_operator import DBOperator

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

login_manager = LoginManager()
login_manager.init_app(app)

match = Match()

db = DBOperator()

# users = {
#     'admin': {
#         'password': 'admin',
#         'role': '0',
#         'alliance': 'admin'
#     },
#     'r1': {
#         'password': '1',
#         'role': '1',
#         'alliance': 'red'
#     },
#     'r2': {
#         'password': '1',
#         'role': '1',
#         'alliance': 'red'
#     },
#     'b1': {
#         'password': '1',
#         'role': '1',
#         'alliance': 'blue'
#     },
#     'b2': {
#         'password': '1',
#         'role': '1',
#         'alliance': 'blue'
#     }
# }


class User(UserMixin):
    pass


@login_manager.user_loader
def user_loader(username):
    """  
 設置二： 透過這邊的設置讓flask_login可以隨時取到目前的使用者id   
 :param email:官網此例將email當id使用，賦值給予user.id    
 """
    usernames = db.get_all_username()
    if not username in usernames:
        return None
    print("user_loader", username)

    user_info = db.get_user(username)

    user = User()
    user.id = user_info[1]
    user.role = user_info[3]
    user.alliance = user_info[4]

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

    username = request.form['account']
    password = request.form['password']

    result = db.login_query(username, password)
    if not result:
        return render_template('login.html', wrong_account_or_password=True)

    #  實作User類別
    user = User()
    user.id = result[0][1]
    user.role = result[0][3]
    user.alliance = result[0][4]

    login_user(user)

    return redirect(url_for('index'))


@app.route('/logout')
def logout():
    """  
 logout\_user會將所有的相關session資訊給pop掉 
 """
    logout_user()
    # return 'Logged out'
    return redirect(url_for('index'))


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


@app.route('/simpleManagement')
def simpleManagement():
    print(db.get_matches_info())
    return render_template("simpleManagement.html", matches_info=db.get_matches_info())


@app.route('/management')
def control():
    if int(current_user.role) > 0:
        return "", 403
    return render_template("management.html")


@app.route('/test')
def test():
    return render_template("login copy.html")
    # return render_template("test2.html")


@app.route('/test2')
def test2():
    return render_template("test2.html")


def sync_match_info(alliance):
    socketio.emit('sync_match_info', {
        "matchLevel": match.level,
        "matchNumber": match.id,
        "matchState": match.state,
        "alliance": alliance,
        "team1": match.alliance[alliance].team1,
        "team2": match.alliance[alliance].team2,
    }, to=alliance)


@socketio.on('connect')
def connect():
    if not current_user.is_authenticated:
        raise ConnectionRefusedError('unauthorized!')

    print("connected")
    join_room(current_user.alliance)
    # sync_match_info(current_user.alliance)
    emit('sync_match_info', {
        "matchLevel": match.level,
        "matchNumber": match.id,
        "matchState": match.state,
        "alliance": current_user.alliance,
        "team1": match.alliance[current_user.alliance].team1,
        "team2": match.alliance[current_user.alliance].team2,
    })


@socketio.on('update_score')
def update_score(data):
    emit('update_score', data, to=current_user.alliance)
    # print('received message: ' + data)
    print("send to alliance: ", current_user.alliance)


@socketio.on('update_selection')
def update_selection(data):
    emit('update_selection', data, to=current_user.alliance)
    print("send to alliance: ", current_user.alliance)
    print(data)


@socketio.on('load_match', namespace='/management')
def load_match(data):
    match_data = db.load_match_data(data["level"], data["id"])
    match.loadMatch(match_data)
    match.state = "preparing"
    sync_match_info("red")
    sync_match_info("blue")


@socketio.on('start_match', namespace='/management')
def start_match(data):
    if match.state != "preparing":
        return
    if data.level != match.level or data.id != match.id:
        return
    match.state = "started"
    emit('match_start', brocast=True)
    emit('match_start', namespace='/management')
    global gameTimer
    gameTimer = Timer(10, end_match)
    gameTimer.start()


@socketio.on('stop_match', namespace='/management')
def stop_match(data):
    gameTimer.cancel()
    end_match()


def end_match(interrupted=False):
    match.state = "ended"
    socketio.emit('match_end')
    socketio.emit('match_end', namespace='/management')
    # Todo: save match data to database
    match.reset()


if __name__ == '__main__':
    app.debug = True
    socketio.run(app, host='0.0.0.0', port=5000)
