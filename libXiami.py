import urllib
import urllib2
import cookielib
import StrCookieJar
import json
import lxml.html


headers = {
    "Referer": "http://www.xiami.com/member/login",
    "User-Agent": 'Mozilla/5.0 (IsomByt; checker)',
}

class User:

    def __init__(self):
        self.opener = None
        self._data = None

    def loadCookie(self,cookie):
        self.cookie = StrCookieJar.StrCookieJar(cookie)
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookie))

    def dumpCookie(self):
        return self.cookie.dump()

    def login(self,email,password):
        self.cookie = StrCookieJar.StrCookieJar()
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookie))

        login_url = "https://login.xiami.com/member/login"

        request = urllib2.Request(login_url,headers=headers)
        response = self.opener.open(request)
        data = response.read()
        dom = lxml.html.fromstring(data)
        args = dict(map(lambda x:(str(x.name),unicode(x.value).encode("u8")),dom.xpath("//form//input")))
        args["email"] = email
        args["password"] = password

        request = urllib2.Request(login_url, urllib.urlencode(args), headers)
        response = self.opener.open(request)
        data = response.read()

    def __getitem__(self,key):
        if not self.data:
            raise BaseException("please login")
        return self.data[key]

    @property
    def data(self):
        if not self._data:
            data = self.getuserinfo()
            if data["status"]:
                self._data = data["data"]['userInfo']
        return self._data

    def getuserinfo(self):
        url = "http://www.xiami.com/index/home"
        request = urllib2.Request(url,headers=headers)

        response = self.opener.open(request)
        data = response.read()
        return json.loads(data)

    @property
    def ischeckined(self):
        if self.data and self.data["is"]:
            return True
        return False

    @property
    def islogined(self):
        if self.data and self.data["user_id"]:
            return True
        return False

    def checkin(self):
        url = "http://www.xiami.com/task/signin"
        request = urllib2.Request(url,urllib.urlencode({}),headers)

        response = self.opener.open(request)
        days = response.read()
        if days:
            return int(days)
        return None

