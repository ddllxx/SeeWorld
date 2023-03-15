import pymysql

host = '127.0.0.1'
password = '123456'
username = 'seeword'
database = 'seeworld'

# conn = None
conn = None #pymysql.connect(host=host, user=username, passwd=password, database=database)
# cursor = None

#connect the sql
def Sqlconn():
    global conn
    if not conn or not conn.open:
        if conn:
            conn.close()
        conn = pymysql.connect(host=host, user=username, passwd=password, database=database)
    cursor = conn.cursor()
    return cursor

def SqlDisconn(cursor):
    cursor.close()
    # conn.close()

#exit the sql
def SqlExec(sql):
    flag = 3
    while flag > 0:
        try:
            cursor = Sqlconn()
            cursor.execute(sql)
            return cursor
        except:
            print('connect lost. retry...\n')
            flag -= 1
    print('could not connect to the database')

#commit the aql
def SqlCommit():
    flag = 3
    while flag > 0:
        try:
            conn.commit()
            return
        except:
            cursor = Sqlconn()
            SqlDisconn(cursor)
            flag -= 1
            print('connect lost. retry...\n')
    print('could not connect to the database')

#get user information
def getUserInfo(id):
    # cursor = Sqlconn()
    sql = f'SELECT * FROM t_user WHERE id = {id}'
    cursor = SqlExec(sql)
    data = cursor.fetchall()
    SqlDisconn(cursor)
    if len(data) == 0:
        return None
    return data[0]

#get user focus
def getUserFocus(id):
    # cursor = Sqlconn()
    sql = f'SELECT id2 FROM t_focus WHERE id1 = {id}'
    cursor = SqlExec(sql)
    data = cursor.fetchall()
    SqlDisconn(cursor)
    return data

#get all the world
def getAllWorld(start, count, type):
    # cursor = Sqlconn()
    sql = ''
    if type == '0':
        sql = f'SELECT user_id, name, p_date, t_message.id, title, description, type FROM t_message INNER JOIN t_user ON t_user.id = t_message.user_id ORDER BY p_date DESC LIMIT {start}, {count}'
    else:
        sql = f'SELECT user_id, name, p_date, t_message.id, title, description, type FROM t_message INNER JOIN t_user ON t_user.id = t_message.user_id WHERE type={type} ORDER BY p_date DESC LIMIT {start}, {count}'

    cursor = SqlExec(sql)
    data = cursor.fetchall()
    SqlDisconn(cursor)
    return data

#get user world
def getUserWorld(id):
    # cursor = Sqlconn()
    sql = f'SELECT p_date, id, title, description, detail FROM t_message WHERE user_id = {id}'
    cursor = SqlExec(sql)
    data = cursor.fetchall()
    SqlDisconn(cursor)
    return data

#get the message
def getMessage(id):
    # cursor = Sqlconn()
    sql = f'SELECT title, description, detail, user_id FROM t_message WHERE id = {id}'
    cursor = SqlExec(sql)
    data = cursor.fetchall()
    SqlDisconn(cursor)
    return data[0]

#get the comment
def getComment(messageId):
    # cursor = Sqlconn()
    sql = f'SELECT name, content, t_user.id, t_comment.id, t_comment.p_date FROM t_user INNER JOIN t_comment ON t_user.id = t_comment.user_id WHERE t_comment.m_id = {messageId}'
    cursor = SqlExec(sql)
    data = cursor.fetchall()
    SqlDisconn(cursor)
    return data

#add the comment
def addComment(uid, mid, content):
    # cursor = Sqlconn()
    sql = f'INSERT INTO t_comment(user_id, m_id, content) VALUES({uid}, {mid}, \'{content}\')'
    cursor = SqlExec(sql)
    SqlDisconn(cursor)
    SqlCommit()

#delete the comment
def delComment(id):
    sql = f'DELETE FROM t_comment WHERE id = {id}'
    cursor = SqlExec(sql)
    SqlDisconn(cursor)
    SqlCommit()

#register the account
def register(name, password, sex, age, profession, nation, introduction):
    # cursor = Sqlconn()
    sql = f'SELECT * FROM t_user where name=\'{name}\''
    cursor = SqlExec(sql)
    data = cursor.fetchall()
    if len(data) != 0:
        SqlDisconn(cursor)
        return False
    else:
        cursor.execute(f'INSERT INTO t_user(name, password, sex, age, profession, nation, introduction) VALUES(\'{name}\', \'{password}\', \'{sex}\', {age}, \'{profession}\', \'{nation}\', \'{introduction}\')')
        SqlDisconn(cursor)
        SqlCommit()
        return True

#add the follow
def addFollow(uid, id):
    # cursor = Sqlconn()
    sql = f'INSERT INTO t_focus VALUES({uid}, {id})'
    cursor = SqlExec(sql)
    SqlDisconn(cursor)
    SqlCommit()

#remove the follow
def removeFollow(uid, id):
    # cursor = Sqlconn()
    sql = f'DELETE FROM t_focus WHERE id1 = {uid} AND id2 = {id}'
    cursor = SqlExec(sql)
    SqlDisconn(cursor)
    SqlCommit()

#check the follow
def isFollow(uid, id):
    # cursor = Sqlconn()
    sql = f'SELECT * FROM t_focus WHERE id1={uid} AND id2={id}'
    cursor = SqlExec(sql)
    data = cursor.fetchall()
    SqlDisconn(cursor)
    if len(data) != 0:
        return True
    else:
        return False
#add the message
def addMessage(id, title, desc, detail, type):
    # cursor = Sqlconn()
    sql = f'INSERT INTO t_message(user_id, title, description, detail, type) VALUES({id}, \'{title}\', \'{desc}\', \'{detail}\', {type})'
    cursor = SqlExec(sql)
    SqlDisconn(cursor)
    SqlCommit()

#get username
def getUserByname(name):
    # cursor = Sqlconn()
    sql = f"SELECT id, password FROM t_user WHERE name = '{name}'"
    cursor = SqlExec(sql)
    data = cursor.fetchall()
    SqlDisconn(cursor)
    return data

#update Password
def updatePassword(uid, password):
    sql = f'UPDATE t_user SET password=\'{password}\' WHERE id={uid}'
    cursor = SqlExec(sql)
    SqlDisconn(cursor)
    SqlCommit()