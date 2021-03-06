

import os
import sys
import urlparse
import logging
import json
import psycopg2
import psycopg2.extras

class DB:
    """
    Mix this into an application object to handle database miscellany
    """

    def init_db(self):
        """ 
        Connect to database, create tables if they don't exist .. 
        """

        logging.info("Initializing database..")

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
            # prolly something like: export DATABASE_URL=postgres://sensei:sensei@localhost:5432/mhs
            logging.error("No $DATABASE_URL found in environ, ABORTING STARTUP")
            logging.debug("try: export DATABASE_URL=postgres://sensei:sensei@localhost:5432/mhs")
            sys.exit(1)

        # build connections to db
        self.cursor = self.db.cursor(cursor_factory = psycopg2.extras.DictCursor)
        cursor = self.cursor

        queries = {
            'resources': """CREATE TABLE IF NOT EXISTS resources (
                id BIGSERIAL PRIMARY KEY,
                slug VARCHAR(50) UNIQUE, 
                name VARCHAR(100), 
                email VARCHAR(100), 
                phone VARCHAR(100), 
                description TEXT, 
                link VARCHAR(100),
                logo VARCHAR(100),
                public BOOLEAN DEFAULT FALSE
                )""",

            'reviews': """CREATE TABLE IF NOT EXISTS reviews (
                id BIGSERIAL PRIMARY KEY,
                resource_id INT, 
                author_id INT, 
                role VARCHAR(100), 
                rating INT, 
                public BOOLEAN DEFAULT FALSE,
                review TEXT
                )""",

            'authors': """CREATE TABLE IF NOT EXISTS authors (
                id BIGSERIAL PRIMARY KEY,
                name VARCHAR(100), 
                login VARCHAR(100) UNIQUE, 
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

            # signups to be validated
            'signups': """ CREATE TABLE IF NOT EXISTS signups (
                id BIGSERIAL PRIMARY KEY,
                email VARCHAR(100),
                hash VARCHAR(500)
                )""",
            # sessions when that comes
        }


        for table in queries:
            logging.debug( 'CREATING (IF NOT EXISTS) {}'.format(table))
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

