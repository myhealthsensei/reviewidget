import tornado.web
HTTPError = tornado.web.HTTPError

from handlers import BaseHandler

class Admin(BaseHandler):

    @tornado.web.authenticated
    def get(self):

        self.cursor.execute("SELECT * FROM resources")
        links = [dict(row) for row in self.cursor.fetchall()]

        self.render('admin.html', links=links)

