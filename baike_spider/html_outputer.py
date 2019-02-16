class HtmlOutputer(object):

    def __init__(self):
        self.datas = [] # 保存数据的列表

    def collet_data(self, data):
        # 数据不为空就加入列表
        if data is None:
            return
        self.datas.append(data)

    def output_html(self):
        # 打开一个output.html存放结果
        fout = open('output.html', 'w', encoding='utf-8')
        fout.write("<html>")
        fout.write("<body>")

        for data in self.datas:
            fout.write("<tr>")
            fout.write("<td>%s</td>" % data['url']) # 链接
            fout.write("<td>%s</td>" % data['title']) # 标题
            fout.write("<td>%s</td>" % data['summary']) # 介绍
            fout.write("</tr>")

        fout.write("</body>")
        fout.write("</html>")
        fout.close()