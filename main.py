#!/usr/bin/env python

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import os.path
import tornado.auth
import tornado.escape
import json

from Authentification import Profile, authentification

from tornado.options import define, options

define("port", default=9999, help="run on the given port", type=int)
from es import db

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/booking", BookingHandler),
            (r"/car", ManageHandler),
            (r"/car/add", CarAddHandler),
            (r"/profile", ProfileHandler),
            (r"/report", ReportHandler),
            (r"/register", RegisterHandler),
            (r"/login", LoginHandler),
            (r"/logout", LogoutHandler),
            (r"/invoice", InvoiceHandler),
            (r"/", MainHandler)

        ]
        settings = dict(
            cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=True,
            debug=True,
            autoescape=None,
            login_url = "/login"
        )
        tornado.web.Application.__init__(self, handlers, **settings)


class BaseHandler(tornado.web.RequestHandler):
    def prepare(self):
        self.db = db()

    def get_current_user(self):
        return self.get_cookie("profileid")
    def get_profile(self):
        return tornado.escape.json_decode(self.get_secure_cookie('udata'))

class InvoiceHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('invoice.html')



class MainHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        profile = self.get_profile()
        print json.dumps(profile)
        self.render('dashboard.html', profile=profile)

class BookingHandler(BaseHandler):
    @tornado.web.asynchronous
    def get(self):
        profile = self.get_profile()
        self.render('booking.html', profile=profile)

class ManageHandler(BaseHandler):
    @tornado.web.asynchronous
    def get(self):
        self.db = authentification()
        brands = self.auth.load_brands()
        profile = self.auth.get_profile(self.get_current_user())
        self.render('car.html', brands=brands, profile=profile)

class CarAddHandler(BaseHandler):
    def get(self):
        pass

    def post(self):
        args = {
            'license': self.get_argument('add_license', False, strip=True),
            'model': self.get_argument('add_model', False, strip=True),
            'brand': self.get_argument('add_brand', False, strip=True),
            'type': self.get_argument('add_type', False, strip=True),
            'engine': self.get_argument('add_engine', False, strip=True),
            'fuel': self.get_argument('add_fuel', False, strip=True),
            'fuel_type': self.get_argument('add_fuel_type', False, strip=True),
            'places': self.get_argument('add_places', False, strip=True),
            'rental_price': self.get_argument('add_rental_price', False, strip=True),
            'status': self.get_argument('add_status', False, strip=True)
        }

        self.write(args)


class ProfileHandler(BaseHandler):
    @tornado.web.asynchronous
    def get(self):
        profile = self.get_profile()
        self.render('profile.html', profile=profile)

class ReportHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        profile = self.get_profile()
        datatable = self.db.get_report_datatable()
        self.render('report.html', profile=profile,datatable=datatable)

class RegisterHandler(BaseHandler):
    @tornado.web.asynchronous
    def get(self):
        self.render('register.html' )

class LoginHandler(BaseHandler):
    @tornado.web.asynchronous
    def get(self):
        self.render('login.html', error = self.get_argument('error',0, True))

    def post(self):
        username = str(self.get_argument('username', strip=True))
        password = str(self.get_argument('password', strip=True))
        profile = self.db.do_login(username,password)

        if profile:
            self.set_current_user(profile['_id'], profile)
            self.redirect('/')
        else:
            self.redirect('/login?error=1')



    def set_current_user(self, user, profile):
        if user:
            self.set_cookie("profileid", str(user))
            self.set_secure_cookie('udata', tornado.escape.json_encode(profile))
        else:
            self.clear_cookie("profileid")

        #if username == 'admin' and password=='admin':self.redirect('/'):
         #   pass

class LogoutHandler(BaseHandler):
    @tornado.web.asynchronous
    def get(self):
        self.clear_all_cookies()
        self.clear_cookie('profileid')
        self.clear_cookie('udata')
        self.redirect('/')




                    #TODO: secure cookie
        #self.set_secure_cookie('do_login','this is my password')








def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
