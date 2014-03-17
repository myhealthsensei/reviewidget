from hashlib import sha256
import logging

import tornado.web
HTTPError = tornado.web.HTTPError

class Login(tornado.web.RequestHandler):
    def get(self, error=None):
        self.render('login.html', error=error)

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

        self.redirect('/')

