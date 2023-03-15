from seeWorldDB import getUserByname
import time

session_map = {}
pretime = 0
session_end = 0

#Used to detect formatting errors of user names and passwords
def formatDangerStr(s : str):
    if s == None:
        return s
    s = s.replace('\\', '\\\\')
    s = s.replace('\n', ' ')
    s = s.replace('\t', ' ')
    s = s.replace('\'', '\\\'')
    s = s.replace('\"', '\\"')
    s = s.replace('\r', '')
    return s

#Log in with a user name and password
def login(name, password):
    name = formatDangerStr(name)
    password = formatDangerStr(password)
    data = getUserByname(name)
    if len(data) == 0 or data[0][1] != password:
        return (False, 0)
    else:
        newtime = int(time.time())
        global pretime
        if newtime != pretime:
            pretime = newtime
            session_end = 0
        session_id = str(int(time.time())) + str(session_end)
        session_end += 1
        session_map[session_id] = [newtime, data[0][0]]
        return (True, session_id, data[0][0])

#Log out after use
def logout(session):
    session_map.pop(session)