
from tornado.testing import AsyncHTTPTestCase
from tornado.httpclient import HTTPRequest
from tornado.httputil import HTTPHeaders

from web import App

class TestCase(AsyncHTTPTestCase):

    _cookies = HTTPHeaders()

    def get_app(self):
        """
        Instantiate the app and do whatever database fakery you need
        """
        self._app = App()

        return self._app

    def fetch(self, url, args=None):
        if not args:
            Req = HTTPRequest( self.get_url(url), method="GET", headers=self._cookies )
        else:
            Req = HTTPRequest( self.get_url(url), method="POST", body=urlencode(args), headers=self._cookies)

        self.http_client.fetch( Req, self.stop)

        response = self.wait()

        #maintain cookies
        if 'Set-Cookie' in response.headers:
            self._cookies['Cookie'] = response.headers['Set-Cookie']

        return response

class Test(TestCase):

    def test_sanity(self):

        response = self.fetch('/')

        assert response.code == 200
