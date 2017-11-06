import urllib, re, requests
FACEBOOK_TOKEN = "<Facebook Token>"

# Example simple feed loader
class FeedLoader():
    source = 'feed'
    fields = 'id,from,message,name,status_type,shares,to,updated_time,created_time,caption,link,type,message_tags,story'
    limit = 100

    def __init__(self, parent_id, since=None, until=None):
        self.query = "%s/%s" % (parent_id, self.source)
        self.args = {'fields': self.fields, 'limit': self.limit, 'since': since, 'until': until}

    def fb_request_url(self, path, args=None):
        args = args or {}
        args["access_token"] = FACEBOOK_TOKEN
        return "https://graph.facebook.com/" + path + "?format=json&" + urllib.urlencode(args)

    def get_next_token(self, url):
        u = re.search('until=([0-9]*)', url)
        until = u.group(1)
        u = re.search('__paging_token=([a-zA-Z0-9_]*)', url)
        token = u.group(1)
        return {'until': until, '__paging_token': token}

    def get_next_page_url(self, response):
        if response.has_key('paging') and response['paging'].has_key('next'):
            next_token = self.get_next_token(response['paging']['next'])
            return self.fb_request_url(self.query, args=dict(self.args.items() + next_token.items()))
        else:
            return None

    def get_url(self):
        return self.fb_request_url(self.query, self.args)


    def download_feed(self):
        res = []
        url = self.get_url()
        while url is not None:
            response = requests.get(url).json()
            res.extend(response['data'])
            url = self.get_next_page_url(response)
        return res

res =  FeedLoader("proctergamble", '2017-01-01', '2017-11-01').download_feed()
for i in res:
    if 'message' in i:
        print u"[{created_time}] {message}".format(**i)

