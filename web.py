
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


class App(tornado.web.Application):

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
            debug = True,  # autoreloads on changes, among other things
        )

        """ Map handler classes to URLs with regex """
        from handlers.content import Page
        from handlers.reviews import Reviews
        from handlers.auth import Login
        handlers = [
            (r"/", MainHandler),
            (r"/reviews", Reviews),  # meant to be for an async widget, crufty now
            (r"/page/(.*)", Page),
            (r"/login/?", Login),
        ]


        self.init_db()

        if seed:
            self.seed()

        # let tornado __init__ whatever it needs
        tornado.web.Application.__init__(self, handlers, **settings)

    def init_db(self):
        """ 
        Connect to database, create tables if they don't exist .. 
        stash this code somewhere else at some point as a mixin
        """

        logging.info("Initializing database..")

        import os
        import urlparse

        import psycopg2
        import psycopg2.extras

        if "DATABASE_URL" in os.environ:
            urlparse.uses_netloc.append("postgres")
            url = urlparse.urlparse(os.environ["DATABASE_URL"])

            self.db = psycopg2.connect(
                database=url.path[1:],
                user=url.username,
                password=url.password,
                host=url.hostname,
                port=url.port
            )

        else:
            logging.error("No $DATABASE_URL found in environ, ABORTING STARTUP")
            os.exit(1)

        # build connections to db
        self.cursor = self.db.cursor(cursor_factory = psycopg2.extras.DictCursor)
        cursor = self.cursor

        queries = {
            'resources': """CREATE TABLE IF NOT EXISTS resources (
                id BIGSERIAL PRIMARY KEY,
                slug VARCHAR(50), 
                name VARCHAR(100), 
                email VARCHAR(100), 
                phone VARCHAR(100), 
                description TEXT, 
                logo VARCHAR(100)
                )""",

            'reviews': """CREATE TABLE IF NOT EXISTS reviews (
                id BIGSERIAL PRIMARY KEY,
                resource_id INT, 
                author_id INT, 
                role VARCHAR(100), 
                rating INT, 
                review TEXT
                )""",

            'authors': """CREATE TABLE IF NOT EXISTS authors (
                id BIGSERIAL PRIMARY KEY,
                name VARCHAR(100), 
                passhash VARCHAR(100), 
                admin BOOL, 
                email VARCHAR(100)
                )""",

            'tags': """CREATE TABLE IF NOT EXISTS tags (
                id BIGSERIAL PRIMARY KEY,
                slug VARCHAR(100), 
                human VARCHAR(100)
                )""",

            # m2m table linking tags and reviews
            'tags_reviews': """CREATE TABLE IF NOT EXISTS tags_reviews (
                tag_id INT, 
                review_id INT
                )""",
            # sessions when that comes
        }


        for table in queries:
            logging.debug( 'CREATING {}'.format(table))
            cursor.execute( queries[table])

        self.db.commit()


    def seed(self):
        """ Pump in some placeholder data for dev work / testing """

        from random import choice

        cursor = self.db.cursor()

        # stash dummy content here
        self.content = json.loads(open('static/alice.json').read())

        # we have hash/content
        for key in self.content:
            slug = key
            description = self.content[key]

            words = self.content[key].split()[1:-2]

            name = choice(words).capitalize() + ' ' + choice(words).capitalize()
            email = 'nobody@nowhere.com'  # should choose some blanks, whatevs
            phone = '312-555-1212'

            logo = 'http://lorempixel.com/200/200/animals/' 

            cursor.execute( "INSERT INTO resources (slug, name, email, phone, description, logo) VALUES (%s,%s,%s,%s,%s,%s)", 
                            (slug, name, email, phone, description, logo))

        self.db.commit()



def main():
    from tornado.options import define, options
    """
    define any extra commandline params
    """
    define("port", default=8001, help="run on the given port", type=int)
    define("runtests", default=False, help="run tests", type=bool)
    define("seed", default=False, help="Build tables and set up dummy/fixture data")

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
    application.listen(options.port)
    logging.info( 'Serving on port %d' % options.port )
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()

