import requests

#for test
class Test:
    def __init__(self, url, sessionID):
        self.url = url
        self.header = {}
        self.cookies = {"session": sessionID}

    #test IsMe
    def testIsMe(self):
        response = requests.request('GET', url=self.url + "/isMe", cookies=self.cookies)
        data = response.json()
        if data['code'] == 1:
            print("test isMe OK")
        else:
            print("test isMe fail.")

    #test See page
    def testSee(self, start, count, type):
        response = requests.request('GET', url=self.url + f"/getAllWorld?start={start}&count={count}&type={type}", cookies=self.cookies)
        data = response.json()
        if data['code'] == 1:
            print("test see OK")
        else:
            print("test see fail.")

    #test user information
    def testUserinfo(self, id):
        response = requests.request('GET', url=self.url + f"/getUserInfo?id={id}", cookies=self.cookies)
        data = response.json()
        if data['code'] == 1:
            print("test getUserInfo OK")
        else:
            print("test UserInfo fail.")

    #test check
    def testCheck(self, id):
        response = requests.request('GET', url=self.url + f"/checkFocus?id={id}", cookies=self.cookies)
        data = response.json()
        if data.get('code') != None:
            print("test checkFocus OK")

    #test get focus
    def testGetFocus(self, id):
        response = requests.request('GET', url=self.url + f"/getFocus?id={id}", cookies=self.cookies)
        data = response.json()
        if data['code'] == 1:
            print("test getFocus OK")
        else:
            print("test getFocus fail.")

    #test get user world
    def testGetUserWorld(self, id):
        response = requests.request('GET', url=self.url + f"/getUserWorld?id={id}", cookies=self.cookies)
        data = response.json()
        if data['code'] == 1:
            print("test getUserWorld OK")
        else:
            print("test getUserWorld fail.")

    #test get message
    def testGetMessage(self, id):
        response = requests.request('GET', url=self.url + f"/getMessage?id={id}", cookies=self.cookies)
        data = response.json()
        if data['code'] == 1:
            print("test getMessage OK")
        else:
            print("test getMessage fail.")

    #test get the comment
    def testGetComment(self, id):
        response = requests.request('GET', url=self.url + f"/getComment?id={id}", cookies=self.cookies)
        data = response.json()
        if data['code'] == 1:
            print("test getComment OK")
        else:
            print("test getComment fail.")

    def testAll(self):
        self.testIsMe()
        self.testSee(0, 10, 0)
        self.testUserinfo(1)
        self.testCheck(2)
        self.testGetFocus(1)
        self.testGetUserWorld(1)
        self.testGetMessage(1)
        self.testGetComment(1)


test = Test("http://pawtest.pythonanywhere.com/", "16727526100")

test.testAll()