import tornado.web
import json
import logging

HTTPError = tornado.web.HTTPError

class Reviews(tornado.web.RequestHandler):
    def get(self):
        """ look up approved reviews by whatever page is calling for them """

        # look up any reviews for this page and dump them back as JSON
        page = self.page

        self.finish( json.dumps([]))

    def post(self):
        """ incoming reviews """

        body = self.get_argument('review')  # should throw an error if not passed in
        author = self.get_argument('author', '')
        logging.info(author)
        page = self.page

        logging.info( page)

        # stash this in a database somewhere
        db = self.application.db.cursor()  # db is a connection, but this is a cursor
        db.execute( "INSERT INTO reviews (url, author, body, approved) VALUES (?,?,?,?)", (page, author, body, False))
        self.application.db.commit()

        self.finish()

    @property
    def page(self):
        page = self.request.headers['referer']
        # properly parse this and check domains for multi-tenant, etc
        page = page.split('page/')[1]  # huge TODO

        return page
