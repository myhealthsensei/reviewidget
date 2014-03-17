import tornado.web
import psycopg2.extras

class BaseHandler(tornado.web.RequestHandler):

    @property
    def db(self): 
        """ convenience shortcut """
        return self.application.db


    _cursor = None

    @property
    def cursor(self):
        """Create a new cursor per request"""
        if not self._cursor:
            self._cursor = self.db.cursor(cursor_factory=psycopg2.extras.DictCursor)

        return self._cursor


    _user = None

    @property
    def user(self): return self.get_current_user()

    def get_current_user(self):
        if not self._user:
            login = self.get_secure_cookie('user')
            if not login:
                return None

            self.cursor.execute( "SELECT * FROM authors WHERE login=%s", (login,))
            self._user = self.cursor.fetchone()

        return self._user

