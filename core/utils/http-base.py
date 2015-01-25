#!/usr/bin/python env
#coding=utf-8

import os,sys
import urllib2
import cookielib

class Http:
    def __init__(self, url, port = 80, timeout = 5, cookies = None, proxy = None):
        self._url = url
        self._cookies = cookies
        self._proxy = proxy
        self._timeout = timeout
        self.code = -1
        self.data = ''

    def head(self):
        try:
            request = urllib2.Request(self._url)
            request.get_method = lambda: 'HEAD'
            response = urllib2.urlopen(request, timeout = self._timeout)
            self.code = response.getcode()
            self.data = response.headers
        except urllib2.HTTPError,e:
            self.code = e.code
            self.data = str(e)
        except Exception,e:
            self.code = -1
            self.data = str(e)

        return self

    def get(self):
        try:
            opener = urllib2.build_opener(urllib2.HTTPHandler)
            headers['Accept'] = 'application/json'
            url = '%s%s' % (config.base_url, url)
            if data:
                data = urllib.urlencode(data)
                url += ('?%s' % data)
            request = urllib2.Request(url, headers=headers)
            request.get_method = lambda: 'GET'
            resp = opener.open(request, timeout=30)
            return cls._decode(resp.read(), resp.getcode())
        except urllib2.HTTPError, e:
            return cls._decode(e.read(), e.getcode())

    def code(self):
        response = None

        try:
            req = urllib2.Request(self._url)
            opener = urllib2.build_opener()
            response = opener.open(req, timeout = self._timeout)
            retcode = response.code 
        except urllib2.URLError as e:
            if hasattr(e, 'code'):
                self.code = e.code
                self.data = str(e)
        except Exception,e:
            self.code = -1
            self.data = str(e)
        finally:
            if response:
                response.close()

        return self


if __name__ == "__main__":
    tmp = Http("http://www.geostar.com.cn/php木马.php")
    print tmp.head()
    print tmp.code()

