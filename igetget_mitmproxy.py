import json
import pymongo
from mitmproxy import ctx


def request(flow):
    flow.client = pymongo.MongoClient('localhost')
    flow.db = flow.client['igetget']
    flow.collection = flow.db['books']

def response(flow):
    url = 'https://entree.igetget.com/ebook2/v1/ebook/list'
    if flow.request.url.startswith(url):
        text = flow.response.text
        data = json.loads(text)
        books = data.get('c').get('list')
        for book in books:
            data = {
                'title': book.get('operating_title'),
                'cover': book.get('cover'),
                'summary': book.get('other_share_summary'),
                'price': book.get('price')
            }
            print(data)
            ctx.log.info(str(data))
            flow.collection.insert(data)
    flow.client.close()
