import json
from mitmproxy import ctx

def response(flow):
    url = 'https://entree.igetget.com/ebook2/v1/ebook/list'
    if flow.request.url.startswith(url):
        text = flow.response.text
        data = json.loads(text)
        books = data.get('c').get('list')
        for book in books:
            data = {
                'name': book.get('book_name'),
                'cover': book.get('cover'),
                'summary': book.get('other_share_summary'),
                'price': book.get('price')
            }
            ctx.log.info(str(data))
