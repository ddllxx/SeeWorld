from flask import Flask, render_template, request, redirect, make_response
from flask_bootstrap import Bootstrap4
import login as lg
from login import formatDangerStr
import seeWorldDB as db
import json
import re

app = Flask(__name__)

boostrap = Bootstrap4(app)

#Use session to check for login
def haveLogin(session):
    # return True
    return session != None and lg.session_map.get(session) != None

#Check whether the password meets the format requirements
def detectPassword(str):
    if str == None or len(str) < 5:
        return False
    elif re.search('[0-9]+', str) == None or re.search('[A-Za-z]+', str) == None:
        return False
    return True

#Check that the registration meets all requirements
def checkRegister(name, password, sex, age, profession, nation, introduction):
    if len(name) == 0 or len(name) > 20:
        return "0 < the length of name <= 20"
    if sex != 'man' and sex != 'feman':
        return "Your must select the sex between man and feman"
    if int(age) <= 0 or int(age) > 200:
        return "Your age must bigger than 0 and less than 200"
    if len(profession) <= 0 or len(profession) > 20:
        return "0 < the length of the profession <= 20"
    if len(nation) <= 0 or len(nation) > 20:
        return "0 < the length of the nation <= 20"
    if not detectPassword(password):
        return "Your password(at least 5 characters) should be a mix of numbers and letters."
    return 'ok'

#Open the home page
@app.route('/')
def index():
    return render_template('index.html')

#Open the login page
@app.route('/loginPage')
def loginOrReginster():
    return render_template('login.html')

#Open the see page
@app.route('/see')
def see():
    session = request.cookies.get('session')
    if haveLogin(session):
        page = int(request.args['page'])
        type = request.args['type']
        if type == '':
            type = '0'
        return render_template('see.html', page = page, type=type)
    else:
        return render_template('error.html', message="please login first")

#Open the publishment detail page
@app.route('/detail')
def detail():
    session = request.cookies.get('session')
    if not haveLogin(session):
        return render_template('error.html', message='please login first')
    return render_template('detail.html', id = request.args['id'])

#Open the user page
@app.route('/user')
def user():
    session = request.cookies.get('session')
    if not haveLogin(session):
        return render_template('error.html', message='please login first')
    return render_template('user.html', id = lg.session_map[session][1])

#Open the publishment page
@app.route('/publish')
def publish():
    session = request.cookies.get('session')
    if not haveLogin(session):
        return render_template('error.html', message="please login first")
    return render_template('publish.html')

#Open the login page
@app.route('/login', methods=["POST"])
def login():
    req = request
    user = req.form['name']
    password = req.form['password']
    result = lg.login(user, password)
    if not result[0]:
        return render_template('error.html', message='user name or password error.')
    else:
        response = make_response(render_template('user.html', id=result[2]))
        response.set_cookie('session', result[1], max_age=3600)
        return response

#Open the error page
@app.route('/err')
def err():
    return render_template('error.html', message="error message")

# session isme
@app.route('/isMe')
def isMe():
    session = request.cookies.get('session')
    if haveLogin(session):
        id = lg.session_map[session][1]
        return '{"code": 1, "id":' + str(id) + '}'
    else:
        return '{"code": 0}'

#check not log in
@app.route('/user2')
def getUser():
    session = request.cookies.get('session')
    if not haveLogin(session):
        return render_template('error.html', message="please login first")
    else:
        id = request.args['id']
        return render_template('user2.html', id = id)

#User information
@app.route('/getUserInfo')
def getUserInfo():
    session = request.cookies.get('session')
    if not haveLogin(session):
        return '{"code" : 0}'
    else:
        id = request.args['id']
        ans = db.getUserInfo(id)
        if ans == None:
            return '{"code": 0}'
        user = {}
        user['code'] = 1
        user['id'] = ans[0]
        user['name'] = ans[1]
        user['sex'] = ans[3]
        user['age'] = ans[4]
        user['profession'] = ans[5]
        user['nation'] = ans[6]
        user['introduction'] = ans[7]
        return json.dumps(user)

# log out
@app.route('/logout')
def logOut():
    session = request.cookies.get('session')
    if haveLogin(session):
        lg.logout(session)
    respose = redirect('/')
    respose.delete_cookie('session')
    return respose

#Follow on the forums
@app.route('/getFocus')
def getFocus():
    session = request.cookies.get('session')
    if not haveLogin(session):
        return '{"code": 0}'
    else:
        id = request.args['id']
        data = db.getUserFocus(id)
        response = {}
        response['code'] = 1
        response['focus'] = list(data)
        return json.dumps(response)

#get all world
@app.route('/getAllWorld')
def getAllWorld():
    session = request.cookies.get('session')
    if not haveLogin(session):
        return '{"code": 0}'
    else:
        start = request.args['start']
        count = request.args['count']
        type = request.args['type']
        data = db.getAllWorld(start, count, type)
        response = {}
        response['code'] = 1
        response['message'] = list(data)
        for i, d in enumerate(response['message']):
            t = d[2].strftime("%Y-%m-%d %H:%M")
            response['message'][i] = list(d)
            response['message'][i][2] = t
        return json.dumps(response)

