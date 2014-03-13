
import json
import logging

import tornado.ioloop
import tornado.web

class MainHandler(tornado.web.RequestHandler):
    """ The homepage, TODO put this in /handlers/ somewhere appropriate """
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
        self.seed()

        # let tornado __init__ whatever it needs
        tornado.web.Application.__init__(self, handlers, **settings)

    def init_db(self):
        """ 
        Connect to database, create tables if they don't exist .. 
        stash this code somewhere else at some point as a mixin
        """

        logging.info("Initializing database..")
        
        import sqlite3
        self.db = sqlite3.connect('data.db')
        cursor = self.db.cursor()

        queries = {
            'resources': "CREATE TABLE resources (slug, name, email, phone, description, logo)",
            'reviews': "CREATE TABLE reviews (resource, author, role, rating, review)",  # join on resource and author
            'authors': "CREATE TABLE authors (name, role, email)",
            'tags': "CREATE TABLE tags (slug, human)",
            'tags_reviews': "CREATE TABLE tags_reviews (tag_id, review_id)", #m2m, use ROWID for _id
            # sessions when that comes
        }


        for table in queries:
            cursor.execute( "SELECT name FROM sqlite_master WHERE type='table' AND name = ?", (table,))
            if not cursor.fetchall():
                logging.info( "creating table {}".format(table)) 
                cursor.execute( queries[table])

        self.db.commit()

    def seed(self):
        """ Pump in some placeholder data for dev work / testing """

        from random import choice

        cursor = self.db.cursor()

        # we have hash/content
        for key in self.content:
            slug = key
            description = self.content[key]

            words = self.content[key].split()[1:-2]

            name = choice(words).capitalize() + ' ' + choice(words).capitalize()
            email = 'nobody@nowhere.com'  # should choose some blanks, whatevs
            phone = '312-555-1212'

            logo = 'http://lorempixel.com/200/200/animals/' 

            cursor.execute( "INSERT INTO resources (slug, name, email, phone, description, logo) VALUES (?,?,?,?,?,?)", 
                            (slug, name, email, phone, description, logo))

        self.db.commit()



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
    logging.info( 'Serving on port %d' % options.port )
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()

