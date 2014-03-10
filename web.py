
import json
from logging import info

import tornado.ioloop
import tornado.web

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        links = self.application.content.keys()

        outs = {'links':links}

        self.render('main.html', **outs)

class App(tornado.web.Application):

    """ 
        The Application is usually a singleton per process,
        which makes it a good place to stash globals like 
        database connections or dummy content you don't want to hit the disk for
    """

    def __init__(self):
        """ Settings """
        settings = dict(
            cookie_secret="change this in production",  # key for encrypted cookies
            template_path= "templates",  # put templates in /templates/
            static_path= "static",  # and static files in /static/
            xsrf_cookies= False,
            autoescape = None,
            debug = True,  # autoreloads on changes, among other things
        )

        """ Map handler classes to URLs with regex """
        from handlers.content import Page
        from handlers.reviews import Reviews
        handlers = [
            (r"/", MainHandler),
            (r"/reviews", Reviews),
            (r"/page/(.*)", Page),
        ]

        # stash dummy content here
        self.content = json.loads(open('static/alice.json').read())

        self.init_db()

        # let tornado __init__ whatever it needs
        tornado.web.Application.__init__(self, handlers, **settings)

    def init_db(self):
        """ Connect to database, create tables if they don't exist """
        
        import sqlite3
        self.db = sqlite3.connect('data.db')

        return


def main():
    from tornado.options import define, options
    """
    define any extra commandline params
    """
    define("port", default=8001, help="run on the given port", type=int)
    define("runtests", default=False, help="run tests", type=bool)

    """
    parse however the process was started
    """
    tornado.options.parse_command_line()

    """
    do whatever with the options defined above.  when/if this gets long
    and ugly, refactor it into it's own file
    """
    if options.runtests:
        #put tests in the tests folder
        import tests, unittest
        import sys
        sys.argv = ['web.py',] #unittest goes digging in argv
        unittest.main('tests')
        return


    application = App()
    application.listen(options.port)
    info( 'Serving on port %d' % options.port )
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()

