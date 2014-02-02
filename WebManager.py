import web
import gevent
import gevent.monkey
import gevent.pywsgi
from db import xiamidb
import time
import traceback
import os
from libXiami import User
gevent.monkey.patch_all()


class Main:

    def GET(self):
        return file("static/index.html").read()

    def POST(self):
        args = web.input()
        email = args.pop("email")
        password = args.pop("password")
        user = User()
        user.login(email,password)
        if user.islogined:
            xiamidb.add(user["user_id"],email,password)
            account = xiamidb.get(user["user_id"])
            account["last"] = time.time()
            account["cookie"] = user.dumpCookie()
            account["email"] = email
            if "savepw" in args:
                account["password"] = password
            else:
                account["password"] = None
            if "notifyme" in args:
                account["notify"] = True
            else:
                account["notify"] = False
            account["errcount"] = 0
            account["nexttime"] = account["last"]
            account["days"] = int(user["sign"]["persist_num"])
            xiamidb.update(**account)
            yield "email:%s\n"%email
            yield "uid:%s\n"%account['uid']
            yield "cookie:\n%s"%account['cookie']
            yield "days:%s\n"%account["days"]
            yield '\xe7\x99\xbb\xe8\xae\xb0\xe6\x88\x90\xe5\x8a\x9f\xef\xbc\x8c\xe8\xaf\xb7\xe5\x85\xb3\xe9\x97\xad\xe9\xa1\xb5\xe9\x9d\xa2'
        else:
            yield '\xe6\x97\xa0\xe6\xb3\x95\xe8\x8e\xb7\xe5\x8f\x96\xe7\x94\xa8\xe6\x88\xb7\xe4\xbf\xa1\xe6\x81\xaf\xef\xbc\x8c\xe8\xaf\xb7\xe6\xa3\x80\xe6\x9f\xa5\xe5\xb8\x90\xe5\x8f\xb7\xe6\x88\x96\xe5\xaf\x86\xe7\xa0\x81'


class Ctrl:

    def GET(self):
        yield "uid\temail\t\t\tdays\tlastcheck\tnextcheck\terrcount\tstatus\n"
        accounts = xiamidb.scan()
        for account in accounts:
            account["last"] -= time.time()
            account["nexttime"] -= time.time()
            yield "%(uid)s\t%(email)s\t%(days)s\t%(last)s\t%(nexttime)s\t%(errcount)s\t%(status)s\n"%account

class StaticFile:

    def GET(self,filename):
        path = "static/%s"%filename
        if os.path.exists(path):
            return file(path,"rb")
        return "404"


def checkin(account):
    user = User()
    user.loadCookie(account["cookie"])
    if not user.islogined and account["password"]:
        user.login(account["email"],account["password"])
    if user.islogined:
        if not user.ischeckined:
            days = user.checkin()
            if days:
                account["days"] = days
            else:
                account["errcount"] += 1
                account["nexttime"] = time.time() + 600
                account["status"] = u'\u7b7e\u5230\u5931\u8d25'
        else:
            days = int(user["sign"]["persist_num"])
            account["nexttime"] = time.time() + 3600
        account["status"] = u'\u6ca1\u6709\u5f02\u5e38'
    else:
        account["errcount"] += 1
        account["nexttime"] = time.time() + 600
        account["status"] = u'\u767b\u5f55\u5931\u8d25'
    account["last"] = time.time()
    xiamidb.update (**account)

def daemon():
    while True:
        accounts = xiamidb.scan(where="errcount<3 and nexttime<%s"%time.time())
        for account in accounts:
            try:
                checkin(account)
            except:
                traceback.print_exc()
                print "checkin error"
            time.sleep(5)
        time.sleep(5)

urls = (
    "/", "Main",
    "/Ctrl","Ctrl",
    "/(.*)","StaticFile",
)


def serve_forever():
    gevent.spawn(daemon)
    print web
    application = web.application(urls, globals()).wsgifunc()
    print 'Serving on 8888'
    server = gevent.pywsgi.WSGIServer(('', 8888), application)
    server.serve_forever()

if __name__ == "__main__":
    serve_forever()
