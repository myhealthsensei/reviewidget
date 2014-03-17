import tornado.web
HTTPError = tornado.web.HTTPError

class Page(tornado.web.RequestHandler):
    def get(self, page):

        self.application.cursor.execute( "SELECT * FROM resources WHERE slug=%s", (page,))

        page = dict(self.application.cursor.fetchone())

        if not page:
            raise HTTPError(404)

        out = {'page':page}
        self.render('page.html', **out)