#get user world
@app.route('/getUserWorld')
def getUserWorld():
    session = request.cookies.get('session')
    if not haveLogin(session):
        return '{"code": 0}'
    else:
        id = request.args['id']
        data = db.getUserWorld(id)
        response = {}
        response['code'] = 1
        response['message'] = list(data)
        for i, d in enumerate(response['message']):
            t = d[0].strftime('%Y-%m-%d %H:%M')
            response['message'][i] = list(d)
            response['message'][i][0] = t
        return json.dumps(response)

#get the message
@app.route('/getMessage')
def getMessage():
    session = request.cookies.get('session')
    if not haveLogin(session):
        return '{"code": 0}'
    else:
        id = request.args['id']
        data = db.getMessage(id)
        data = list(data)
        response = {}
        response['code'] = 1
        response['message'] = data
        return json.dumps(response)

#get comment from other
@app.route('/getComment')
def getComment():
    session = request.cookies.get('session')
    if not haveLogin(session):
        return '{"code": 0}'
    else:
        id = request.args['id']
        data = db.getComment(id)
        data = list(data)
        response = {}
        response['code'] = 1
        response['comment'] = data
        for i, c in enumerate(response['comment']):
            t = c[4].strftime('%Y-%m-%d %H:%M')
            response['comment'][i] = list(c)
            response['comment'][i][4] = t
        return json.dumps(response)

#delete the comment
@app.route('/delComment')
def delComment():
    session = request.cookies.get('session')
    if not haveLogin(session):
        return '{"code": 0}'
    else:
        id = request.args['id']
        if len(id) == 0:
            return '{"code": 0}'
        db.delComment(id)


#comment information
@app.route('/comment')
def comment():
    session = request.cookies.get('session')
    if not haveLogin(session):
        return render_template('error.html', message="please login first")
    else:
        uid = lg.session_map[session][1]
        mid = request.args['id']
        content = request.args['comment']
        content = formatDangerStr(content)
        if len(content) == 0:
            return render_template('/error.html', message="comment should not be empty")
        db.addComment(uid, mid, content)
        return redirect('/detail?id='+mid)

#register information
@app.route('/register', methods=['POST'])
def register():
    name = request.form.get('name')
    password = request.form.get('password')
    sex = request.form.get('sex')
    age = request.form.get('age')
    profession = request.form.get('profession')
    nation = request.form.get('nation')
    introduction = request.form.get('introduction')
    name = formatDangerStr(name)
    password = formatDangerStr(password)
    sex = formatDangerStr(sex)
    age = formatDangerStr(age)
    profession = formatDangerStr(profession)
    nation = formatDangerStr(nation)
    introduction = formatDangerStr(introduction)
    check = checkRegister(name, password, sex, age, profession, nation, introduction)
    if check != 'ok':
        return render_template('error.html', message="register fail: " + check)
    if not db.register(name, password, sex, age, profession, nation, introduction):
        return render_template('error.html', message='The user name ' + request.form.get('name') + 'you have chosen is already cooupied, please try another username!')
    return render_template('success.html', message = 'Your registration has been successful! Please remeber your User Name : ' + request.form.get('name'))

#follow other information
@app.route('/follow')
def follow():
    session = request.cookies.get('session')
    if not haveLogin(session):
        return render_template('error.html', message="please login first")
    else:
        uid = lg.session_map[session][1]
        id = request.args['id']
        f = int(request.args['flag'])
        if f == 1:
            db.addFollow(uid, id)
        else:
            db.removeFollow(uid, id)
        return '{"code": 1}'

#focus the other
@app.route('/checkFocus')
def checkFocus():
    session = request.cookies.get('session')
    if not haveLogin(session):
        return '{"code": -1}'
    else:
        uid = lg.session_map[session][1]
        id = int(request.args['id'])
        if id == uid:
            return '{"code": 2}'
        if db.isFollow(uid, id):
            return '{"code": 1}'
        else:
            return '{"code": 0}'

#publish on the seeworld
@app.route('/publishCommit')
def publishCommit():
    session = request.cookies.get('session')
    if not haveLogin(session):
        return render_template('error.html', message='please login first')
    else:
        uid = lg.session_map[session][1]
        title = request.args['title']
        desc = request.args['description']
        detail = request.args['detail']
        title = formatDangerStr(title)
        desc = formatDangerStr(desc)
        detail = formatDangerStr(detail)
        type = request.args['type']
        if title == '' or desc == '':
            return render_template('error.html', message="title and description should not be empty")
        db.addMessage(uid, title, desc, detail, type)
        return redirect('/see?page=1&type=0')

#register a new
@app.route('/registerNew')
def registerNew():
    return render_template('register.html')

#change the user password
@app.route('/changePassword', methods=['POST'])
def changePassword():
    session = request.cookies.get('session')
    if not haveLogin(session):
        return render_template('error.html', message='please login first')
    password = request.form['password']
    if not detectPassword(password):
        return render_template('error.html', message='Your password(at least 5 characters) should be a mix of numbers and letters.')
    uid = lg.session_map[session][1]
    db.updatePassword(uid, password)
    lg.session_map.pop(session)
    response = make_response(render_template('success.html', message='update message ok. Please login again.'))
    response.delete_cookie('session')
    return response


app.run(debug=True)