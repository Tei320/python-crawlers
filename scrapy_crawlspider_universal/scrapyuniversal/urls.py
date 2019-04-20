
def china_start_page(start, end):
    for page in range(start, end+1):
        yield 'https://tech.china.com/articles/index_' + str(page) + '.html'