
import json
import logging

import tornado.ioloop
import tornado.web

class MainHandler(tornado.web.RequestHandler):
    """ The homepage, TODO put this in /handlers/ somewhere appropriate """
    def get(self):

        cursor = self.application.cursor
        cursor.execute( "SELECT * FROM resources")  # eh.. random? somehow?

        links = [dict(row) for row in cursor.fetchall()][:13]

        # links = self.application.content.keys()
        outs = {'links':links}

        self.render('main.html', **outs)

from db import DB
class App(DB, tornado.web.Application):

    """ 
        The Application is usually a singleton per process,
        which makes it a good place to stash globals like 
        database connections or dummy content you don't want to hit the disk for
    """

    def __init__(self, seed=False):
        """ Settings """
        settings = dict(
            cookie_secret="change this in production",  # key for encrypted cookies
            template_path= "templates",  # put templates in /templates/
            static_path= "static",  # and static files in /static/
            xsrf_cookies= False,
            autoescape = None,
            login_url = '/login/', 
            debug = True,  # autoreloads on changes, among other things
        )

        """ Map handler classes to URLs with regex """
        from handlers.content import Page
        from handlers.reviews import Reviews
        from handlers.auth import Login,Logout
        from handlers.admin import Admin
        handlers = [
            (r"/", MainHandler),
            # (r"/reviews", Reviews),  # meant to be for an async widget, crufty now
            (r"/page/(.*)", Page),
            (r"/login/?", Login),
            (r"/logout/?", Logout),
            (r"/admin/?", Admin),
        ]

        self.init_db()

        # fixtures if we want them
        if seed:
            self.seed()

        # let tornado __init__ whatever it needs
        tornado.web.Application.__init__(self, handlers, **settings)


    def adduser(self, login):
        """ util method to add users from commandline, good for bootstrapping the first user """
    
        logging.info('Adding user {}'.format(login))

        self.cursor.execute( "SELECT * FROM authors WHERE login=%s", (login,)) 
        if self.cursor.fetchone():
            return logging.error( "User {} already exists - aborting!".format(login))
    
        import getpass
        from hashlib import sha256

        # prompt for password at commandline
        password = getpass.getpass()
        passhash = sha256(password+self.settings['cookie_secret']).hexdigest()

        # dump it into database
        self.cursor.execute( "INSERT INTO authors (login,passhash,admin) VALUES (%s,%s,%s)", (login,passhash,True))
        self.db.commit()


def main():
    from tornado.options import define, options
    """
    define any extra commandline params
    """
    define("port", default=8001, help="run on the given port", type=int)
    define("runtests", default=False, help="run tests", type=bool)
    define("seed", default=False, help="Build tables and set up dummy/fixture data")
    define("adduser", default='', help="Add user from commandline, eg --adduser=japherwocky")

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

    application = App(seed=options.seed)

    if options.adduser:
        application.adduser(options.adduser)

    application.listen(options.port)
    logging.info( 'Serving on port %d' % options.port )
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()

