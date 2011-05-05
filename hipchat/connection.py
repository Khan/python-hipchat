import hipchat.config
import json

from urllib import urlencode
from urllib2 import urlopen, Request

def partial(func, *args, **keywords):
    def newfunc(*fargs, **fkeywords):
        newkeywords = keywords.copy()
        newkeywords.update(fkeywords)
        return func(*(args + fargs), **newkeywords)
    newfunc.func = func
    newfunc.args = args
    newfunc.keywords = keywords
    return newfunc


def call_hipchat(cls, ReturnType, url, data=True, **kw):
    auth = [('format', 'json'), ('auth_token', hipchat.config.token)]
    if not data:
        auth.extend(kw.items())
    req = Request(url=url + '?%s' % urlencode(auth))
    if data:
        req.add_data(urlencode(kw.items()))
    return ReturnType(json.load(urlopen(req)))


class HipChatObject(object):
    def __init__(self, jsono):
        self.jsono = jsono
        for k, v in jsono[self.sort].iteritems():
            setattr(self, k, v)

    def __str__(self):
        return json.dumps(self.jsono)
