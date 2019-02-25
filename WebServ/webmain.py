import tornado.ioloop
import tornado.web
import tornado.options
import pymysql
import os

tornado.options.define("port", default=8000, type=int, help="tornado run on port")

class FinDB(object):
    def __init__(self):
        self.db = pymysql.connect(host='127.0.0.1', user='root', password='billchang106',
                                  db='financial', port=3306)
        self.cur = self.db.cursor()

    def __delete__(self, instance):
        self.db.close()

    def query(self, sqlstr):
        try:
            self.cur.execute(sqlstr)
            result = self.cur.fetchall()
        except Exception as e:
            self.db.rollback()
        else:
            return result

    def insert(self, sqlstr):
        try:
            self.cur.execute(sqlstr)
            self.cur.commit()
        except Exception as e:
            self.db.rollback()

class LoginHdl(tornado.web.RequestHandler):
    def __init__(self, application, request, **kwargs):
        tornado.web.RequestHandler.__init__(self, application, request, **kwargs)
        self.db = FinDB()

    def get(self):
        self.render("index.html", type="login")

    def post(self):
        username = self.get_argument("form-username")
        password = self.get_argument("form-password")
        sqlstr = "select password from user where username='%s';" % username
        result = self.db.query(sqlstr)
        if result:
            pswd = result[0][0]
            if pswd == password:
                self.redirect("/posi")
            else:
                self.render("index.html",type="logerr")
        else:
            self.render("index.html", type="logerr")

class PosiHdl(tornado.web.RequestHandler):
    def __init__(self, application, request, **kwargs):
        tornado.web.RequestHandler.__init__(self, application, request, **kwargs)
        self.db = FinDB()

    def get(self):
        sqlstr="select * from financial.position where posi_type='股票';"
        stocks = self.db.query(sqlstr)
        sqlstr = "select * from position where posi_type='期货';"
        futures = self.db.query(sqlstr)
        sqlstr = "select * from position where posi_type='基金';"
        funds = self.db.query(sqlstr)
        sqlstr = "select * from position where posi_type='期权';"
        options = self.db.query(sqlstr)
        self.render("posi.html", stock=stocks, future=futures, fund=funds, options=options)

def make_app():
    current_path = os.path.dirname(__file__)
    settings = dict(static_path=os.path.join(current_path, "static"),
                    template_path=os.path.join(current_path, "template"))
    return tornado.web.Application(
        [
            (r"/", LoginHdl),
            (r"/posi", PosiHdl)
        ],
        **settings
    )

if __name__ == "__main__":
    app = make_app()
    tornado.options.parse_command_line()
    app.listen(tornado.options.options.port)
    tornado.ioloop.IOLoop.current().start()