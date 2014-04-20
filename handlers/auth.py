from hashlib import sha256
import logging

import tornado.web
HTTPError = tornado.web.HTTPError

from handlers import BaseHandler

class Login(BaseHandler):
    def get(self, error=None):
        self.render('login.html', error=error, next=self.get_argument('next', '/'))

    def post(self):
        """ Check incoming args, set appropriate cookies """
        login = self.get_argument('login').strip().lower()

        password = self.get_argument('password')  # major TODO is SSL
        passhash = sha256(password + self.application.settings['cookie_secret']).hexdigest()

        user = self.application.cursor.execute( "SELECT * FROM authors WHERE login=%s", (login,))
        user = self.application.cursor.fetchone()

        if not user:
            return self.get( error="Invalid Login")

        elif passhash != user['passhash']:
            return self.get(error="Invalid Password")

        else:
            self.set_secure_cookie('user', user['login'])

        self.redirect(self.get_argument('next'))

class Logout(tornado.web.RequestHandler):
    def get(self):
        self.clear_cookie('user')

        self.redirect('/')

class Signup(BaseHandler):
    def post(self):
        """ validate an email address to be used as a login """
        # post an email
        email = self.get_argument('email')

        # validate that it's legal.. i guess if it bounces it isn't!

        # generate a token
        token = sha256( email + self.application.settings['cookie_secret']).hexdigest()

        # send email with URL

    def get(self, token):
        """ check an incoming token to validate an email, display a form to set the password """
        pass 


