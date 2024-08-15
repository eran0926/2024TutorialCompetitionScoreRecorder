from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO, emit, join_room, leave_room, Namespace, ConnectionRefusedError
from flask_login import LoginManager, UserMixin, login_user, current_user, login_required, logout_user
from threading import Timer
from module.match import Match, recorderIdToObjectNameTable
from module.db_operator import DBOperator
from module.utils import get_nested_attribute, set_nested_attribute
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

login_manager = LoginManager()
login_manager.init_app(app)

match = Match()

db = DBOperator()


debug_counter = 0


def debug_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        global debug_counter
        debug_counter += 1
        print("function", func.__name__, "called", debug_counter)
        re = func(*args, **kwargs)
        print("function", func.__name__, "end", debug_counter)
        return re
    return wrapper


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
    user_info = db.get_user(username)

    user = User()
    user.id = user_info[1]
    user.role = user_info[3]
    user.alliance = user_info[4]

    return user


@login_manager.unauthorized_handler
def unauthorized_callback():
    # return redirect(url_for("login"))
    print(request.path)
    return redirect('/login?next=' + request.path)


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

    # return redirect(url_for('index'))
    return redirect(request.args.get('next') or url_for('index'))


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/')
def index():
    return redirect(url_for("counter"))


@app.route('/counter')
@login_required
def counter():
    if int(current_user.role) != 1:
        return "", 403
    return render_template("counter.html", user={'id': current_user.id})


@app.route('/scoreboard')
def scoreboard():
    return render_template("scoreboard.html")


@app.route('/simpleManagement')
@login_required
def simpleManagement():
    if int(current_user.role) > 0:
        return "", 403
    return render_template("simpleManagement.html", matches_info=db.get_matches_info())


@app.route('/board')
def board():
    return render_template("board.html")


@app.route('/leaderboard')
def leaderboard():
    return render_template("leaderboard.html")


@app.route('/management')
def control():
    if int(current_user.role) > 0:
        return "", 403
    return render_template("management.html")


@app.route('/test')
def test():
    return render_template("result.html")


@app.route('/test2')
def test2():
    return render_template("test2.html")


def sync_counter_match_info(alliance):
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
    print("Connect------------------------------------------------------------------------------------------------------------------------------------------------------------------")

    join_room(current_user.alliance)
    if current_user.role == 1:
        match.recorder.add(request.sid)
    emit('sync_match_info', {
        "matchLevel": match.level,
        "matchNumber": match.id,
        "matchState": match.state,
        "alliance": current_user.alliance,
        "team1": match.alliance[current_user.alliance].team1,
        "team2": match.alliance[current_user.alliance].team2,
    })
    print("sync_match_info")
    print(match.get_all_recorder_data(current_user.alliance))
    emit('update_value', {
        "from": "host",
        "data": match.get_all_recorder_data(current_user.alliance)
    })


@socketio.on('disconnect')
def disconnect():
    if current_user.role == 1:
        match.recorder.remove(request.sid)
        if request.sid in match.commitedRecorder:
            match.commitedRecorder.remove(request.sid)


@socketio.on('update_value')
def update_score(msg):
    emit('update_value', msg, to=current_user.alliance)
    for data in msg["data"]:
        attr_name = current_user.alliance + "." + \
            recorderIdToObjectNameTable[data["id"]]
        set_nested_attribute(match, attr_name, data["value"])
    match.countScore()
    update_board_value(
        {"from": "host", "data": match.get_all_board_data()})
    print(match.red.score)


@socketio.on('commit')
def commit(msg):
    match.commitedRecorder.add(request.sid)
    if match.allCommited():
        match.state = "All Commited"
        db.change_match_state(match.level, match.id, match.state)
        socketio.emit('all_commited', {
                      "level": match.level, "id": match.id}, namespace='/management')
        return


class ManagementSocket(Namespace):
    def on_sync_match_state(self):
        emit('sync_match_state', match.state)

    def on_load_match(self, data):
        match.reset()
        match_data = db.load_match_data(data["level"], data["id"])
        match.loadMatch(match_data)
        match.state = "Preparing"
        db.change_match_state(match.level, match.id, match.state)
        db.reset_other_loaded_match_state(match.level, match.id)
        sync_counter_match_info("red")
        sync_counter_match_info("blue")
        sync_board_match_info()

    def on_start_match(self, data):
        global gameTimer
        if match.state != "Preparing":
            emit('wrong_state', 'Match is not in preparing state')
            print("wrong state")
            return
        if data["level"] != match.level or int(data["id"]) != match.id:
            emit('wrong_match', 'Match level or number is not correct')
            print("wrong match")
            print(data["level"], match.level, data["id"], match.id)
            return
        match.state = "Running"
        db.change_match_state(match.level, match.id, match.state)
        # emit('match_start', brocast=True)
        socketio.emit('match_start')
        socketio.emit('match_start', namespace='/management')
        socketio.emit('match_start', namespace='/board')
        gameTimer = Timer(151, self.end_match)
        # gameTimer = Timer(21, self.end_match)
        gameTimer.start()

    def on_interrupt_match(self, data):
        global gameTimer
        gameTimer.cancel()
        match.state = "Interrupted"
        db.change_match_state(match.level, match.id, match.state)
        socketio.emit('match_interrupted')
        socketio.emit('match_interrupted', {"level": match.level,
                                            "id": match.id}, namespace='/management')
        socketio.emit('match_interrupted', namespace='/board')
        match.reset()

    def end_match(self):
        match.state = "Ended"
        db.change_match_state(match.level, match.id, match.state)
        socketio.emit('match_end')
        socketio.emit('match_end', {"level": match.level,
                                    "id": match.id}, namespace='/management')

    def on_save_and_show(self, data):
        match.state = "Saved"
        db.change_match_state(match.level, match.id, match.state)
        # TODO: save match data to database
        match.end_match_settle()
        match_result = match.get_match_result()
        socketio.emit('reload')
        # socketio.emit('show_result', to="board")
        socketio.emit('show_result', match_result, to="board")
        tmp = match_result.copy()
        detail_data = match.get_detail_data()
        tmp.extend(detail_data)
        db.save_match_data(tmp)
        print("save and show")
        # print("\n\n\nsimulated save and show\n\n\n")


def sync_board_match_info():
    match_info = {
        "match-level": match.level,
        "match-number": match.id,
        "red-team1": match.alliance["red"].team1,
        "red-team2": match.alliance["red"].team2,
        "blue-team1": match.alliance["blue"].team1,
        "blue-team2": match.alliance["blue"].team2,
    }
    print("------\n\n------------------")
    socketio.emit('sync_match_info', match_info, namespace='/board')


def update_board_value(data):
    print("update_board_value")
    print(data)
    socketio.emit('update_value', data, namespace='/board')


class BoardSocket(Namespace):
    def on_connect(self):
        sync_board_match_info()
        update_board_value(
            {"from": "host", "data": match.get_all_board_data()})

    def on_sync_board_match_info(self):
        sync_board_match_info()


update_board_value
if __name__ == '__main__':
    app.debug = True
    socketio.on_namespace(ManagementSocket('/management'))
    socketio.on_namespace(BoardSocket('/board'))
    socketio.run(app, host='0.0.0.0', port=5000)
