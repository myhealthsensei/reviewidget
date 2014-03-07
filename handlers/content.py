import tornado.web
HTTPError = tornado.web.HTTPError

class Page(tornado.web.RequestHandler):
    def get(self, page):

        if page not in self.application.content:
            raise HTTPError(404)

        else:
            page = self.application.content[page]

        out = {'page':page}
        self.render('page.html', **out)

