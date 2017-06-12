#!/usr/bin/env python

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import os.path
import tornado.auth
import tornado.escape


from Authentification import Profile, authentification

from tornado.options import define, options

define("port", default=9999, help="run on the given port", type=int)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/booking", BookingHandler),
            (r"/car", ManageHandler),
            (r"/profile", ProfileHandler),
            (r"/report", ReportHandler),
            (r"/register", RegisterHandler),
            (r"/login", LoginHandler),
            (r"/", MainHandler)

        ]
        settings = dict(
            cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=True,
            debug=True,
            autoescape=None,
        )
        tornado.web.Application.__init__(self, handlers, **settings)


class BaseHandler(tornado.web.RequestHandler):
    pass

class MainHandler(BaseHandler):
    @tornado.web.asynchronous
    def get(self):
        self.render('dashboard.html')

class BookingHandler(BaseHandler):
    @tornado.web.asynchronous
    def get(self):
        self.render('booking.html')

class ManageHandler(BaseHandler):
    @tornado.web.asynchronous
    def get(self):
        self.render('car.html')

class ProfileHandler(BaseHandler):
    @tornado.web.asynchronous
    def get(self):
        self.render('profile.html')

class ReportHandler(BaseHandler):
    @tornado.web.asynchronous
    def get(self):
        self.render('report.html')

class RegisterHandler(BaseHandler):
    @tornado.web.asynchronous
    def get(self):
        self.render('register.html')

class LoginHandler(BaseHandler):
    @tornado.web.asynchronous
    def get(self):
        self.render('login.html', error = self.get_argument('error',0, True))

    def post(self):
        self.auth = authentification()
        username = str(self.get_argument('username', strip=True))
        password = str(self.get_argument('password', strip=True))
        check_login = self.auth.do_login_probe(username, password)
        if check_login == False or check_login== None:
            self.redirect('/login?error=1')
        else:
            print type(check_login)
            if len(check_login) >=2:
                self.redirect('/')






        #if username == 'admin' and password=='admin':self.redirect('/'):
         #   pass





        #TODO: secure cookie
        #self.set_secure_cookie('do_login','this is my password')








def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()