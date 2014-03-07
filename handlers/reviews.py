import tornado.web
import json

HTTPError = tornado.web.HTTPError

class Reviews(tornado.web.RequestHandler):
    def get(self):


        page = self.request.headers['referer']

        # properly parse this and check domains for multi-tenant, etc
        page = page.split('page/')[1]  # huge TODO

        # look up any reviews for this page and dump them back as JSON

        self.finish( json.dumps([]))

