import tornado.web
HTTPError = tornado.web.HTTPError

from handlers import BaseHandler

class Admin(BaseHandler):

    @tornado.web.authenticated
    def get(self):

        self.cursor.execute("SELECT * FROM resources")
        links = [dict(row) for row in self.cursor.fetchall()]

        self.render('admin.html', links=links)

class Edit(BaseHandler):

    @tornado.web.authenticated
    def get(self, slug):

        if slug == 'new':
            data = defaultdict( lambda x: '')
            data['id'] = 0
        else:
            self.cursor.execute("SELECT * FROM resources WHERE slug=%s", (slug,))
            data = dict(self.cursor.fetchone())

        self.render('editresource.html', page=data, **data)


    def post(self, slug):
        """
        Wherein we should probably be using an ORM / form validation lib
        """

        incoming = {}
        varchars = ['slug', 'name', 'email', 'phone', 'description', 'link', 'logo']

        incoming['id'] = int(self.get_argument('id'))  # pass 0 on new, but always an int

        for varchar in varchars:
            incoming[varchar] = self.get_argument( varchar )

        args = tuple( [incoming[k] for k in varchars] +[incoming['id']])
        # an edit
        if incoming['id'] > 0:
            self.cursor.execute(
            """ 
            UPDATE resources SET
                slug = %s,
                name = %s,
                email = %s,
                phone = %s,
                description = %s,
                link = %s,
                logo = %s
            WHERE id=%s
            """, args)

        return self.redirect( '/admin/resource/{}'.format(incoming['slug']))

