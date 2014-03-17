import tornado.web
HTTPError = tornado.web.HTTPError

from handlers import BaseHandler

class Admin(BaseHandler):

    @tornado.web.authenticated
    def get(self):

        self.render('main.html', links=[])

