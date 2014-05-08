import tornado.web
HTTPError = tornado.web.HTTPError
from handlers import BaseHandler

class Resource(BaseHandler):
    def get(self, slug=None):

        if not slug:
            return self.get_index()

        self.application.cursor.execute( "SELECT * FROM resources WHERE slug=%s", (page,))

        page = dict(self.application.cursor.fetchone())

        if not page:
            raise HTTPError(404)

        out = {'resource':resource }
        self.render('page.html', **out)

    def get_index(self):
        """
        Load some sort of something that lists all resources
        """

        out = {
            'user':self.user
            }

        self.render('resource.html', **out)

