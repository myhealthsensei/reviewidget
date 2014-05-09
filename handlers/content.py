import json
import tornado.web
HTTPError = tornado.web.HTTPError
from handlers import BaseHandler
from collections import defaultdict

from psycopg2 import IntegrityError

class Resource(BaseHandler):
    keys = ['description', 'id', 'public', 'logo', 'slug', 'name', 'email', 'phone', 'link']

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

    def post(self, slug=None):
        data = json.loads(self.request.body)

        if data['id']: 
            self.update(data)
        else: 
            self.create(data)

    def create(self, data):
        """
        CREATE A NEW RESOURCE
        """

        # not all keys will get posted, but dont trust what *does* get posted
        keys = [k for k in self.keys if k in data.keys()]  # maybe a set() intersection

        # id is False, but postgres wants it to be None for the autoinc
        keys.remove('id')

        q = """INSERT INTO resources ({}) VALUES ({})""".format( 
            ','.join(keys), ','.join( ['%s' for i in range(len(keys))]))

        try:
            # insert row
            self.cursor.execute(q, [data[k] for k in keys])

            # get the new id if it was successful
            self.cursor.execute("""SELECT CURRVAL('resources_id_seq')""")
            data['id'] = self.cursor.fetchone()[0]

            # commit to the db
            self.db.commit()

            # pass it all back to the frontend
            self.finish(data)

        except IntegrityError as e:
            # oh dear, we've violated a constraint.. generate error messages and send them back out

            # duplicate key constraint
            if e.pgcode == '23505':
                # get the key
                errorkey = e.message.split('Key (',1)[1].split(')')[0]
                data['errors'] = {errorkey: 'A resource is already using this URL!'}

            self.db.rollback()  # reset the transaction for everything else
            return self.finish(data)






