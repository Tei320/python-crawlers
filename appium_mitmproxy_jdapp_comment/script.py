import json


def response(flow):
    # ware_url = 'api.m.jd.com/client.action?functionId=wareBusiness' # 商品详情
    comment_url = 'api.m.jd.com/client.action?functionId=getCommentListWithCard' # 评论详情
    if comment_url in flow.request.url:
        text = flow.response.text
        data = json.loads(text)
        commetns = data.get('commentInfoList') or []
        for comment in commetns:
            if comment.get('commentInfo') and comment.get('commentInfo').get('commentData'):
                info = comment.get('commentInfo')
                nickname = info.get('userNickName')
                content = info.get('commentData')
                date = info.get('commentDate')
                print("*******************")
                print(nickname)
                print(content)
                print(date)