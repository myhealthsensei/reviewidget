
from logging import info

import tornado.ioloop
import tornado.web

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

application = tornado.web.Application([
    (r"/", MainHandler),
])


class App(tornado.web.Application):

    """ 
        The Application is usually a singleton per process,
        which makes it a good place to stash globals like 
        database connections
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
        handlers = [
            (r"/", MainHandler),
        ]

        tornado.web.Application.__init__(self, handlers, **settings)


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

